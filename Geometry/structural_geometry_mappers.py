"""
structural_geometry_mappers.py

Module that defines a few helper objects for wrangling and mapping structural geometric data.
"""

from sqlite3 import *
from math import sqrt
import numpy as np
from typing import Union, Dict
from dataclasses import dataclass
from collections import defaultdict

S7_GEOMETRY_QUERY = """SELECT
BeamNumber,
node1.X,
node1.Y,
node1.Z,
node2.X,
node2.Y,
node2.Z,
PropertyName
FROM BeamProperties AS BP
JOIN NodalCoordinates AS node1 ON node1.NodeNumber = BP.N1
JOIN NodalCoordinates AS node2 ON node2.NodeNumber = BP.N2;"""

S7_FORCE_QUERY = """SELECT
BeamNumber,
ResultCase,
ResultCaseName,
Position,
Fx,
Fy,
Fz,
Mx,
My,
Mz
FROM BeamForces;"""


def query_from_sql(db_fp: str, query: str = S7_GEOMETRY_QUERY, results_as_dict=False) -> list[dict]:
    """
    Retrieve beam geometry from a SQLite database.
    Each row returned is a tuple:
    (BeamNumber, node1.X, node1.Y, node1.Z, node2.X, node2.Y, node2.Z)
    """
    connection = connect(db_fp)
    if results_as_dict:
        connection.row_factory = Row
    cursor = connection.cursor()

    if results_as_dict:
        results = [dict(row) for row in cursor.execute(query).fetchall()]
    else:
        results = cursor.execute(query).fetchall()

    connection.close()
    return results


@dataclass
class Node:
    x: float
    y: float
    z: float

    def __eq__(self, other):
        if isinstance(other, Node):
            if sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2) < 0.0001:
                return True
        elif isinstance(other, list) or isinstance(other, tuple):
            if sqrt((other[0] - self.x) ** 2 + (other[1] - self.y) ** 2 + (other[2] - self.z) ** 2) < 0.0001:
                return True
        return False


class Beam:
    """Minimalist representation of a beam object.

    Allows for indexing of the end points that define the beam with an override to __getitem__()."""

    def __init__(self, number: int, start: Union[tuple, int], end: Union[tuple, int], profile: str, group: str):
        self.number = int(number)
        self.start = start
        self.end = end
        self.profile = profile
        self.group = group
        self.length = self._get_length()

    def __getitem__(self, item):
        # If indexed, returns the start and end point objects of the beam
        if isinstance(item, int):
            return [self.start, self.end][item]
        else:
            raise ValueError(f"Index must be an integer, {type(item)}")

    def __str__(self):
        return f"{self.number} | {self.start} -> {self.end} | {self.profile} | {self.group}"

    def __repr__(self):
        return self.__str__()

    def _get_length(self):
        length = sqrt((self.end[0] - self.start[0])**2 + (self.end[1] - self.start[1])**2 + (self.end[2] - self.start[2])**2)
        return length


class GeometricTransformer:
    def __init__(self):
        # The transformation is stored as a 4x4 homogeneous transformation matrix.
        # It combines rotation, translation, and uniform scaling.
        self.transformation = None

    @staticmethod
    def _create_frame(p0: list, p1: list, p2: list):
        """
        Given three non-collinear points p0, p1, p2, create an orthonormal frame.
        The frame has:
            - origin at p0,
            - the first axis along (p1 - p0),
            - the second axis defined by the component of (p2 - p0) orthogonal to (p1 - p0),
            - the third axis computed as the cross product of the first two axes.
        """
        p0 = np.asarray(p0, dtype=float)
        p1 = np.asarray(p1, dtype=float)
        p2 = np.asarray(p2, dtype=float)

        # First axis: from p0 to p1.
        v1 = p1 - p0
        norm_v1 = np.linalg.norm(v1)
        if norm_v1 < 1e-8:
            raise ValueError("p0 and p1 are too close; cannot define a valid axis.")
        ex = v1 / norm_v1

        # Second axis: remove the component of (p2-p0) along ex.
        v2 = p2 - p0
        proj = np.dot(v2, ex) * ex
        ey_temp = v2 - proj
        norm_ey = np.linalg.norm(ey_temp)
        if norm_ey < 1e-8:
            raise ValueError("p0, p1, and p2 are collinear; cannot define a valid plane.")
        ey = ey_temp / norm_ey

        # Third axis: cross product of ex and ey.
        ez = np.cross(ex, ey)
        norm_ez = np.linalg.norm(ez)
        if norm_ez < 1e-8:
            raise ValueError("Computed third axis is zero; something went wrong.")
        ez /= norm_ez

        return p0, ex, ey, ez

    def set_mapping_points(self, points_model1: list[list], points_model2: list[list]):
        """
        Set the mapping by providing three corresponding points in model1 and model2.
        This method computes a similarity transformation (rotation, translation,
        and uniform scaling) that maps points from model1 to model2.

        Parameters:
            points_model1: list or tuple of three points (each a 3-element array-like)
            points_model2: list or tuple of three points (each a 3-element array-like)
        """
        if len(points_model1) != 3 or len(points_model2) != 3:
            raise ValueError("Exactly three points are required for both coordinate systems.")

        # Create coordinate frames for model1 and model2.
        O1, e1, e2, e3 = self._create_frame(*points_model1)
        O2, f1, f2, f3 = self._create_frame(*points_model2)

        # Construct rotation matrices from the frames (each column is a basis vector).
        R1 = np.column_stack((e1, e2, e3))
        R2 = np.column_stack((f1, f2, f3))

        # Compute the rotation component ignoring scaling for now.
        R = R2 @ np.linalg.inv(R1)

        # Compute a uniform scaling factor.
        # Here we use the distance between the first and second points.
        p0_model1 = np.asarray(points_model1[0], dtype=float)
        p1_model1 = np.asarray(points_model1[1], dtype=float)
        p0_model2 = np.asarray(points_model2[0], dtype=float)
        p1_model2 = np.asarray(points_model2[1], dtype=float)

        dist_model1 = np.linalg.norm(p1_model1 - p0_model1)
        dist_model2 = np.linalg.norm(p1_model2 - p0_model2)

        if dist_model1 < 1e-8:
            raise ValueError("The first two points in model1 are too close to compute scaling.")

        scale = dist_model2 / dist_model1

        # Integrate the scaling into the rotation matrix.
        R_scaled = scale * R

        # Compute the translation component.
        # The transformed origin should match: O2 = R_scaled * O1 + t
        t = O2 - R_scaled @ O1

        # Assemble the 4x4 homogeneous transformation matrix.
        self.transformation = np.eye(4)
        self.transformation[:3, :3] = R_scaled
        self.transformation[:3, 3] = t

    def transform_point(self, point: tuple) -> np.ndarray:
        """
        Transform a single 3D point from model1 coordinates to model2 coordinates.

        Parameters:
            point: a 3-element array-like representing the point in model1.

        Returns:
            A NumPy array representing the transformed point in model2.
        """
        if self.transformation is None:
            raise ValueError("Transformation has not been set. Call set_mapping_points() first.")

        point_homog = np.append(np.asarray(point, dtype=float), 1.0)
        transformed_homog = self.transformation @ point_homog
        return transformed_homog[:3]

    def transform_beam(self, beam: Beam) -> Beam:
        """
        Transform a line defined by a start point and an end point from model1
        to model2 coordinates.

        Parameters:
            start: a 3-element array-like representing the start point.
            end: a 3-element array-like representing the end point.

        Returns:
            A tuple (start_transformed, end_transformed) where each is a NumPy array
            representing the transformed point in model2.
        """
        start_transformed = self.transform_point(beam.start)
        end_transformed = self.transform_point(beam.end)
        return Beam(beam.number, start_transformed, end_transformed, beam.profile)


class BeamJoiner:
    def __init__(self, model_beams: list[Beam], node_dict: dict = None,  tolerance=0.005,
                 target_groups: tuple[str, ...] = ()):
        """
        Class that allows for joining of strings of beams based on rule sets.

        Iterates through the list of model beams to find lists of elements that:
        - Are collinear
        - Meet the connectivity criteria (share a node, and do not have intersection with more members)
        - Have the same profile

        Target groups is an optional parameter that can allow for only some groups to be considered in the output.
        All members provided in the model_beams list will be used for connectivity checks.
        Only the target_group elements will have grouping result returned.
        """
        self.model_beams = model_beams
        self.tolerance = tolerance
        self.target_groups = target_groups

        if len(target_groups) > 0:
            self.target_beams = [b for b in self.model_beams if b.group in self.target_groups]
        else:
            self.target_beams = self.model_beams

        if node_dict:
            self.node_dict = node_dict
        else:
            self.node_dict = self._get_node_dict()

        self.node_element_dict, self.beam_topology_dict = self._get_nodal_association_and_beam_dicts()

        self.beam_groups = self.group_collinear_beams()

    def _get_node_dict(self) -> Dict[int, Node]:
        """
        Method to create a node dictionary.

        Method is only invoked if node_dict has not been provided as an input.
        The nodes are determined by finding common points from the full collection of model
        beam coordinates. If the points occur within a particular tolerance, a node with a
        unique number is created and added to the dictionary.

        Effectively allows a collection of geometrically defined beams to be converted to
        a collection of topologically defined beams.
        :return: node_dict
        """

        # Start with an empty list
        node_list = []
        for beam in self.model_beams:
            node1 = Node(*beam.start)
            node2 = Node(*beam.end)
            if node1 not in node_list:
                node_list.append(node1)
            if node2 not in node_list:
                node_list.append(node2)

        # Once the list has been completely populated, convert it to a dictionary
        node_dict = {i: n for i, n in zip(range(1, len(node_list) + 1), node_list)}

        return node_dict

    def _get_nodal_association_and_beam_dicts(self) -> tuple[Dict[int, list], Dict[int, list]]:

        node_list = [i for i in self.node_dict.keys()]
        node_list.sort()

        # Create associativity dictionary
        node_element_dict = defaultdict(list)

        beam_topology_dict = {}
        # Assign nodes to the end of each beam
        for beam in self.model_beams:
            beam_nodes = []
            for i in range(len(node_list)):
                if beam.start == self.node_dict[i + 1]:
                    beam_nodes.append(i + 1)
                    node_element_dict[i + 1].append(beam.number)
                if beam.end == self.node_dict[i + 1]:
                    beam_nodes.append(i + 1)
                    node_element_dict[i + 1].append(beam.number)
            beam_topology_dict[beam.number] = beam_nodes

        return node_element_dict, beam_topology_dict

    def _check_collinear(self, beam1, beam2) -> bool:
        """
        Determines if two beams are collinear.
        """

        # Convert the start and end points into numpy arrays for vector arithmetic.
        start1 = np.array(beam1.start)
        end1 = np.array(beam1.end)
        start2 = np.array(beam2.start)
        end2 = np.array(beam2.end)

        # Compute the direction vectors of each beam.
        vec1 = end1 - start1
        vec2 = end2 - start2

        # Use the cross product to determine collinearity.
        cross_prod = np.cross(vec1, vec2)

        # If the magnitude of the cross product is close to zero, the vectors are collinear.
        if np.linalg.norm(cross_prod) < self.tolerance:
            return True
        else:
            return False

    def _check_connectivity(self, beam1: Beam, beam2: Beam) -> bool:
        """
        Determines whether the two candidate beams satisfy the connectivity criteria.

        Evaluates to true if the following conditions are satisfied:
        - The beams share a node
        - The node in question is only shared by those two beams
        """

        beam1_nodes = self.beam_topology_dict[beam1.number]
        beam2_nodes = self.beam_topology_dict[beam2.number]

        # The below logic checks to see if they share a node and if that node is only connected to two elements
        for node_num in beam1_nodes:
            if node_num in beam2_nodes:
                elements_connected_to_node = self.node_element_dict[node_num]
                if len(elements_connected_to_node) == 2:
                    return True

        return False

    @staticmethod
    def _check_profile_match(beam1: Beam, beam2: Beam) -> bool:
        if beam1.profile == beam2.profile:
            return True
        else:
            return False

    def _check_membership(self, beam1: Beam, beam2: Beam) -> bool:
        """
        Function for checking whether the referenced beams occur as part of the same member group.
        :param beam1:
        :param beam2:
        :return:
        """
        if self._check_collinear(beam1, beam2) and self._check_connectivity(beam1, beam2) \
                and self._check_profile_match(beam1, beam2):
            return True
        return False

    def _find(self, x: int, parent: dict) -> int:
        """Compresses the path within the dict."""
        if parent[x] != x:
            parent[x] = self._find(parent[x], parent)
        return parent[x]

    def _union(self, x: int, y: int, parent: dict):
        """Merges elements if they contain a common parent."""
        root_x = self._find(x, parent)
        root_y = self._find(y, parent)
        if root_x != root_y:
            parent[root_y] = root_x

    def group_collinear_beams(self) -> list[list[Beam]]:
        """
        Groups beams that are collinear (and satisfy additional rules) using a union-find structure.
        """
        # Step 1: Initialize each beam as its own set.
        parent = {beam.number: beam.number for beam in self.target_beams}

        # Step 2: Merge sets for beams that are collinear and satisfy connectivity.
        # Can change the below line to only iterate through the target
        n = len(self.target_beams)
        progress_increment = int(n / 100)
        print(f"Commencing beam segment grouping. Target groups: {self.target_groups}")
        for i in range(n):
            if i == progress_increment:
                print(f"\t{i / n:.2%} of grouping complete")
                progress_increment += int(n / 100)
            for j in range(i + 1, n):
                # Ensure beams are collinear and pass the membership checks.
                if self._check_membership(self.target_beams[i], self.target_beams[j]):
                    self._union(self.target_beams[i].number, self.target_beams[j].number, parent)

        # Step 3: Group beams by their representative.
        groups = {}
        for beam in self.target_beams:
            root = self._find(beam.number, parent)
            groups.setdefault(root, []).append(beam)
        group_lists = list(groups.values())
        return group_lists


class BeamMapper:
    def __init__(self, model1_beams: list[Beam], model2_beams: list[Beam]):
        """
        Initialize the mapper with two sets of line segments.

        Each set is expected to be a list of line segments. Each line segment
        is defined as a tuple or list: (start, end), where start and end are
        3-element array-like objects (e.g. lists, tuples, or NumPy arrays).

        The lines are implicitly assigned IDs based on their position in the list:
        for model 1, the first line is ID 1, the second is ID 2, etc., and similarly
        for model 2.

        Parameters:
            model1_beams: list of line segments from model 1.
            model2_beams: list of line segments from model 2.
        """
        self.model1_beams = model1_beams
        self.model2_beams = model2_beams

    @staticmethod
    def _line_midpoint(line):
        """
        Given a line segment (start, end), return its midpoint.
        """
        start = np.asarray(line[0], dtype=float)
        end = np.asarray(line[1], dtype=float)
        return (start + end) / 2.0

    @staticmethod
    def _project_point_onto_line(point: list, beam: Beam) -> tuple[np.ndarray, float]:
        """
        Project a point onto a line segment defined by (A, B).

        Parameters:
            point: the 3D point (array-like) to project.
            beam: a tuple (A, B) where A and B are the endpoints of the line.

        Returns:
            A tuple (proj_point, t, dist) where:
                - proj_point is the projection of the point onto the infinite line
                  through A and B,
                - t is the scalar parameter such that proj_point = A + t*(B-A),
                  and
                - dist is the perpendicular distance from the point to the line.
        """
        A = np.asarray(beam[0], dtype=float)
        B = np.asarray(beam[1], dtype=float)
        point = np.asarray(point, dtype=float)
        AB = B - A
        norm_sq = np.dot(AB, AB)

        if norm_sq < 1e-12:
            raise ValueError("The endpoints of the line are too close to define a valid line.")
        # Compute scalar projection parameter t
        t = np.dot(point - A, AB) / norm_sq
        proj_point = A + t * AB
        dist = np.linalg.norm(point - proj_point)
        return proj_point, t, dist

    def map_lines(self, tolerance: Union[float, int], max_tolerance: Union[float, int]) -> dict:
        """
        Map each line segment from model 1 to a candidate line segment in model 2.

        For each model 1 beam, we project its start, mid, and end points onto each model 2 beam.
        Only candidates for which all three projections:
            - fall within the candidate segment (i.e. 0.0 <= t <= 1.0), and
            - have a perpendicular distance <= tolerance
        are considered.
        Among those, the candidate with the smallest maximum distance is chosen.
        If no candidate qualifies, the mapping for that beam is set to None.

        :returns:
            A dictionary mapping model1 beam IDs to the matching model2 beam ID (or None if no match).
        """
        mapping = {}

        for m1_beam in self.model1_beams:
            best_match_id = None
            best_metric = None  # We will use the maximum of the three distances as our "metric"

            # Compute the midpoint of m1_beam using the helper method
            mid_point = self._line_midpoint((m1_beam.start, m1_beam.end))

            for m2_beam in self.model2_beams:
                # Project the start point
                proj_point1, t1, dist1 = self._project_point_onto_line(m1_beam.start, m2_beam)
                # Project the midpoint
                proj_point_mid, t_mid, dist_mid = self._project_point_onto_line(mid_point, m2_beam)
                # Project the end point
                proj_point2, t2, dist2 = self._project_point_onto_line(m1_beam.end, m2_beam)

                # Check that ALL projected points lie on the candidate segment (t between 0 and 1)
                # and that their distances are within the tolerance.
                if (0.0 - tolerance <= t1 <= 1.0 + tolerance and dist1 <= tolerance and
                        0.0 - tolerance <= t_mid <= 1.0 + tolerance and dist_mid <= tolerance and
                        0.0 - tolerance <= t2 <= 1.0 + tolerance and dist2 <= tolerance):

                    # Use the worst (largest) of the three distances as the candidate metric.
                    candidate_metric = max(dist1, dist_mid, dist2)

                    # Update if this candidate is a better match.
                    if best_metric is None or candidate_metric < best_metric:
                        best_metric = candidate_metric
                        best_match_id = m2_beam.number

            mapping[m1_beam.number] = best_match_id

        return mapping


def _check_inclusion(candidate: str, test_strings: tuple[str, ...]):
    for t in test_strings:
        if t in candidate:
            return True
    return False


def map_models(model1_beams: list[Beam], model2_beams: list[Beam], src_mpts: list, dst_mpts: list,
               tolerance: Union[int, float] = 200):
    """Transforms objects in one model from one cartesian axis system to another, and
    finds the mapping of objects between the models.

    Object coordinates from model 1 are transformed using the GeometricTransformer class.
    Object mappings between models are then found using the LineMapper class.

    :returns
        Prints the mapping as a series of tab separated values.
        Returns None"""

    transformer = GeometricTransformer()
    transformer.set_mapping_points(src_mpts, dst_mpts)

    # Apply the transformation to each target point.
    transformed_beams = [transformer.transform_beam(b) for b in model1_beams]
    m1_trans_beam_dict = {b.number: b for b in transformed_beams}
    m2_beam_dict = {b.number: b for b in model2_beams}

    mapper = BeamMapper(transformed_beams, model2_beams)
    mapping = mapper.map_lines(tolerance, tolerance)

    tab = "\t"
    print("Mapping of target model lines (transformed) to reference model lines:")
    for m1_trans_beam_number, m2_beam_number in mapping.items():
        m1_trans_beam = m1_trans_beam_dict[m1_trans_beam_number]
        if m2_beam_number is not None:
            m2_beam = m2_beam_dict[m2_beam_number]
            print(
                f"{m1_trans_beam.number}\t{tab.join(str(c) for c in m1_trans_beam.start)}\t{tab.join(str(c) for c in m1_trans_beam.end)}\t{m2_beam_number}\t{m1_trans_beam.profile}\t{m2_beam.profile}")
        else:
            print(f"{m1_trans_beam.number}\tNone")


if __name__ == "__main__":
    # Define
    strand_1_db = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.3\V1_3_3-Umax-LB\V1_3_3_LB_GmaxNLA.db"
    strand_2_db = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.3.5\V1_3_5_LB_Gmax\V1_3_5_LB_GmaxNLA.db"

    # These points represent the same physical locations in both models.
    # Points in source coordinate system (model 1):
    source_mapping_points = [
        [0.0, 0.0, 0.0],  # Point A
        [100.0, 0.0, 0.0],  # Point B
        [0.0, 200.0, 0.0]  # Point C
    ]

    # Corresponding points in the destination coordinate system (model 2):
    destination_mapping_points = [
        [0.0, 0.0, 0.0],  # Mapped A
        [100.0, 0.0, 0.0],  # Mapped B
        [0.0, 200.0, 0.0]  # Mapped C
    ]

    # Have used the below filters to only match on a subset of profiles (mostly to ignore stair members)
    section_filters = ("CHS", "RHS", "SHS", "UB", "UC")

    # Tolerance for the geometric mapping procedure
    # If multiple beams lie within the tolerance, the mapping will choose the beam with an end point that is closest
    # to the target (either start or end)
    tolerance = 0.2



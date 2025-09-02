import os

if __name__ == '__main__':

    # ----------------------------------------------------------------------
    # INPUTS
    # ----------------------------------------------------------------------
    fp = r"C:\Users\Josh.Finnin\Mott MacDonald\MBC SAM Project Portal - 01-Structures\Work\Design\05 - Roof\01 - FE Models\V1.4.5"
    global_axes = True

    file_names = [i for i in os.listdir(fp) if ".NLA" in i]
    # file_names.sort(key=lambda x: int(x.split(" ")[0]))

    for file in file_names:
        file_path = os.path.join(fp, file)
        if global_axes:
            print(
                f'r"{file_path}": (r"{os.path.join(fp, file.split(".")[0]) + ".st7"}", r"{os.path.join(fp, "Global Axes Parquet", file.split(".")[0])}"),')
        else:
            print(
                f'r"{file_path}": (r"{os.path.join(fp, file.split(".")[0]) + ".st7"}", r"{os.path.join(fp, "Principal Axes Parquet", file.split(".")[0])}"),')


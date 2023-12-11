def get_input(day: int) -> str:
    floc = 'C:/Users/ABled/PycharmProjects/AoC-2023/inputs/'
    fname = str(day) + ".txt"

    with open(floc + fname) as file:
        return file.read()

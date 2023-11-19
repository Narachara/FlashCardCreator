
my_string ="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

def cut(input_string, chunk_size=40):
    space_positions = [i for i in range(len(input_string)) if input_string[i].isspace()]
    cut_positions = [i for i in range(0, 500, chunk_size)]

    cutarray = [0] * len(cut_positions)

    for i in range(len(cut_positions)-1):
        for space in space_positions:
                if cut_positions[i] - 10 < space < cut_positions[i + 1] + 10:
                    cutarray[i+1] = space

    for i in range(len(cut_positions)-1):
        start = cutarray[i]
        end = cutarray[i+1]
        chunk = input_string[start:end].strip()
        print(chunk)


cut(my_string)
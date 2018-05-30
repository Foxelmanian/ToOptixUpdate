

file = open("no_design_space.inp", "w")
maximum_element_id = 1000

file.write("*ELSET \n")
counter = 0
for ii in range(maximum_element_id):

    file.write(str(ii) + ",")

    counter += 1

    if counter == 8:
        counter = 0
        file.write("\n")
file.write("\n")

file.close()


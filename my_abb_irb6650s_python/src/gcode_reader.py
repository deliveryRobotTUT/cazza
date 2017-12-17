import numpy as np

# function to read the "G-code" file and create way-points
def get_waypoints(file_name):
    temp_x_y = []
    waypoints = []
    # z_points = []
    z_found = False
    z_found_num = 0
    z_value = 0
    z_value_prev = 0
    with open(file_name, 'r') as f_gcode:
        for line in f_gcode:
            if 'G1' in line and ';' not in line:
                # find the lines to get the Z-coordinate or height of print
                if 'Z' in line:
                    if z_found_num != 0:
                        z_found = True
                        z_value_prev = z_value
                    # print z_value_prev
                    z_found_num = z_found_num + 1
                    z_index_start = line.find('Z') + 1
                    z_index_end = line.find(' ', z_index_start)
                    z_value = float(line[z_index_start:z_index_end])
                else:
                    # find the X-Y coordinates for printing
                    z_found = False
                    if 'X' and 'Y' in line:
                        x_index_start = line.find('X') + 1
                        x_index_end = line.find(' ', x_index_start)
                        y_index_start = line.find('Y') + 1
                        y_index_end = line.find(' ', y_index_start)
                        x_value = float(line[x_index_start:x_index_end])
                        y_value = float(line[y_index_start:y_index_end])
                        temp_x_y.append([x_value, y_value])
            if z_found:
                # append the way-point array with newer Z-values and its corresponding X-Y coordinates
                waypoints.append([z_value_prev, temp_x_y])
                temp_x_y = []
    waypoints.append([z_value, temp_x_y])
    return waypoints


if __name__ == "__main__":
    filename = 'Base side 1 rev3.gcode'
    w_points = get_waypoints(filename)

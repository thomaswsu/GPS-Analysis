def calc_velocity(distance: list, decimal_time: list):
    assert(len(distance) == len(decimal_time))
    ret = [0]

    for i in range(1, len(distance)):
        deltaT = decimal_time[i] - decimal_time[i - 1]
        if deltaT == 0:
            print("There was a division by 0. There is some kind of time error.")
            ret.append(0)
            continue
        ret.append(distance[i] / deltaT)
    return(ret)

def calc_acc(velocity_list: list, decimal_time: list):
    ret = [0, 0]

    for i in range(2, len(velocity_list)):
        deltaT = decimal_time[i] - decimal_time[i - 1]
        if deltaT == 0:
            print("There was a division by 0. There is some kind of time error.")
            ret.append(0)
            continue
        ret.append(velocity_list[i] / deltaT)
    
    return(ret)

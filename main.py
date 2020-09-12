import pandas # open csv files
import utc
import longlat
import movement
import os
""" Don't forget to install pandas and geopy
Usage path should be set to /~/GPS_Analysis/Manual Algorithm
To run: python3 -i main.py 
"""


if __name__ == "__main__":
    f = ""
    file_name = ""
    print("Welcome! Make sure your working directory contains \"Data/Barranquilla/\"")
    while len(file_name) == 0  or not(os.path.isfile(f)):
        file_name = input("Enter a csv path. Example: \"Data/D01/3_15091000 Bar 1.CSV\"\nfile path: ") 
            # example: 3_15091000 Bar 1.CSV
        f = file_name
        if len(file_name) == 0:
            print("Enter a valid file name")
        elif not(os.path.isfile(f)): # file_name = False when no input  
            print("\"{}\" is not a valid path. Enter a different path.".format(f))
    
    """ ratio of data to use. 0.5 is half the data. 0.1 is 10% of data. 1.0 is 100% of data.
    """
    portion_of_data = 1.0 

    """ Parameter to decide when there is an error. If disDiff < disError then we mark it as an error
    Haven't experimented with this value at all! 
    """
    disError = 100  

    print("Reading CSV: {}".format(f))
    data = pandas.read_csv(f)

    utc_time = []
    lattitude = []
    longitute = []
    distance_traveled = []
    true_movement = []
    for i in range(int(len(data) / portion_of_data)):
        """ Read in data from CSV -  True Movement is for validation purposes. 
        """
        utc_time.append(int(data["TIME"][i]))
        lattitude.append(str(data["LATITUDE N/S"][i]))
        longitute.append(str(data["LONGITUDE E/W"][i]))
        true_movement.append(int(data["MOVEMENT"][i])) 

    """ Calculate relevent values in list form.
    """    
    distance_traveled = longlat.convert_long_and_lat_list_to_distance_list(lattitude, longitute)
    speed = movement.calc_velocity(distance_traveled, utc_time)
    acceleration = movement.calc_acc(distance_traveled, utc_time)

    """ Note that event and error start with 0 or non-error values as a starting point. (an assumpition) 
    This is because it is not possible to deterime if the truck is moving or not at time 0.
    (With our algorithm)

    Event = 1 -> Stopping
    Event = 0 -> Moving

    Error = 1 -> Error
    Error = 0 -> No Error
    """

    """ Not sure if I should make the very first event a "0" or a "1". 
    Some sheets start at 0 some start at 1
    """
    event = [0] 
    error = [0]

    """ Create csv as a record. This is more for debugging purposes but can also be handy for analyzing data.
    """
    outfile = file_name[:-4] + "_predicted.csv" # Chop off .csv from filename
    f = open(outfile,"w")

    f.write("UTC_TIME, Distance, Speed, Acceleration, True Event, Event, Error\n")
    f.write("{}, {}, {}, {}, {}, {}, {}\n".\
                    format(utc_time[0], distance_traveled[0], speed[0], acceleration[0],\
                         true_movement[0], event[0], error[0]))

    for i in range(1, len(utc_time)):
        timeDif = utc_time[i] - utc_time[i - 1] # calculate the time difference from last data point
        """ timeDif>0 & accdcc<=8 & dist<=38*timeDif?
        """
        if not((timeDif > 0) and (acceleration[i] <= 8) and \
            (distance_traveled[i] <= 38 * timeDif)):
            event.append(event[-1])
            error.append(1)
            f.write("{}, {}, {}, {},{}, {}, {}\n".\
                format(utc_time[i], distance_traveled[i], speed[i], acceleration[i],\
                     true_movement[i], event[-1], error[-1]))
        
        elif speed[i] == 0:
            """ Speed=0?
            Note that this is very weird. But it yields better results by a long shot! 
            """
            event.append(0)
            error.append(0)
            f.write("{}, {}, {}, {},{}, {}, {}\n".\
                format(utc_time[i], distance_traveled[i], speed[i], acceleration[i],\
                     true_movement[i], event[-1], error[-1]))
        
        elif not(distance_traveled[i] < disError):
            """ disDif<disError?
            Notice the "not()" This checks for the "NO" case insted of the "YES" case.
            """
            event.append(event[-1])
            error.append(1)
            f.write("{}, {}, {}, {},{}, {}, {}\n".\
                format(utc_time[i], distance_traveled[i], speed[i], acceleration[i],\
                     true_movement[i], event[-1], error[-1]))
        else:
            """ Supposedly, Flag == True but that doesn't really make sense...
            I think "Flag" is trying to check if there's a error, but doesn't look like its needed...
            """
            event.append(1)
            error.append(1)
            f.write("{}, {}, {}, {},{}, {}, {}\n".\
                format(utc_time[i], distance_traveled[i], speed[i], acceleration[i],\
                     true_movement[i], event[-1], error[-1]))

    """ Calculate error relative to Movement column. 
    "Accuracy without error" refers to the differences between the predicted movement (event) and true movement.
    "Accuracy without error" doesn't count the values the were marked as a error. 
    """
    accuracy_without_error = 0
    accuracy_with_error = 0
    for i in range(1, len(true_movement)):
        if true_movement[i] == event[i]:
            accuracy_without_error += 1
        if true_movement[i] == event[i] or error[i] == 1:
            accuracy_with_error += 1

    print("Accuracy without error: {}".format(accuracy_without_error / len(true_movement)))
    print("Accuracy with error: {}".format(accuracy_with_error/ len(true_movement)))

    f.close()
    print("Program Finished")


"""
Reading CSV: Data/Results/3_15091000 Bar 1 copy.CSV
Accuracy with error: 0.7184273448538202
Accuracy without error: 0.9187044886425388
Program Finished

Reading CSV: Data/Results/3_15091100 Bar 2 copy.CSV
Accuracy with error: 0.8255676657584015
Accuracy without error: 0.9376021798365123
Program Finished

Reading CSV: Data/Results/3_15091200 Bar 3 copy.CSV
Accuracy with error: 0.6603443726085235
Accuracy without error: 0.7873730043541364
Program Finished

Reading CSV: Data/Results/3_15091400 Bar 4 copy.CSV
Accuracy with error: 0.8360280044323563
Accuracy without error: 0.9241966354387026
Program Finished

Reading CSV: Data/Results/3_15091701 Bar 5 copy.CSV
Accuracy with error: 0.6640625
Accuracy without error: 0.9597916666666667
Program Finished
"""
def convertTime (time):
    temp = time.split(':')
    timeMinutes = (int(temp[0])*60)+int(temp[1])+int(temp[2])/60
    return timeMinutes

def create_time_columns(bare_frame):

    # convert to integers
    bare_frame["Swim Minutes"] = bare_frame["Swim"].apply(convertTime)
    bare_frame["T1 Minutes"] = bare_frame["T1"].apply(convertTime)
    bare_frame["Bike Minutes"] = bare_frame["Bike"].apply(convertTime)
    bare_frame["T2 Minutes"] = bare_frame["T2"].apply(convertTime)
    bare_frame["Run Minutes"] = bare_frame["Run"].apply(convertTime)
    # bare_frame["Elapsed Minutes"] = bare_frame["Chip Elapsed"].apply(convert_time)

    # create cumulative times
    bare_frame["Swim+T1"] = round(bare_frame["Swim Minutes"] + bare_frame["T1 Minutes"], 2)
    bare_frame["Plus Bike"] = round(bare_frame["Swim+T1"] + bare_frame["Bike Minutes"], 2)
    bare_frame["Plus T2"] = round(bare_frame["Plus Bike"] + bare_frame["T2 Minutes"], 2)
    bare_frame["Total"] = round(bare_frame["Plus T2"] + bare_frame["Run Minutes"], 2)

    return bare_frame
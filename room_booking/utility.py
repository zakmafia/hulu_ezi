# Utility function (time_converter)
def booking_time_am_pm_converter(booking_time):
    splited = None
    booking_time_am_pm = None
    if len(booking_time) == 6:
        splited = booking_time.split(' ')
        booking_time = splited[0] + ':00 ' + splited[1]
    elif len(booking_time) == 7:
                splited = booking_time.split(' ')
                booking_time = splited[0] + ':00 ' + splited[1]
    splited_time = booking_time.split(" ")
    if splited_time[1].startswith("a"):
        booking_time_am_pm = splited_time[0] + " AM"
    else:
        booking_time_am_pm = splited_time[0] + " PM"

    return booking_time_am_pm
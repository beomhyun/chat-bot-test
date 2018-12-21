import datetime
dt = datetime.datetime.now()

if dt.weekday() == 0 :
    start = dt.day
    end = dt.day +6
elif dt.weekday() == 1:
    start = dt.day-1
    end = dt.day +5
elif dt.weekday() == 2:
    start = dt.day-2
    end = dt.day +4
elif dt.weekday() == 3:
    start = dt.day-3
    end = dt.day +3
elif dt.weekday() == 4:
    start = dt.day-4
    end = dt.day +2
elif dt.weekday() == 5:
    start = dt.day-5
    end = dt.day +1
elif dt.weekday() == 6:
    start = dt.day -6
    end = dt.day
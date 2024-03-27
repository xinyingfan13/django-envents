import datetime
from models import Timetable


def calendar(request):
    place = int(request.POST.get("place"))
    event_date = request.POST.get("event_date")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    timetables = Timetable.objects.filter(place=place, event_date=event_date)

    s_t = start_time.split(':')
    e_t = end_time.split(':')

    start = datetime.time(int(s_t[0]), int(s_t[1]))
    end = datetime.time(int(e_t[0]), int(e_t[1]))
    marker = False
    counter = 0
    for timetable in timetables:
        print(timetable)
        counter += 1
        if not ((timetable.start_time <= start <= timetable.end_time)
                or (timetable.start_time <= end <= timetable.end_time)
                or (start <= timetable.start_time and end >= timetable.end_time)):
            marker = True
            break
    return marker or counter == 0



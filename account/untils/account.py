from datetime import date

from admi.models import DayNumber


def day_visit(request):
    if today := DayNumber.objects.filter(day=date.today()):
        temp = today[0]
        temp.visit_count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.visit_count = 1
    temp.save()

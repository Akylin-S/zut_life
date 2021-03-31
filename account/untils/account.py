from datetime import date

from admi.models import DayNumber


def day_visit(request):
    today = DayNumber.objects.filter(day=date.today())
    if today:
        temp = today[0]
        temp.visit_count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.visit_count = 1
    temp.save()

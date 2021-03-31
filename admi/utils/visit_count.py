from datetime import date

from admi.models import DayNumber


def visit_count(request):
    today = DayNumber.objects.filter(day=date.today())
    if today:
        temp = today[0]
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.visit_count = 1
    temp.save()
    today = DayNumber.objects.filter(day=date.today())[0]
    print(today.visit_count)
    return today

def five_visit(request):
    day = DayNumber.objects.all().order_by('-day')
    day = day.order_by('day')
    return day

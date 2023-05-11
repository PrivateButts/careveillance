from celery import shared_task
from django.utils import timezone

from tracker.models import Schedule, Task


@shared_task
def CreateScheduledTasks():
    """Create tasks for schedules that are due."""
    for schedule in Schedule.objects.filter(reoccurrence__isnull=False):
        if schedule.time_next_due() < timezone.now():
            Task.objects.create(schedule=schedule)

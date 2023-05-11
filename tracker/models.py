from django.utils import timezone
from django.db import models

from careveillance.helpers import BaseModel


class Schedule(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    type = models.CharField(
        max_length=7,
        choices=(("time", "Time based"), ("counter", "Counter based")),
        default="counter",
        help_text=(
            "Time based schedules are for things that happen every x days/weeks/months. "
            + "Counter based schedules are for things that happen every x miles or uses."
        ),
    )
    tick = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="How often a counter based schedule should trigger (every 3,000 miles).",
    )
    unit = models.CharField(
        max_length=255, null=True, blank=True, help_text="The unit of the tick (miles, uses, etc)."
    )
    reoccurrence = models.DurationField(
        null=True,
        blank=True,
        help_text="How often a time based schedule should trigger (every 3 weeks).",
    )

    def time_next_due(self) -> timezone.datetime:
        """Return the next time this schedule is due."""
        if not self.task_set.filter(completed_at__isnull=False).exists():
            return self.created_at + self.reoccurrence
        return (
            self.task_set.filter(completed_at__isnull=False).latest("completed_at").completed_at
            + self.reoccurrence
        )

    def counter_next_due(self) -> float:
        """Return the next counter this schedule is due."""
        most_recent_log = self.counter_logs.latest("created_at")
        last_completed_task = self.task_set.filter(completed_at__isnull=False).latest(
            "completed_at"
        )
        base_value = last_completed_task.value if last_completed_task else 0
        current_value = most_recent_log.value if most_recent_log else 0
        return base_value + self.tick - current_value

    def __str__(self):
        return self.name


class Task(BaseModel):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.CharField(max_length=255, null=True, blank=True)

    def complete(self, user):
        """Mark this task as completed."""
        self.completed_at = timezone.now()
        self.completed_by = user
        self.save()

    @property
    def completed(self):
        return self.completed_at is not None

    def __str__(self):
        return self.name


class CounterLog(BaseModel):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    value = models.FloatField()

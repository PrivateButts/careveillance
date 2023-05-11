from datetime import timedelta
from django.test import TestCase

from tracker import factories


class ScheduleModelTestCase(TestCase):
    def test_time_next_due_empty(self):
        """Test that time_next_due returns the created_at time if no tasks have been completed."""
        schedule = factories.TimeScheduleFactory()
        self.assertEqual(schedule.time_next_due(), schedule.created_at + schedule.reoccurrence)

    def test_time_next_due_with_tasks(self):
        """Test that time_next_due returns the time of the last completed task plus the reoccurrence."""
        schedule = factories.TimeScheduleFactory()
        factories.TaskFactory(
            schedule=schedule, completed_at=schedule.created_at + timedelta(days=1)
        )
        self.assertEqual(
            schedule.time_next_due(),
            schedule.created_at + schedule.reoccurrence + timedelta(days=1),
        )

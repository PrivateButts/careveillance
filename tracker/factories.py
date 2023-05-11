from datetime import timedelta
from random import randint
import factory

from tracker.models import Schedule, Task, CounterLog


class TimeScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    name = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    type = "time"
    reoccurrence = factory.LazyAttribute(lambda s: timedelta(days=randint(1, 100)))


class CounterScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    name = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    type = "counter"
    tick = factory.Faker("pyint", min_value=1, max_value=1000)
    unit = factory.Faker("word")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    schedule = factory.SubFactory(TimeScheduleFactory)


class CounterLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CounterLog

    schedule = factory.SubFactory(CounterScheduleFactory)
    value = factory.Faker("pyint", min_value=1, max_value=1000)

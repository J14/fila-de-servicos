from django.db import models
from django.core.exceptions import ValidationError

from . import managers


class Person(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    people = models.ManyToManyField(
        Person,
        related_name="services",
        through="Queue",
    )

    def __str__(self):
        return self.name


class Queue(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        related_name="queue"
    )
    attending = models.BooleanField()
    attended = models.BooleanField(default=False)

    enqueue = managers.EnqueueManager()
    objects = models.Manager()

    class Meta:
        ordering = ('service', 'id')

    def __str__(self):
        return "{} - {} - {}".format(
            self.service, self.id, self.person
        )

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)

        if self.attending:
            exists = Queue.objects.filter(
                attending=True, service__id=self.service.id
            ).exclude(
                id=self.id
            ).exists()
            if exists:
                raise ValidationError(
                    "there can not be two attending person"
                    " in the same queue"
                )

    def save(self, *args, **kwargs):
        if not self.attending:
            if not Queue.enqueue.filter(service=self.service).exists():
                self.attending = True

        super().save(*args, **kwargs)

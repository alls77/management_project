from django.db import models


class AbstractNameEntity(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class AbstractTimeRangeEntity(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    class Meta:
        abstract = True


class AbstractEmailEntity(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        abstract = True


class AbstractWorker(AbstractNameEntity):
    surname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)

    class Meta:
        abstract = True

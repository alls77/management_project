from django.db import models

STATUSES = {
    'NEW': 0,
    'APPROVED': 1,
    'CANCELLED': 2,
    'FINISHED': 3
}


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


class Company(AbstractNameEntity):
    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return f'Company: {self.name} ({self.id})'


class Manager(AbstractWorker, AbstractEmailEntity):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return f'{self.company}; manager:{self.name} ({self.id})'


class Work(AbstractNameEntity):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='works')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.company}; work:{self.name} ({self.id})'


class Worker(AbstractWorker):
    def __str__(self):
        return f'{self.name} {self.surname} ({self.id})'


class Workplace(AbstractNameEntity):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='workplaces')
    worker = models.ForeignKey(Worker, blank=True, null=True, on_delete=models.SET_NULL, related_name='workplaces')
    status = models.IntegerField(choices=(
        (STATUSES['NEW'], 'New'),
        (STATUSES['APPROVED'], 'Approved'),
        (STATUSES['CANCELLED'], 'Cancelled'),
        (STATUSES['FINISHED'], 'Finished')), blank=True, null=True)
    time_limit = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['worker', 'status'], name='unique_worker')]

    def __str__(self):
        return f'{self.work}; workplace:{self.name} ({self.id})'


class WorkTime(AbstractTimeRangeEntity):
    workplace = models.ForeignKey(Workplace, on_delete=models.PROTECT, related_name='worktimes')
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, related_name='worktimes')
    status = models.IntegerField(choices=(
        (STATUSES['NEW'], 'New'),
        (STATUSES['APPROVED'], 'Approved'),
        (STATUSES['CANCELLED'], 'Cancelled')), default=STATUSES['NEW'])

    def __str__(self):
        return f'{self.worker}; {self.date_start} {self.date_end})'


class Statistics(AbstractTimeRangeEntity):
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, related_name='statistics')
    hours_worked = models.FloatField()

    class Meta:
        verbose_name_plural = "Statistics"

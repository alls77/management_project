from django.db import models


class AbstractWorker(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)

    class Meta:
        abstract = True


class Company(models.Model):
    name = models.CharField("company's name", max_length=100)

    def __str__(self):
        return f'Company: {self.name} ({self.id})'

    class Meta:
        verbose_name_plural = "Companies"


class Manager(AbstractWorker):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return f'{self.company}; manager:{self.name} ({self.id})'


class Work(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='works')

    def __str__(self):
        return f'{self.company}; work:{self.title} ({self.id})'


class Worker(AbstractWorker):

    def __str__(self):
        return f'{self.name} {self.surname} ({self.id})'


class Workplace(models.Model):
    title = models.CharField(max_length=200)
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name='workplaces')
    worker = models.OneToOneField(Worker, blank=True, null=True, on_delete=models.SET_NULL, related_name='workplace')

    STATUS_NEW = 0
    STATUS_APPROVED = 1
    STATUS_CANCELLED = 2
    STATUS_FINISHED = 3

    status = models.IntegerField(choices=(
        (STATUS_NEW, 'New'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_FINISHED, 'Finished'))
    )

    def __str__(self):
        return f'{self.work}; workplace:{self.title} ({self.id})'


class WorkTime(models.Model):
    STATUS_NEW = 0
    STATUS_APPROVED = 1
    STATUS_CANCELLED = 2

    workplace = models.ForeignKey(Workplace, on_delete=models.PROTECT, related_name='worktimes')
    worker = models.ForeignKey(Worker, on_delete=models.PROTECT, related_name='workers')

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.IntegerField(choices=(
        (STATUS_NEW, 'New'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancelled'))
    )

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


class Workplace(models.Model):
    title = models.CharField(max_length=200)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='workplaces')

    def __str__(self):
        return f'{self.work}; workplace:{self.title} ({self.id})'


class Worker(AbstractWorker):
    workplace = models.OneToOneField(
        Workplace, blank=True, null=True, on_delete=models.SET_NULL, related_name='worker')

    def __str__(self):
        return f'{self.name} ({self.id}); {self.workplace}'

import requests
import datetime

from django.core.mail import send_mail

from .models import Worker, Workplace, Statistics, STATUSES
from management.celery_app import app


@app.task(name='manage_app.tasks.create_workers')
def create_workers(url='https://jsonplaceholder.typicode.com/users'):
    response = requests.get(url)

    if response.status_code == 200:
        workers = response.json()

        for worker in workers:
            worker_full_name = worker['name'].split()

            Worker.objects.get_or_create(
                name=worker_full_name[0],
                surname=worker_full_name[1]
            )


@app.task(name='manage_app.tasks.create_statistics')
def create_statistics(days=7):
    start_date = datetime.date.today() - datetime.timedelta(days=days)

    for workplace in Workplace.objects.filter(status=STATUSES['APPROVED']).prefetch_related('worktimes'):
        worktimes = workplace.worktimes.filter(date_start__gte=start_date)

        hours_worked = datetime.timedelta(days=0)
        for worktime in worktimes:
            hours_worked += worktime.date_end - worktime.date_start

        hours_worked = hours_worked.days * 24 + hours_worked.seconds / 3600

        Statistics.objects.create(
            workplace=workplace,
            date_start=start_date,
            date_end=datetime.date.today(),
            hours_worked=hours_worked
        )

        if hours_worked > workplace.time_limit:
            manager_email = workplace.work.company.managers.order_by('?').first().email
            message = (f"worker: {workplace.worker.name} {workplace.worker.surname} - overtime hours: "
                       f"{hours_worked - workplace.time_limit}")

            send_message.apply_async(args=(manager_email, "Overtime hours", message,))


@app.task(name="manage_app.tasks.send_message")
def send_message(email, subject, message):
    send_mail(subject,
              message,
              recipient_list=[email, ],
              from_email="manage_app@mail.com")

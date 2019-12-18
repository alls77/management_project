from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError

from manage_app.models import Company, Manager, Work, Workplace, WorkTime, Worker


class CompanyModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )

    def test_company(self):
        self.assertEqual(self.company.name, "test company")


class ManagerModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.manager = Manager.objects.create(
            name="john",
            surname="doe",
            company=cls.company
        )

    def test_manager(self):
        self.assertEqual(self.manager.name, "john")
        self.assertEqual(self.manager.surname, "doe")
        self.assertEqual(self.manager.company.id, self.company.id)


class WorkModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.work = Work.objects.create(
            name="test work",
            description="test description",
            company=cls.company
        )

    def test_work(self):
        self.assertEqual(self.work.name, "test work")
        self.assertEqual(self.work.description, "test description")
        self.assertEqual(self.work.company.id, self.company.id)

    def test_work_without_description(self):
        work = Work.objects.create(
            name="test work",
            company=self.company
        )
        self.assertEqual(work.description, None)


class WorkplaceModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.worker = Worker.objects.create(
            name="john",
            surname="doe",
        )
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.work = Work.objects.create(
            name="test work",
            description="test description",
            company=cls.company,
        )
        cls.workplace = Workplace.objects.create(
            name="test workplace",
            work=cls.work,
            worker=cls.worker,
            status=0
        )

    def test_workplace(self):
        self.assertEqual(self.workplace.name, "test workplace")
        self.assertEqual(self.workplace.work, self.work)
        self.assertEqual(self.workplace.worker, self.worker)

    def test_unique_worker_with_workplace(self):
        with self.assertRaises(IntegrityError):
            Workplace.objects.create(
                name="new name",
                work=self.work,
                worker=self.worker,
                status=0
            )


class WorktimeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.worker = Worker.objects.create(
            name="john",
            surname="doe",
        )
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.work = Work.objects.create(
            name="test work",
            description="test description",
            company=cls.company,
        )
        cls.workplace = Workplace.objects.create(
            name="test workplace",
            work=cls.work,
            worker=cls.worker,
            status=0
        )
        cls.worktime = WorkTime.objects.create(
            worker=cls.worker,
            workplace=cls.workplace,
            date_start=datetime.now(),
            date_end=datetime.now(),
        )

    def test_worktime(self):
        self.assertIsNotNone(self.worktime.id)

    def test_worktime_default_status(self):
        self.assertEqual(self.worktime.status, 0)

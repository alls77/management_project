from django.test import TestCase
from django.urls import reverse

from manage_app.models import Company, Manager, Work, Workplace, WorkTime, Worker


class IndexViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse('index')

    def test_index_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_app/index.html')


class CompaniesViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.url = reverse('companies')

    def test_companies_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["companies"])
        self.assertEqual(response.context["companies"].last(), self.company)


class CompanyDetailsViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.url = reverse('detail', kwargs={'pk': cls.company.pk})

    def test_company_details_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["company"])

    def test_company_details_view_negative(self):
        response = self.client.get(reverse('detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)


class CompanyManagersViewTest(TestCase):
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
        cls.url = reverse('managers', kwargs={'pk': cls.company.pk})

    def test_company_managers_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["managers"])


class CreateWorkViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = Company.objects.create(
            name="test company",
        )
        cls.url = reverse('create_work', kwargs={'pk': cls.company.pk})

    def test_create_work(self):
        work = {
            'company': self.company.id,
            'name': 'test name',
            'description': 'test description'
        }
        response = self.client.post(self.url, work)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.company.works.last().name, work['name'])
        self.assertEqual(self.company.works.last().description, work['description'])

    def test_create_work_without_data(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', u'This field is required.')

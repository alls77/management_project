import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from management.celery_app import app
from .forms import WorkCreateForm, WorkTimeCreateForm, WorkplaceCreateForm
from .models import STATUSES
from .permissions import IsReviewer
from .serializers import *

sentry_logger = logging.getLogger('sentry_logger')


class IndexView(TemplateView):
    template_name = 'manage_app/index.html'


class CompaniesView(LoginRequiredMixin, ListView):
    template_name = 'manage_app/companies.html'
    model = Company
    context_object_name = 'companies'


class CompanyDetailsView(UserPassesTestMixin, DetailView):
    template_name = 'manage_app/company_detail.html'
    context_object_name = 'company'

    def test_func(self):
        return self.request.user.groups.filter(name='Reviewers').exists()

    def get_queryset(self):
        return Company.objects.prefetch_related('works__workplaces__worker')


class CreateWorkView(CreateView):
    template_name = 'manage_app/create_work.html'
    form_class = WorkCreateForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        company = get_object_or_404(Company, id=self.kwargs['pk'])
        return {'company': company}

    def form_valid(self, form):
        self.object = form.save()
        sentry_logger.info("new work created", extra={'work_name': self.request.POST['name']})
        return super().form_valid(form)


class CompanyManagersView(ListView):
    template_name = 'manage_app/company_managers.html'
    context_object_name = 'managers'

    def get_queryset(self):
        return Manager.objects.filter(company__id=self.kwargs['pk'])


class WorkersView(ListView):
    template_name = 'manage_app/workers.html'
    model = Worker
    context_object_name = 'workers'


class CreateWorkersView(View):
    def get(self, request):
        app.send_task('manage_app.tasks.create_workers')
        return redirect(reverse_lazy('workers'), )


class CreateWorkTimeView(CreateView):
    template_name = 'manage_app/create_worktime.html'
    form_class = WorkTimeCreateForm

    def get_success_url(self):
        return reverse_lazy('worker_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.worker = get_object_or_404(Worker, id=self.kwargs['pk'])
        self.object.workplace = get_object_or_404(Workplace, id=self.kwargs['work_id'])
        sentry_logger.info("new worktime created")
        return super().form_valid(form)


class WorkersDetailsView(DetailView):
    template_name = 'manage_app/worker_detail.html'
    context_object_name = 'worker'

    def get_queryset(self):
        return Worker.objects.prefetch_related('workplaces__worktimes')


class CreateWorkplaceView(CreateView):
    template_name = 'manage_app/create_workplace.html'
    form_class = WorkplaceCreateForm

    def get_success_url(self):
        return reverse_lazy('companies')

    def get_initial(self):
        work = get_object_or_404(Work, id=self.kwargs['work_id'])
        return {'work': work}

    def form_valid(self, form):
        self.object = form.save()
        sentry_logger.info("workplace created", extra={'workplace_name': self.request.POST['name']})
        return super().form_valid(form)


class UpdateWorkplaceView(UpdateView):
    model = Workplace
    fields = ['worker']
    template_name = 'manage_app/update_workplace.html'

    def get_success_url(self):
        return reverse_lazy('companies')

    def form_valid(self, form):
        if self.request.POST['worker']:
            self.object = form.save(commit=False)
            self.object.status = STATUSES['NEW']
            sentry_logger.info("workplace updated")
            return super().form_valid(form)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanySerializer
        return CompanyDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.IsAuthenticated, IsReviewer,)
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def managers(self, request):
        company = self.get_object()
        managers = Manager.objects.filter(company=company)
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkerSerializer
        return WorkerDetailSerializer


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkSerializer
        return WorkDetailSerializer


class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkplaceSerializer
        return WorkplaceDetailSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

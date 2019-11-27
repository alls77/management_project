from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Company, Manager, Work, Worker, Workplace


def index(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'manage_app/index.html', context)


def detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    context = {'company': company}
    return render(request, 'manage_app/detail.html', context)

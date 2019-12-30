from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('companies/', views.CompaniesView.as_view(), name='companies'),
    path('companies/<int:pk>/', views.CompanyDetailsView.as_view(), name='detail'),
    path('companies/<int:pk>/managers/', views.CompanyManagersView.as_view(), name='managers'),
    path('companies/<int:pk>/create_work/', views.CreateWorkView.as_view(), name='create_work'),

    path('workplace/<int:pk>/appointment/', views.UpdateWorkplaceView.as_view(), name='worker_appointment'),
    path('works/<int:work_id>/create_workplace/', views.CreateWorkplaceView.as_view(), name='create_workplace'),

    path('workers/', views.WorkersView.as_view(), name='workers'),
    path('workers/create_workers/', views.CreateWorkersView.as_view(), name='create_workers'),
    path('workers/<int:pk>/', views.WorkersDetailsView.as_view(), name='worker_detail'),
    path('workers/<int:pk>/works/<int:work_id>/', views.CreateWorkTimeView.as_view(), name='create_worktime'),
]

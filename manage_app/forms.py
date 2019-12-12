from django import forms

from .models import Work, WorkTime, Workplace


class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('name', 'description', 'company')


class WorkplaceCreateForm(forms.ModelForm):
    class Meta:
        model = Workplace
        fields = ('name', 'work')


class WorkTimeCreateForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = ('date_start', 'date_end')

        widgets = {
            'date_start': forms.DateTimeInput(attrs={'placeholder': '2019-01-30 10:20'}),
            'date_end': forms.DateTimeInput(attrs={'placeholder': '2019-01-30 10:20'})
        }

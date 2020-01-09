from rest_framework import serializers

from .models import Company, Manager, Work, Worker, Workplace


class ManagerSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Manager
        fields = ('id', 'name', 'surname', 'email', 'company')


class WorkplaceSerializer(serializers.ModelSerializer):
    work = serializers.ReadOnlyField(source='work.name')

    class Meta:
        model = Workplace
        fields = ('id', 'name', 'work')


class WorkplaceDetailSerializer(serializers.ModelSerializer):
    work = serializers.ReadOnlyField(source='work.name')
    worker = serializers.HyperlinkedRelatedField(read_only=True, view_name='worker-detail')

    class Meta:
        model = Workplace
        fields = ('id', 'name', 'work', 'worker', 'status')


class WorkSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Work
        fields = ('id', 'name', 'company', 'description')


class WorkDetailSerializer(serializers.ModelSerializer):
    workplaces = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='workplace-detail')
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Work
        fields = ('id', 'name', 'company', 'description', 'workplaces')


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'surname')


class WorkerDetailSerializer(serializers.ModelSerializer):
    workplaces = serializers.StringRelatedField(many=True)

    class Meta:
        model = Worker
        fields = ('id', 'name', 'surname', 'birth_date', 'workplaces')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class CompanyDetailSerializer(serializers.ModelSerializer):
    works = WorkSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'works')

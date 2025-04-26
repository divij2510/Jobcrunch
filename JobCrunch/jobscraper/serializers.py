# jobscraper/serializers.py
from rest_framework import serializers
from .models import Company, Job

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'website']

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'company_name', 'location', 
            'description', 'apply_link', 'source', 'date_posted', 
            'date_scraped','salary'
        ]

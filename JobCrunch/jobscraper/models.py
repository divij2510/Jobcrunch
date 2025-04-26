from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=50, blank = True, null=True)
    apply_link = models.URLField()
    source = models.CharField(max_length=100)  
    date_posted = models.DateTimeField(null=True, blank=True)
    date_scraped = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('title', 'company', 'location')  
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location']),
            models.Index(fields=['date_posted']),
        ]
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f"{self.title} at {self.company.name}"

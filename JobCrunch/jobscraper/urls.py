from django.urls import path
from . import views

urlpatterns = [
    path("scrape-timesjobs/", views.scrape_timesjobs, name="scrape_timesjobs"),
    path("scrape-wellfound/", views.scrape_wellfound, name="scrape_wellfound"),
    path("all-jobs/", views.get_all_jobs, name="get_all_jobs"),
    path("all-companies/", views.get_all_companies, name="get_all_companies"),
    path("delete-jobs/", views.delete_jobs_before, name="delete_jobs_before"),
]

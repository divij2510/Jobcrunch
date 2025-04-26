from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json

from .models import Job, Company
from .scrapers.times_jobs_scraper import TimesJobsScraper
from .scrapers.wellfound_scraper import WellfoundScraper

def is_api_request(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("api") == "1"

def index(request):
    return render(request, "jobscraper/index.html")


@require_http_methods(["POST", "GET"])
@csrf_exempt
def scrape_timesjobs(request):
    scraper = TimesJobsScraper()
    # before = Job.objects.count()
    jobs = scraper.scrape()
    # after = Job.objects.count()
    message = f"{len(jobs)} jobs scraped from TimesJobs."

    if is_api_request(request):
        return JsonResponse({"message": message})

    return render(request, "jobscraper/index.html", {"message": message})


@require_http_methods(["POST", "GET"])
@csrf_exempt
def scrape_wellfound(request):
    start_page = int(request.POST.get("start_page") or request.GET.get("start_page", 1))
    end_page = int(request.POST.get("end_page") or request.GET.get("end_page", 5))

    scraper = WellfoundScraper()
    # before = Job.objects.count()
    jobs = scraper.scrape(start_page=start_page, end_page=end_page)
    # after = Job.objects.count()
    message = f"{len(jobs)} jobs scraped from Wellfound."

    if is_api_request(request):
        return JsonResponse({"message": message})

    return render(request, "jobscraper/index.html", {"message": message})


@require_http_methods(["GET"])
def get_all_jobs(request):
    jobs = Job.objects.select_related("company").all()
    if is_api_request(request):
        job_list = [
            {
                "title": job.title,
                "company": job.company.name,
                "location": job.location,
                "salary": job.salary,
                "description": job.description,
                "apply_link": job.apply_link,
                "source": job.source,
                "date_scraped": job.date_scraped
            } for job in jobs
        ]
        return JsonResponse(job_list, safe=False)

    return render(request, "jobscraper/all_jobs.html", {"jobs": jobs})


@require_http_methods(["GET"])
def get_all_companies(request):
    companies = Company.objects.all()
    if is_api_request(request):
        company_list = [{"name": comp.name, "website": comp.website} for comp in companies]
        return JsonResponse(company_list, safe=False)

    return render(request, "jobscraper/all_companies.html", {"companies": companies})


@require_http_methods(["POST", "GET"])
@csrf_exempt
def delete_jobs_before(request):
    if request.method == "GET":
        return render(request, "jobscraper/delete_jobs.html")

    try:
        data = request.POST or json.loads(request.body)
        date_str = data.get("before_date")
        delete_before = datetime.strptime(date_str, f"%Y-%m-%d")
    except:
        error = "Invalid or missing 'before_date'. Format should be YYYY-MM-DD."
        if is_api_request(request):
            return JsonResponse({"error": error}, status=400)
        return render(request, "jobscraper/delete_jobs.html", {"error": error})

    deleted_count, _ = Job.objects.filter(date_scraped__lt=delete_before).delete()
    message = f"{deleted_count} jobs deleted."

    if is_api_request(request):
        return JsonResponse({"message": message})

    return render(request, "jobscraper/delete_jobs.html", {"message": message})

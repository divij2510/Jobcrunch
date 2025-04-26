# Tech Choices
- Django (with sqlite3)
- Beautiful Soup 4, requests
- Selenium

*Django* is the most versatile framework that can work with python scripts of all sorts, so its perfect to use for a scraping heavy Rest API. 

I also used *Django template engine* to dynamically generate HTML and CSS styling for basic dashboard that was directly connected to my internal views.py. 
This is better according to me and is a better choice to use rather than react.js which would put a massive overhead and seperate deployment. For a simple dashboard and management ui normal HTML, CSS templates work best.

The app is fully functional using Django templates that trigger scrape-jobs and get requests to query the database.

# Documentation

## 1. scrape timesjobs

scrape jobs from timesjobs and save

**POST**  
`/api/scrape-timesjobs/`

**GET**  
`/api/scrape-timesjobs/`

### example request
```
GET /api/scrape-timesjobs/
```

### response
```json
{
  "message": "50 jobs scraped from TimesJobs."
}
```

---

## 2. scrape wellfound

scrape jobs from wellfound with pages

**POST**  
`/api/scrape-wellfound/`

**GET**  
`/api/scrape-wellfound/`

### query or form params
- start_page (optional) default 1  
- end_page (optional) default 5

### example request
```
GET /api/scrape-wellfound/?start_page=2&end_page=4
```

### response
```json
{
  "message": "120 jobs scraped from Wellfound."
}
```

---

## 3. get all jobs

get all jobs in system

**GET**  
`/api/all-jobs/`

### example request
```
GET /api/all-jobs/
```

### response
```json
[
  {
    "title": "Backend Dev",
    "company": "TechCorp",
    "location": "Bangalore",
    "salary": "12 LPA",
    "description": "REST API dev",
    "apply_link": "https://example.com/job1",
    "source": "TimesJobs",
    "date_scraped": "2025-04-21"
  }
]
```

---

## 4. get all companies

get all companies saved

**GET**  
`/api/all-companies/`

### example request
```
GET /api/all-companies/
```

### response
```json
[
  {
    "name": "TechCorp",
    "website": "https://techcorp.com"
  }
]
```

---

## 5. delete jobs before date

delete jobs scraped before date

**POST**  
`/api/delete-jobs/`

**GET**  
`/api/delete-jobs/`

### form or json body
```json
{
  "before_date": "2025-04-01"
}
```

### response
```json
{
  "message": "30 jobs deleted."
}
```

### error response
```json
{
  "error": "Invalid or missing 'before_date'. Format should be YYYY-MM-DD."
}
```

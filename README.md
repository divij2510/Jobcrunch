
# JobCrunch

Its a Backend API and direct-use hybrid web-scraping tool for online job listings for startups in India. It scrapes using selenium and beautiful soup 4 and users can create, update and delete their scraped databases and also apply to IT jobs!

## Images

### Run Scrape jobs:
![Scraper demo](images/Screenshot%202025-04-22%20002801.png)

### Manage database:
![Scraper crud](images/Screenshot%202025-04-22%20002857.png)

### Delete outdated job listings:
![Scraper crud](images/Screenshot%202025-04-22%20002925.png)

## Documentation
View Documentation [HERE](https://github.com/divij2510/Jobcrunch/blob/main/submission.md)


## Requirements

To run this project, you will need to install the following python packages in your machine.

```text
asgiref -- 3.7.2
certifi -- 2024.2.2
charset-normalizer -- 3.3.2
cffi -- 1.16.0
cryptography -- 42.0.5
Django -- 5.0.3
idna -- 3.6
pillow -- 10.2.0
pycparser -- 2.21
pytz -- 2024.1
requests -- 2.31.0
selenium -- 4.19.0
soupsieve -- 2.5
sqlparse -- 0.4.4
tzdata -- 2024.1
urllib3 -- 2.2.1
webdriver-manager -- 4.0.1
beautifulsoup4 -- 4.12.3
```



## Install and Run

Make sure to have python installed in your system, If required you can make a virtual environment for dependencies.

```bash
  git clone https://github.com/divij2510/Jobcrunch.git
```  
  After cloning, move into the directory having the project files using the change directory command
```bash
  cd Jobcrunch
```
  Create a virtual environment where all the required python packages will be installed
```
python -m venv env
```
  Activate the virtual environment
```
.\env\Scripts\activate
```
  Install all the project Requirements
```
pip install -r requirements.txt
```
  Apply migrations and create your superuser (follow the prompts)
```
python manage.py migrate
python manage.py createsuperuser
```
Run the development server with:
```
python manage.py runserver
```



  

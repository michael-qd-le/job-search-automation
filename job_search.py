import requests

TARGET_ROLES = [
    "CRM specialist",
    "Automation specialist",
    "Marketing Automation Operations",
    "Martech",
    "Revenue Operations",
    "Back office specialist",
    "Back office analyst",
    "Business Operations",
    "Research Operations",
    "Strategy & Ops",
    "Go-to-Market Operations",
    "Process Implementation",
    "Digital Transformation",
    "Business Process Analyst",
    "AI enablement",
    "Data Analyst",
    "Marketing Analyst",
    "Customer Analyst",
    "Product Analyst",
    "Business Analyst",
    "Fraud Analyst",
    "CRM analyst",
    "Automation Analyst",
    "Digitalization and Process Analyst",
    "AI analyst",
    "Project Manager",
]

def search_jobs(keyword, limit=10):
    url = "https://jobsearch.api.jobtechdev.se/search"
    params = {"q": keyword, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    return data["hits"]


if __name__ == "__main__":
    seen_ids = set()
    for role in TARGET_ROLES:
        jobs = search_jobs(role, limit=5)
        for job in jobs:
            if job["id"] in seen_ids:
                continue
            seen_ids.add(job["id"])
            headline = job["headline"]
            employer = job["employer"]["name"]
            location = job["workplace_address"]["municipality"]
            employment_type = job["employment_type"]["label"]
            must_have_languages = job["must_have"]["languages"]
            nice_to_have_languages = job["nice_to_have"]["languages"]
            deadline = job["application_deadline"]
            url = job["webpage_url"]
            print(headline, employer, location, employment_type, must_have_languages, nice_to_have_languages, deadline, url)






    
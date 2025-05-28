import requests
from bs4 import BeautifulSoup

def scrape_indeed(query="data analyst", location="France", max_pages=1):
    headers = {'User-Agent': 'Mozilla/5.0'}
    jobs = []
    for page in range(max_pages):
        start = page * 10
        url = f"https://fr.indeed.com/jobs?q={query}&l={location}&start={start}"
        print(f"[DEBUG] Scraping Indeed page {page+1}: {url}")
        r = requests.get(url, headers=headers)
        print(f"[DEBUG] Status code: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')

        for job in soup.select('a.tapItem'):
            title = job.select_one('.jobTitle').get_text(strip=True)
            company = job.select_one('.companyName')
            company = company.get_text(strip=True) if company else ""
            description = job.select_one('.job-snippet').get_text(strip=True)
            print(f"[DEBUG] Found job: {title} at {company}")
            jobs.append({
                'title': title,
                'company': company,
                'description': description,
                'source': 'Indeed'
            })
    print(f"[DEBUG] Total Indeed jobs scraped: {len(jobs)}")
    return jobs

def scrape_wttj(query="data analyst", max_pages=1):
    jobs = []
    for page in range(1, max_pages + 1):
        url = f"https://www.welcometothejungle.com/fr/jobs?query={query}&page={page}"
        print(f"[DEBUG] Scraping WTTJ page {page}: {url}")
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        print(f"[DEBUG] Status code: {r.status_code}")
        if r.status_code != 200:
            print(f"[DEBUG] Skipping page {page} due to bad status code.")
            continue
        data = r.text
        jobs.append({
            "title": f"Offre {page} - {query}",
            "company": "WTTJ",
            "description": data[:500],  # pour démo (HTML brut sinon)
            "source": "WTTJ"
        })
        print(f"[DEBUG] Added WTTJ job for page {page}")
    print(f"[DEBUG] Total WTTJ jobs scraped: {len(jobs)}")
    return jobs
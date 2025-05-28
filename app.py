import pandas as pd
from scraping import scrape_indeed, scrape_wttj
from extract_cv_text import extract_text_from_pdf
from match_tfidf import compute_similarity

cv_text = extract_text_from_pdf("cv.pdf")
print("✅ CV extrait avec succès.")
print(f"[DEBUG] CV Text Length: {len(cv_text)} characters")
print(f"[DEBUG] CV Text Sample: {cv_text[:100]}...")  # Affiche un extrait du CV pour vérification
# Scraping des offres d'emploi
jobs_indeed = scrape_indeed(query="data analyst", max_pages=1)
jobs_wttj = scrape_wttj(query="data analyst", max_pages=1)
# Affichage des offres d'emploi récupérées
print(f"✅ {len(jobs_indeed)} offres d'emploi récupérées depuis Indeed.")
print(f"✅ {len(jobs_wttj)} offres d'emploi récupérées depuis WTTJ.")
# Combinaison des offres d'emploi et calcul de la similarité
all_jobs = jobs_indeed + jobs_wttj
matched_jobs = compute_similarity(cv_text, all_jobs)

df = pd.DataFrame(matched_jobs)
df.to_csv("resultats_matching.csv", index=False)

print("✅ Matching terminé. Résultats enregistrés dans 'resultats_matching.csv'")

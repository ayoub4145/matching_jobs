from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(cv_text, job_descriptions):
    # On crée une liste (corpus) contenant le texte du CV suivi des descriptions de chaque offre d'emploi.
    corpus = [cv_text] + [job["description"] for job in job_descriptions]
    
    # On initialise le vectoriseur TF-IDF en supprimant les mots anglais courants (stop words).
    tfidf = TfidfVectorizer(stop_words='english')
    
    # On transforme le corpus en une matrice TF-IDF (chaque ligne = un texte, chaque colonne = un mot).
    tfidf_matrix = tfidf.fit_transform(corpus)

    # On calcule la similarité cosinus entre le CV (première ligne) et chaque description d'offre (lignes suivantes).
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    # Pour chaque offre et son score de similarité associé :
    for job, score in zip(job_descriptions, scores):
        # On ajoute le score (arrondi à 3 décimales) au dictionnaire de l'offre.
        job["score"] = round(float(score), 3)
        results.append(job)
    
    # On retourne la liste des offres triées par score décroissant (meilleure correspondance en premier).
    return sorted(results, key=lambda x: x["score"], reverse=True)
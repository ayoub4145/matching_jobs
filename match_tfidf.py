from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(cv_text, job_descriptions):
    corpus = [cv_text] + [job["description"] for job in job_descriptions]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(corpus)

    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    for job, score in zip(job_descriptions, scores):
        job["score"] = round(float(score), 3)
        results.append(job)
    return sorted(results, key=lambda x: x["score"], reverse=True)

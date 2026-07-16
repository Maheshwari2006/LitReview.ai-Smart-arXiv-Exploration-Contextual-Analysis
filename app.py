import os
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --------------------------------------------------
# PAPERS FETCHERS (With Year Interval Filter)
# --------------------------------------------------

def fetch_arxiv_papers(query, start_year, end_year, max_results=20):
    cleaned_query = query.replace(" ", "+")
    # Formulate proper query constraint matrix across dates
    date_query = f"submittedDate:[{start_year}01010000+TO+{end_year}12312359]"
    url = f"http://export.arxiv.org/api/query?search_query=all:{cleaned_query}+AND+{date_query}&start=0&max_results={max_results}"
    
    try:
        response = requests.get(url, timeout=25)
        if response.status_code != 200: return []
        root = ET.fromstring(response.content)
        papers = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            papers.append({
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip().replace("\n", " "),
                "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip().replace("\n", " "),
                "link": entry.find("{http://www.w3.org/2005/Atom}id").text.strip(),
                "source": "arXiv"
            })
        return papers
    except Exception:
        return []

def fetch_ieee_papers(query, start_year, end_year, max_results=20):
    # Public Fallback Endpoint Layer Placeholder
    return []

def rank_papers(query, papers):
    if not papers: return []
    docs = [query] + [p["summary"] for p in papers]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(docs)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    
    for i, paper in enumerate(papers):
        paper["score"] = round(float(scores[i]), 3)
        
    # Sort by descending order score relevance matrix
    papers.sort(key=lambda x: x["score"], reverse=True)
    return papers

# --------------------------------------------------
# FLASK ROUTING LAYERS
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    papers = []
    query = ""
    max_results = 10  
    start_year = 2020
    end_year = 2026

    if request.method == "POST":
        query = request.form.get("query", "")
        max_results = max(int(request.form.get("max_results", 20)), 20)  
        start_year = int(request.form.get("start_year", 2020))
        end_year = int(request.form.get("end_year", 2026))

        if query:
            # Query full threshold directly from active index to bypass data limits
            all_papers = fetch_arxiv_papers(query, start_year, end_year, max_results)
            
            # IEEE fallback integration loop allocation if implemented later
            # ieee_list = fetch_ieee_papers(query, start_year, end_year, max_results)
            # all_papers += ieee_list
            
            # Process ranking and apply final strict slice constraint down to UI selection
            ranked = rank_papers(query, all_papers)
            papers = ranked[:max_results]

    return render_template(
        "index.html",
        papers=papers,
        query=query,
        max_results=max_results,
        start_year=start_year,
        end_year=end_year
    )

if __name__ == "__main__":
    app.run(debug=True)
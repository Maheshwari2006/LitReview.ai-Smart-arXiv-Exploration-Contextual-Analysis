import xml.etree.ElementTree as ET
import urllib.parse
from flask import Flask, render_template, request, session
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
# Secure key for session management (prevents the 10-minute reset)
app.secret_key = 'litreview_secret_session_key_2026'

def get_arxiv_papers(query, start_year, end_year):
    """Fetches papers from arXiv API and filters them by publication year."""
    # Format query for arXiv API
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results=30"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
    except Exception:
        return []

    # Parse XML response
    root = ET.fromstring(response.content)
    # XML namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }

    raw_papers = []
    
    for entry in root.findall('atom:entry', namespaces):
        title = entry.find('atom:title', namespaces).text.strip().replace('\n', ' ')
        
        # Extract authors
        authors_list = [author.find('atom:name', namespaces).text for author in entry.findall('atom:author', namespaces)]
        authors_str = ", ".join(authors_list)
        
        # Extract abstract (summary) for TF-IDF calculations
        summary = entry.find('atom:summary', namespaces).text.strip().replace('\n', ' ')
        
        # Extract published year
        published_date = entry.find('atom:published', namespaces).text
        year = published_date[:4] # Extract "YYYY"
        
        # Filter strictly by user-selected year range
        if not (start_year <= year <= end_year):
            continue
            
        # Get Links
        abs_link = ""
        pdf_link = ""
        for link in entry.findall('atom:link', namespaces):
            rel = link.attrib.get('rel')
            title_attr = link.attrib.get('title')
            href = link.attrib.get('href')
            
            if rel == 'alternate':
                abs_link = href
            elif rel == 'related' and title_attr == 'pdf':
                pdf_link = href
            elif href.endswith('.pdf'):
                pdf_link = href

        # Fallback if no specific PDF link found
        if not pdf_link and abs_link:
            pdf_link = abs_link.replace('/abs/', '/pdf/') + ".pdf"

        raw_papers.append({
            'title': title,
            'authors': authors_str,
            'abstract': summary,  # Needed for TF-IDF, hidden on UI
            'year': year,
            'link': abs_link,
            'pdf_link': pdf_link
        })
        
    return raw_papers

def rank_papers(query, papers):
    """Ranks matching papers using TF-IDF and Cosine Similarity."""
    if not papers:
        return []
        
    # Gather abstracts to construct the corpus
    corpus = [paper['abstract'] for paper in papers]
    
    # Run Scikit-Learn TF-IDF vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vector = vectorizer.transform([query])
        
        # Compute Cosine Similarity
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Attach scores to the papers
        for idx, paper in enumerate(papers):
            paper['similarity_score'] = float(similarity_scores[idx])
            
        # Sort papers by descending relevance score
        ranked = sorted(papers, key=lambda x: x['similarity_score'], reverse=True)
        return ranked
    except Exception:
        # Fallback ranking if vectorization fails
        for paper in papers:
            paper['similarity_score'] = 0.0
        return papers

@app.route('/', methods=['GET', 'POST'])
def index():
    query = None
    start_year = "2020"
    end_year = "2026"
    papers = None

    # Scenario A: New search requested
    if request.method == 'POST':
        query = request.form.get('query')
        start_year = request.form.get('start_year', '2020')
        end_year = request.form.get('end_year', '2026')
        
        # Save to browser session
        session['last_query'] = query
        session['last_start'] = start_year
        session['last_end'] = end_year

    # Scenario B: Session restore (avoids 10-minute timeout resets!)
    elif 'last_query' in session:
        query = session['last_query']
        start_year = session['last_start']
        end_year = session['last_end']

    # Execute active search logic
    if query:
        raw_results = get_arxiv_papers(query, start_year, end_year)
        papers = rank_papers(query, raw_results)
        return render_template('index.html', papers=papers, query=query, start_year=start_year, end_year=end_year)

    # Scenario C: Default welcome screen
    return render_template('index.html', papers=None)

if __name__ == '__main__':
    app.run(debug=True)
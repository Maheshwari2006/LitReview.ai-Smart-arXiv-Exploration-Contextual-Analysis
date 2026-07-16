# LitReview.ai-Smart-arXiv-Exploration-Contextual-Analysis

📚 LitReview.ai — Smart arXiv Exploration & Contextual Analysis : 
A Flask-based academic research portal that enables users to search, filter, and rank research papers from arXiv. The application uses TF-IDF Vectorization and Cosine Similarity to rank papers based on their relevance to a user's search query, providing a simple and efficient literature exploration experience.

🚀 Features : 
🔍 Search research papers by keyword
📅 Filter papers by publication year range
📄 Retrieve papers directly from the arXiv API
🎯 Rank papers using TF-IDF and Cosine Similarity
📖 View paper abstracts
📥 Open the original arXiv abstract page
📑 Download research papers in PDF format
🎨 Responsive and clean Bootstrap-based interface

🛠️ Tech Stack -

Backend :
Python
Flask
Requests
XML (ElementTree)
Scikit-learn
Frontend
HTML5
CSS3
Bootstrap 5
Jinja2
Data Source
arXiv API


📂 Project Structure
LitReview.ai/
│
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md

⚙️ Installation
1. Clone the repository
git clone https://github.com/Maheshwari2006/LitReview.ai-Smart-arXiv-Exploration-Contextual-Analysis.git
2. Navigate to the project folder
cd LitReview.ai-Smart-arXiv-Exploration-Contextual-Analysis
3. Create a virtual environment (Optional)
Windows

python -m venv venv
venv\Scripts\activate
Linux / macOS

python3 -m venv venv
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
Or install manually:

pip install flask requests scikit-learn
5. Run the application
python app.py
6. Open your browser
http://127.0.0.1:5000

🔄 Workflow
Enter a research topic or keyword.
Select the publication year range.
Choose the number of papers to retrieve.
The application fetches matching papers from the arXiv API.
Paper abstracts are converted into TF-IDF vectors.
Cosine Similarity calculates the relevance score.
Papers are ranked by relevance and displayed to the user.

📖 Output Includes
Each search result displays:

Research Paper Title
Abstract
Relevance Score
Source
Abstract Link
Direct PDF Download Link

📷 User Interface
The application provides:

Google-inspired search interface
Research topic search
Year range selection
Paper extraction limit slider
Ranked paper cards
Responsive Bootstrap layout

🔮 Future Improvements
IEEE Xplore integration
Semantic Scholar integration
AI-generated paper summaries
Citation generation (APA, IEEE, MLA)
Export search results
Bookmark papers
Semantic search using embeddings
Research trend visualization

👨‍💻 Author
Maheshwari Rewatkar

Demo link : https://litreview-ai-smart-arxiv-exploration.onrender.com/

GitHub: https://github.com/Maheshwari2006
📄 License
This project is licensed under the MIT License.
⭐ If you found this project useful, please consider giving it a Star on GitHub.    is thisi correct 

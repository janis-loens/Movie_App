# 🎬 Movie App – Janis' Filme-Abend

A Python-based movie manager that lets you add, search, update, delete, and view your favorite films using the OMDb API. Data is stored in an SQLite database and visually presented with a clean HTML layout.

## 🚀 Features

- 🔎 Search movies using OMDb API
- 📥 Add movies with title, year, rating, and poster
- ✏️ Update existing movie ratings
- ❌ Delete movies
- 🌐 Generate a movie overview in HTML format

## 🧱 Tech Stack

- Python 3.10+
- SQLite
- SQLAlchemy
- Requests
- OMDb API
- HTML + CSS

## 📦 Installation

```bash
git clone https://github.com/yourusername/movie-app.git
cd movie-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔐 Set Up API Key

Register at [OMDb API](http://www.omdbapi.com/apikey.aspx) and set your API key as an environment variable:

```bash
export API_KEY=your_api_key  # or use a .env file
```

## ▶️ Usage

```bash
python movies.py
```

Follow the prompt to add, list, search, update, or delete movies.

## 📁 Project Structure

```
movie-app/
│
├── website/
│   ├── index_template.html
│   └── style.css
│
├── movies.py
├── movie_storage_sql.py
├── API_communication.py
├── requirements.txt
└── README.md
```

## 📄 License

MIT License.

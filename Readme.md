🎬 Movie Ratings Dashboard

A Streamlit web app to explore movies and check ratings from TMDb, IMDb, and Rotten Tomatoes.
Search by title or browse categories like Popular, Top Rated, and Now Playing.

🚀 Features

🔍 Search movies by title

🎞 Browse TMDb categories (popular, top rated, now playing)

⭐ Compare ratings from TMDb, IMDb, and Rotten Tomatoes

📝 Movie overview & release year

🌐 Links to official websites & TMDb pages

🛠 Tech Stack

Python

Streamlit

TMDb API

OMDb API

⚡ Setup & Installation
1️⃣ Clone the repo
git clone https://github.com/0mGosavi/movie-ratings-app.git
cd movie-ratings-app

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Configure API Keys

Create a .env file in the project root:

TMDB_KEY=your_tmdb_key_here
OMDB_KEY=your_omdb_key_here


(See .env.example for reference — do NOT push your real .env to GitHub.)

4️⃣ Run the app locally
streamlit run app.py

🌍 Deploy on Streamlit Cloud

Push your repo to GitHub

Go to share.streamlit.io

Connect your repo and select app.py

Add your API keys in Secrets Manager:

Go to Settings → Secrets

Paste this:

TMDB_KEY="your_tmdb_key_here"
OMDB_KEY="your_omdb_key_here"


🚀 Done! Your app will get a public link to share.

📂 Project Structure
movie-ratings-app/
│── app.py              # Main Streamlit app
│── requirements.txt    # Dependencies
│── .env.example        # Example env file (safe to push)
│── .gitignore          # Ignore .env, cache files, etc.
│── README.md           # Project documentation

🙌 Credits

TMDb for movie data

OMDb for IMDb & Rotten Tomatoes ratings

Built with ❤️ using Streamlit
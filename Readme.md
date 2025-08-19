# 🎬 Movie Ratings Dashboard

A **Streamlit web application** to explore movies and check ratings from **TMDb, IMDb, and Rotten Tomatoes**.  
Search by title or browse curated categories like **Popular, Top Rated, and Now Playing**.

---

## 🚀 Features
- 🔍 Search movies by title  
- 🎞 Browse TMDb categories (Popular, Top Rated, Now Playing)  
- ⭐ Compare ratings from TMDb, IMDb, and Rotten Tomatoes  
- 📝 View movie overview & release year  
- 🌐 Access official websites & TMDb pages  

---

## 🛠 Tech Stack
- Python  
- Streamlit  
- TMDb API  
- OMDb API  

---

## ⚡ Setup & Installation

### 1️⃣ Clone the repository

git clone https://github.com/0mGosavi/movie-ratings-app.git
cd movie-ratings-app

### 2️⃣ Install dependencies

pip install -r requirements.txt

### 3️⃣ Configure API Keys
Create a .env file in the project root:

&nbsp;&nbsp;&nbsp;TMDB_KEY=your_tmdb_key_here  
&nbsp;&nbsp;&nbsp;OMDB_KEY=your_omdb_key_here    

(See .env.example for reference — do NOT push your real .env to GitHub.)

### 4️⃣ Run the app locally

streamlit run app.py

---

## 🌍 Deployment (Streamlit Cloud)

1. Push your repo to GitHub
2. Go to Streamlit Cloud
3. Connect your repo and select app.py
4. Add your API keys in Secrets Manager → Settings → Secrets
5. Paste:



   

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TMDB_KEY="your_tmdb_key_here"  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;OMDB_KEY="your_omdb_key_here"  

  6. ✅ Done! Your app will be live with a public shareable link

---

## 📂 Project Structure

movie-ratings-app/
- app.py           # Main Streamlit app
- requirements.txt # Dependencies
- .env.example     # Example env file (safe to push)
- .gitignore       # Ignore .env, cache files, etc.
- README.md        # Project documentation



---

## 🙌 Credits

TMDb for movie data.  
OMDb for IMDb & Rotten Tomatoes ratings.  
Built with ❤️ using Streamlit.



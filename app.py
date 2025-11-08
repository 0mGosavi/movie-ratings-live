import os
import requests
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt

# ---------------- ENV & KEYS ---------------- #
load_dotenv()
TMDB_KEY = os.getenv("TMDB_KEY")
OMDB_KEY = os.getenv("OMDB_KEY")

# ---------------- DATABASE ---------------- #
Base = declarative_base()
engine = create_engine("sqlite:///movies.db")  # SQLite DB file
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

class User(Base):
    __tablename__ = "users"
    print("Creating users table HELO")
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)  # hashed password
    watchlist = relationship("Watchlist", back_populates="user")

class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True)
    movie_title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="watchlist")

Base.metadata.create_all(engine)

# ---------------- AUTH HELPERS ---------------- #
def create_user(username, email, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, email=email, password=hashed_pw)
    db.add(user)
    db.commit()

def authenticate_user(username, password):
    user = db.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    return None

def add_to_watchlist(user_id, movie_title):
    if not db.query(Watchlist).filter_by(user_id=user_id, movie_title=movie_title).first():
        entry = Watchlist(movie_title=movie_title, user_id=user_id)
        db.add(entry)
        db.commit()

def get_watchlist(user_id):
    return [w.movie_title for w in db.query(Watchlist).filter_by(user_id=user_id).all()]

# ---------------- API Helpers with Caching ---------------- #
@st.cache_data(show_spinner=False)
def get_tmdb_movies(category="popular"):
    if not TMDB_KEY:
        return []
    url = f"https://api.themoviedb.org/3/movie/{category}?api_key={TMDB_KEY}&language=en-US&page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception:
        return []

@st.cache_data(show_spinner=False)
def search_tmdb_movies(query):
    if not TMDB_KEY:
        return []
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception:
        return []

@st.cache_data(show_spinner=False)
def get_omdb_data(title, year=None):
    if not OMDB_KEY:
        return {}
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"
    if year:
        url += f"&y={year}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            return {}
    except Exception:
        return {}

@st.cache_data(show_spinner=False)
def get_trailer(movie_id):
    """Fetch YouTube trailer for a movie"""
    if not TMDB_KEY:
        return None
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        videos = response.json().get("results", [])
        for video in videos:
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"https://www.youtube.com/embed/{video['key']}"
        return None
    except Exception:
        return None

# ---------------- Helpers ---------------- #
def star_rating(rating, scale=10):
    if rating == "N/A" or rating is None:
        return "N/A"
    stars = "⭐" * int(round(float(rating) / (scale/5)))
    return stars + f" ({rating}/{scale})"

# ---------------- STREAMLIT APP ---------------- #
st.set_page_config(page_title="🎬 Movie Ratings App", layout="wide")

# Session state for login
if "user" not in st.session_state:
    st.session_state.user = None

# Sidebar menu (remember last selected page)
if "menu" not in st.session_state:
    st.session_state["menu"] = "Login"

menu = st.sidebar.selectbox("Menu", ["Login", "Signup", "App"], index=["Login", "Signup", "App"].index(st.session_state["menu"]))

# ---------------- SIGNUP ---------------- #
if menu == "Signup":
    st.sidebar.header("Create Account")
    username = st.sidebar.text_input("Username")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    confirm_password = st.sidebar.text_input("Confirm Password", type="password")

    if st.sidebar.button("Signup"):
        # Validation checks
        if not username or not email or not password or not confirm_password:
            st.sidebar.error("⚠️ All fields are required.")
        elif password != confirm_password:
            st.sidebar.error("⚠️ Passwords do not match.")
        elif db.query(User).filter_by(username=username).first():
            st.sidebar.error("⚠️ Username already exists.")
        elif db.query(User).filter_by(email=email).first():
            st.sidebar.error("⚠️ Email already registered.")
        else:
            create_user(username, email, password)
            st.sidebar.success("✅ Account created successfully! Please log in.")

# ---------------- LOGIN ---------------- #
elif menu == "Login":
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.user = user
            st.sidebar.success(f"✅ Welcome {username}!")
            st.session_state["menu"] = "App"  # Switch menu to App
            st.rerun()  # Refresh page to load the App directly
        else:
            st.sidebar.error("❌ Invalid credentials")

# ---------------- MOVIE APP ---------------- #
elif menu == "App":
    if not st.session_state.user:
        st.warning("⚠️ Please login to access the app.")
        st.stop()

    st.title(f"🎥 Movie Ratings Dashboard - Welcome {st.session_state.user.username}")
    st.write("Search movies or explore categories to see ratings from **TMDb**, **IMDb**, and **Rotten Tomatoes**.")

    # Sidebar options
    st.sidebar.header("Options")
    category = st.sidebar.selectbox(
        "Browse Category",
        ["popular", "top_rated", "now_playing"]
    )

    search_query = st.sidebar.text_input("🔍 Search a movie by title")

    # Manual cache refresh
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.sidebar.success("✅ Cache cleared. Reloading fresh data...")

    # ---------------- Logic ---------------- #
    if search_query:
        movies = search_tmdb_movies(search_query)
    else:
        movies = get_tmdb_movies(category)

    # ---------------- Display Movies ---------------- #
    if not movies:
        st.warning("⚠️ No movies found. Try another search or category.")
    else:
        for movie in movies[:10]:  # show top 10 only
            title = movie.get("title", "N/A")
            poster_path = movie.get("poster_path", None)
            release_date = movie.get("release_date", "N/A")
            overview = movie.get("overview", "No overview available.")
            tmdb_rating = movie.get("vote_average", "N/A")

            # Fetch OMDb data (IMDb + Rotten Tomatoes)
            omdb = get_omdb_data(title, year=release_date[:4] if release_date != "N/A" else None)
            imdb_rating = omdb.get("imdbRating", "N/A")
            rt_rating = "N/A"
            if omdb.get("Ratings"):
                for rating in omdb["Ratings"]:
                    if rating["Source"] == "Rotten Tomatoes":
                        rt_rating = rating["Value"]

            # Layout
            st.markdown("---")
            col1, col2 = st.columns([1, 3])

            with col1:
                if poster_path:
                    st.image(f"https://image.tmdb.org/t/p/w300{poster_path}", use_container_width=True)
                else:
                    st.write("No poster available")

                # Watchlist button (DB-based)
                if st.button(f"⭐ Add '{title}'", key=f"watch_{movie['id']}"):
                    add_to_watchlist(st.session_state.user.id, title)
                    st.success(f"✅ '{title}' added to your watchlist!")

            with col2:
                st.subheader(f"{title} ({release_date[:4] if release_date != 'N/A' else 'Unknown'})")

                # Tabs for ratings & details
                tab1, tab2, tab3, tab4 = st.tabs(["⭐ Ratings", "📝 Overview", "🎞 More Info", "▶ Trailer"])

                with tab1:
                    st.write(f"**TMDb:** {star_rating(tmdb_rating)}")
                    st.write(f"**IMDb:** {star_rating(imdb_rating)}")
                    st.write(f"**Rotten Tomatoes:** {rt_rating}")

                with tab2:
                    st.write(overview)

                with tab3:
                    st.write(f"🔗 [TMDb Page](https://www.themoviedb.org/movie/{movie['id']})")
                    if omdb.get("Website") and omdb.get("Website") != "N/A":
                        st.write(f"🌐 [Official Website]({omdb['Website']})")

                with tab4:
                    trailer_url = get_trailer(movie["id"])
                    if trailer_url:
                        st.components.v1.iframe(trailer_url, height=315)
                    else:
                        st.write("No trailer available")

    # ---------------- Watchlist in Sidebar ---------------- #
    st.sidebar.subheader("📌 Your Watchlist")
    user_watchlist = get_watchlist(st.session_state.user.id)
    if user_watchlist:
        for item in user_watchlist:
            st.sidebar.write("🎬", item)
    else:
        st.sidebar.write("No movies added yet")

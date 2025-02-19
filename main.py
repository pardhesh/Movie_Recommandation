from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load dataset
df = pd.read_csv("movies.csv")

# Fill NaN values
features = ["genres", "keywords", "tagline", "cast", "director", "title"]
for feature in features:
    df[feature] = df[feature].fillna("")

# Combine features into a single string
df["combined_features"] = df["genres"] + " " + df["keywords"] + " " + df["tagline"] + " " + df["cast"] + " " + df["director"] + " " + df["title"]

# Convert text data to numerical vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df["combined_features"])

# Compute similarity scores
similarity = cosine_similarity(feature_vectors)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recommend")
async def recommend(movie: str):
    movie_name = movie.lower()
    list_of_movies = df["title"].tolist()
    
    find_close_match = difflib.get_close_matches(movie_name, list_of_movies)
    
    if not find_close_match:
        return {"recommendations": []}

    close_match = find_close_match[0]
    index_of_movie = df[df.title == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i, movie in sorted_movies[1:11]:  # Get top 10 recommendations
        recommendations.append(df.iloc[i]["title"])

    return {"recommendations": recommendations}

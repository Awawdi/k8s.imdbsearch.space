import os
import logging
from uuid import UUID, uuid4
from imdb import IMDb
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
import pickle

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
CACHE_FILE = 'movie_cache.pkl'

app = FastAPI()

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'rb') as cache_file:
                cache = pickle.load(cache_file)
                logging.info(f"Cache loaded successfully from {CACHE_FILE}")
                return cache
        except Exception as e:
            logging.error(f"Failed to load cache from {CACHE_FILE}: {e}")
            return {}
    logging.info(f"Cache file {CACHE_FILE} not found. Starting with an empty cache.")
    return {}


def save_cache(cache):
    try:
        with open(CACHE_FILE, 'wb') as cache_file:
            pickle.dump(cache, cache_file)
            logging.info(f"Cache saved successfully to {CACHE_FILE}")
    except Exception as e:
        logging.error(f"Failed to save cache to {CACHE_FILE}: {e}")

# Initialize cache
cache = load_cache()

@app.get("/")
async def read_root():
    return {"ENV": f"{os.environ.get('HOSTNAME','DEFAULT')}"}

@app.get("/health")
async def health_check():
    return {"status":"healthy"}

@app.post("/api/search")
async def search_movies_endpoint(payload: dict):
    search_string = payload.get("search")
    if not search_string:
        raise HTTPException(status_code=400, detail="Movie name is required")

    try:
        results = search_movies(search_string, cache)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def search_movies(search_string, cache):
    if search_string in cache:
        logging.info(f"Cache hit for search: {search_string}")
        return cache[search_string]

    logging.info(f"Cache miss for search: {search_string}. Querying IMDb...")
    imdb_instance = IMDb()
    movies = imdb_instance.search_movie(search_string, results=20)  # Limit to top 20 results

    # Extract only basic fields without calling update
    detailed_movies = []
    for movie in movies:
        detailed_movies.append({
            "title": movie.get('title'),
            "year": movie.get('year'),
            "parental_guide": movie.get('certificates'),
            "rating": movie.get('rating'),
            "id": movie.movieID,  # Movie ID can be used later for further details if needed
        })

    # Cache the results
    cache[search_string] = detailed_movies
    save_cache(cache)
    return detailed_movies



# class credentials:
#     self._vm_user, self._vm_password = VaultAPI.get_instance().get_credentials(Users.VM_WARE_USER)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
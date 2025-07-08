# type: ignore
from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine with echo=False to suppress SQL logging
engine = create_engine(DB_URL, echo=False)

def create_table() -> None:
    """
    Create the movies table in the database if it does not exist.
    Returns:
        None
    """
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_image_url TEXT NOT NULL
            )
        """))
        connection.commit()

def list_movies() -> dict:
    """
    Retrieve all movies from the database.
    Returns:
        dict: A dictionary where the keys are movie titles and the values are dictionaries with year and rating.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_image_url FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_image_url": row[3]} for row in movies}

def add_movie(title: str, year: int, rating: float, poster_image_url: str) -> None:
    """
    Add a new movie to the database.
    Args:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
        poster_image_url (str): The URL of the poster image.
    Returns:
        None
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
                INSERT INTO movies (title, year, rating, poster_image_url)
                VALUES (:title, :year, :rating, :poster_image_url)
            """), {
                "title": title,
                "year": year,
                "rating": rating,
                "poster_image_url": poster_image_url
            })
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie: {e}")

def delete_movie(title: str) -> None:
    """
    Delete a movie from the database.
    Args:
        title (str): The title of the movie to delete.
    Returns:
        None
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()
            if result.rowcount == 0:
                print(f"No movie found with title '{title}'.")
            else:
                print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting movie: {e}")

def update_movie(title: str, rating: float) -> None:
    """
    Update a movie's rating in the database.
    Args:
        title (str): The title of the movie to update.
        rating (float): The new rating for the movie.
    Returns:
        None
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"), {
                "title": title,
                "rating": rating
            })
            connection.commit()
            if result.rowcount == 0:
                print(f"No movie found with title '{title}'.")
            else:
                print(f"Rating for '{title}' updated to {rating}.")
        except Exception as e:
            print(f"Error updating movie: {e}")

def search_movie(title: str) -> list[dict[str, str | float]]:
    """
    Search for a movie by title in the database.
    Args:
        title (str): The title of the movie to search for.
    Returns:
        list[dict[str, str | float]]: A list of dictionaries with movie titles and ratings.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, rating FROM movies WHERE title LIKE :title"), {
            "title": f"%{title}%"
        })
        rows = result.fetchall()
    return [{"title": row[0], "rating": row[1]} for row in rows] if rows else []

def sort_movies_by_rating() -> list[dict[str, str | float]]:
    """
    Sort movies by rating in descending order.
    Returns:
        list[dict[str, str | float]]: A list of dictionaries with movie titles and ratings, sorted by rating.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, rating FROM movies ORDER BY rating DESC"))
        rows = result.fetchall()
    return [{"title": row[0], "rating": row[1]} for row in rows]

# 🔧 Create table automatically on module import
create_table()

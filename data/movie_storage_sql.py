# type: ignore
from sqlalchemy import create_engine, text



engine = None

def init_storage() -> None:
    """Initialize the database connection.
    Returns:
        None
    """
    global engine
    DB_URL = f"sqlite:///databases/movies.db"
    engine = create_engine(DB_URL, echo=False)
    create_table()

def create_table() -> None:
    """
    Create the movies table in the database if it does not exist.
    Returns:
        None
    """
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            );
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_image_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """))
        connection.commit()


def get_or_create_user(username: str) -> int:
    """
    Get the user_id for a given username. If the user does not exist, create it.
    
    Args:
        username (str): The username to find or create.
    
    Returns:
        int: The user_id of the existing or newly created user.
    """
    with engine.connect() as connection:
        # Check if user exists
        result = connection.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()

        if result:
            return result[0]  # user_id already exists

        # Create new user
        connection.execute(
            text("INSERT INTO users (username) VALUES (:username)"),
            {"username": username}
        )
        connection.commit()

        # Retrieve the new user's ID
        new_user_id = connection.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()[0]

        return new_user_id



def list_movies(user_id: int) -> dict:
    """
    Retrieve all movies from the database.
    Returns:
        dict: A dictionary where the keys are movie titles and the values are dictionaries with year and rating.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_image_url FROM movies WHERE user_id = :user_id"), {
            "user_id": user_id
        })
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_image_url": row[3]} for row in movies}

def add_movie(title: str, year: int, rating: float, poster_image_url: str, user_id: int) -> None:
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
                INSERT INTO movies (title, year, rating, poster_image_url, user_id)
                VALUES (:title, :year, :rating, :poster_image_url, :user_id)
            """), {
                "title": title,
                "year": year,
                "rating": rating,
                "user_id": user_id,
                "poster_image_url": poster_image_url
            })
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie: {e}")

def delete_movie(title: str, user_id: int) -> None:
    """
    Delete a movie from the database.
    Args:
        title (str): The title of the movie to delete.
    Returns:
        None
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(text("DELETE FROM movies WHERE title = :title AND user_id = :user_id"), {"title": title, "user_id": user_id})
            connection.commit()
            if result.rowcount == 0:
                print(f"No movie found with title '{title}'.")
            else:
                print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting movie: {e}")


def search_movie(title: str, user_id: int) -> list[dict[str, str | float]]:
    """
    Search for a movie by title in the database.
    Args:
        title (str): The title of the movie to search for.
    Returns:
        list[dict[str, str | float]]: A list of dictionaries with movie titles and ratings.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, rating FROM movies WHERE title LIKE :title AND user_id = :user_id"), {
            "title": f"%{title}%",
            "user_id": user_id
        })
        rows = result.fetchall()
    return [{"title": row[0], "rating": row[1]} for row in rows] if rows else []

def sort_movies_by_rating(user_id: int) -> list[dict[str, str | float]]:
    """
    Sort movies by rating in descending order.
    Returns:
        list[dict[str, str | float]]: A list of dictionaries with movie titles and ratings, sorted by rating.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, rating FROM movies WHERE user_id = :user_id ORDER BY rating DESC"), {
            "user_id": user_id
        })
        rows = result.fetchall()
    return [{"title": row[0], "rating": row[1]} for row in rows]

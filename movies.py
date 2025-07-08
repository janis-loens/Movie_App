# type: ignore
import random
import os
from statistics import median as get_median
import movie_storage_sql as storage
import API_communication as api

def pause() -> None:
    """
    Pauses program execution to give the user time to read the output.

    Returns:
        None
    """

    input("\nPress Enter to continue.")


def get_valid_name() -> str:
    """
    Ensures the given movie name is a non-empty string.

    Returns:
        str: A valid movie name.

    Raises:
        ValueError: If the input is empty.
        KeyError: If the movie does not exist in the database.
    """
    while True:
        movie_name = input("Enter the movie name: ").strip()
        if not movie_name:
            raise ValueError("You have to enter a movie name.")
        if movie_name not in storage.list_movies():
            raise KeyError(f"Movie '{movie_name}' does not exist in the database.")
        return movie_name


def get_valid_rating() -> float:
    """
    Ensures the given rating is float between 0 and 10 included.

    Returns:
        float: A float between 0 and 10.

    Raises:
        ValueError: If the input is not a valid float or is outside the range of 0.0 to 10.0.
    """
    while True:
        try:
            rating = float(input("Enter a decimal movie rating (0.0–10.0): "))
            if not 0 <= rating <= 10:
                raise ValueError
            return rating
        except ValueError:
            print("Invalid rating. Please enter a number between 0.0 and 10.0.")


def list_movies() -> None:
    """
    Retrieve and display all movies from the database.

    Returns:
        None
    Raises:
        ValueError: If no movies are found in the database.
    """
    movies = storage.list_movies()
    if not movies:
        raise ValueError("No movies found in the database.")
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def add_movie(movie_name: str) -> None:
    """
    Add a movie to the movie database, unless it is already in the database.

    Args:
        movie_name (str): The name of the movie.
        movie_rating (float): The rating of the movie in the range of 0 to 10, 10 included.
        movie_year (int): The year of the movie release.

    Returns:
        None

    Raises:
        ValueError: If movie name, rating, or year is empty.
        ValueError: If movie name already exists.
    """
    if not movie_name:
        raise ValueError("Movie name must be provided.")
    movies = storage.list_movies()
    if movie_name in movies:
            raise ValueError(f"Movie '{movie_name}' already exists.")
    try:
        movie_data = api.get_movie_data(movie_name)
    except Exception as e:
        print(f"Could not fetch movie data: {e}")
        return  # stop further execution
    if not movie_data:
        raise ValueError(f"Movie '{movie_name}' not found in the database.")
    
    movie_title = movie_data.get("Title", "Unknown")
    movie_year = movie_data.get("Year", "Unknown")
    movie_rating = movie_data.get("imdbRating", "Unknown")
    poster_image_url = movie_data.get("Poster", "Unknown")
    if movie_title == "Unknown" or movie_year == "Unknown" or movie_rating == "Unknown":
        raise ValueError("Movie data not found. Please check the movie name.")
    storage.add_movie(movie_title, movie_year, movie_rating, poster_image_url)


def delete_movie(movie_name: str) -> None:
    """
    Delete a movie and its rating from the movie database, if it exists.

    Args:
        movie_name (str): The name of the movie to delete.

    Returns:
        None

    Raises:
        ValueError: If movie name is empty.
    """
    if not movie_name:
        raise ValueError("Movie name must be provided.")
    storage.delete_movie(movie_name)


def update_movie(movie_name: str, new_movie_rating: float) -> None:
    """
    Update the rating of a movie in the movie database.

    Args:
        movie_name: The name of the movie.
        new_movie_rating: The new rating of the movie.

    Returns:
        None

    Raises:
        ValueError: If movie name or new rating is empty.

    """
    if not movie_name or not new_movie_rating:
        raise ValueError("Movie name and new rating must be provided.")
    storage.update_movie(movie_name, new_movie_rating)


def movies_stats() -> tuple:
    """
    Return statistical information about the movie database, including
    the average rating, median rating, best and worst movies.

    Returns:
        tuple:
            average_rating (float): The average of all movie ratings.
            best_movie (tuple): A tuple of the highest-rated movie (name, rating).
            worst_movie (tuple): A tuple of the lowest-rated movie (name, rating).
            median_rating (float): The median of all movie ratings.
    Raises:
        ValueError: If the movie database is empty.
    """
    
    dict_of_movies = storage.list_movies()
    if not dict_of_movies:
        raise ValueError("No movies found.")
    ratings = list((data["rating"] for movie, data in dict_of_movies.items()))
    sum_of_ratings = sum(ratings)

    max_rating = max(data["rating"] for movie, data in dict_of_movies.items())
    best_movies = [
    (movie, data["rating"])
    for movie, data in dict_of_movies.items()
    if data["rating"] == max_rating
]
    min_rating = min(data["rating"] for movie, data in dict_of_movies.items())
    worst_movies = [
    (movie, data["rating"])
    for movie, data in dict_of_movies.items()
    if data["rating"] == min_rating
    ]

    average_rating = sum_of_ratings / len(ratings)
    median_rating = get_median(ratings)

    return average_rating, best_movies, worst_movies, median_rating


def get_random_movie() -> dict:
    """
    Return a random movie dict from the list of dictionaries of movies.

    Returns:
        dict: A randomly selected movie dict.

    Raises:
        ValueError: If the database is empty.
    """
    dicts_of_movies = storage.list_movies()
    if not dicts_of_movies:
        raise ValueError("No movies found in the database.")
    title, details = random.choice(list(dicts_of_movies.items()))
    if not details or 'rating' not in details:
        raise ValueError("Movie details are incomplete.")
    return {'title': title, **details}


def search_movie(part_of_movie_name: str) -> list[dict]:
    """
    Return all movies containing the input string, case-insensitive.

    Args:
        part_of_movie_name (str): A substring to search for within movie titles.

    Returns:
        list[dict]: A list of dictionaries with movie titles and ratings.

    Raises:
        ValueError: If the database is empty.
    """
    list_of_movie_dicts = storage.search_movie(part_of_movie_name)
    if not list_of_movie_dicts:
        raise ValueError("No movies found with that name.")
    return list_of_movie_dicts


def sort_movies_by_rating() -> list[dict]:
    """
    Sort movies by rating in descending order.

    Returns:
        list[dict]: A list of dictionaries with movie titles and ratings.

    Raises:
        ValueError: If the dictionary is empty.
    """
    sorted_movie_list =  storage.sort_movies_by_rating()
    if not sorted_movie_list:
        raise ValueError("No movies found to sort.")
    return sorted_movie_list


def get_website_name() -> str:
    """
    Get the name of the website from the user.

    Returns:
        str: The name of the website.
    
    Raises:
        ValueError: If the name is empty.
    """
    while True:
        name = input("Enter the name of the website: ").strip()
        if not name:
            raise ValueError("Website name cannot be empty.")
        return name


def generate_website(name: str) -> None:
    """
    Generate a static HTML website for the movie database.

    Args:
        name (str): The name of the website.

    Returns:
        None

    Raises:
        ValueError: If the database is empty.
    """

    base_dir = os.path.dirname(__file__)  # directory of the current script
    template_path = os.path.join(base_dir, "website", "index_template.html")
    index_path = os.path.join(base_dir, "website", "index.html")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, "r") as file:
        template = file.read()
    dict_of_movies = storage.list_movies()

    if not dict_of_movies:
        raise ValueError("No movies found in the database to generate a website.")
    movies_html = ""
    for movie, data in dict_of_movies.items():
        movies_html += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{data['poster_image_url']}" alt="{movie} poster">
                <div class="movie-title">{movie}</div>
                <div class="movie-year">{data['year']}</div>
            </div>
        </li>
        """
    html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movies_html)
    html_content = html_content.replace("__TEMPLATE_TITLE__", name)
    with open(index_path, "w") as file:
        file.write(html_content)
    print("Website generated successfully at /website/index.html.")
    pause()
        


def main():
    """
    Main loop for the movie database CLI. Presents options to the user
    and performs operations based on user input.
    """
    print("Welcome to the Movie Database CLI!")
    websitename = get_website_name()
    menu_text = f"""
        ********** {websitename} **********

        Menu:
        0. Quit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Generate website

        Enter choice (0-9):

        """
    while True:
        user_choice = input(menu_text)

        if user_choice == "0":
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm == "y":
                print("Goodbye!")
                break

        elif user_choice == "1":
            try:
                list_movies()
            except ValueError as v_e:
                print(f"Error: {v_e}")
            except KeyError as k_e:
                print(f"Error: {k_e}")
            except Exception as e:
                print(f"An unexpected error occurred while listing movies: {e}")
            pause()

        elif user_choice == "2":
            while True:
                movie_name = input("Enter movie name: ")
                if movie_name:
                    break
                else:
                    print("Invalid input. You have to enter a movie name.")
            try:
                add_movie(movie_name)
            except ValueError as v_e:
                print(f"Error: {v_e}")
            except KeyError as k_e:
                print(f"Error: {k_e}")
            
            pause()

        elif user_choice == "3":
            try:
                movie_name = get_valid_name()
                confirm = input(f"Are you sure you want to delete '{movie_name}'? (y/n): ").lower()
                if confirm != "y":
                    print("Deletion cancelled.")
                    continue
                # Call the delete_movie function to remove the movie from the database
                delete_movie(movie_name)

            except KeyError as k_e:
                print(f"Error: {k_e}")

            finally:
                pause()

        elif user_choice == "4":
            try:
                movie_name = get_valid_name()
                input_new_rating = get_valid_rating()
                update_movie(movie_name, input_new_rating)
                print(f"Movie '{movie_name}' successfully updated.")

            except KeyError as k_e:
                print(f"Error: {k_e}")

            except ValueError as v_e:
                print(f"Error: {v_e}")

            finally:
                pause()


        elif user_choice == "5":
            try:
                average_rating, best_movies, worst_movies, median_rating = movies_stats()
                print(f"Average rating: {average_rating}")
                print(f"Median rating: {median_rating}")
                print(f"Best movie(s):")
                for movie, rating in best_movies:
                   print(f"\t{movie}, {rating}")
                print(f"Worst movie(s):")
                for movie, rating in worst_movies:
                    print(f"\t{movie}, {rating}")

            except ValueError as v_e:
                print(f"Error: {v_e}")

            finally:
                pause()

        elif user_choice == "6":
            try:
                random_movie = get_random_movie()
                print(f"Your movie for tonight: {random_movie['title']},"
                      f" it's rated {random_movie['rating']}.")

            except ValueError as v_e:
                print(f"Error: {v_e}")
                

            finally:
                pause()

        elif user_choice == "7":
            try:
                while True:
                    part_of_movie_name = input("Enter a part of the movie name: ")
                    if part_of_movie_name:
                        break
                    else:
                        print("You have to enter a part of the movie name.")
                list_of_movies_with_part_in_it = search_movie(part_of_movie_name)
                for movie in list_of_movies_with_part_in_it:
                    print(f"{movie['title']}: {movie['rating']}")

            except ValueError as v_e:
                print(f"Error: {v_e}.")

            except KeyError as k_e:
                print(f"Error: {k_e}.")

            finally:
                pause()

        elif user_choice == "8":
            try:
                movies_sorted_by_rating = sort_movies_by_rating()
                for movie in movies_sorted_by_rating:
                    print(f"{movie['title']}: {movie['rating']}")

            except ValueError as v_e:
                print(f"Error: {v_e}.")

            finally:
                pause()

        elif user_choice == "9":
            generate_website(websitename)

        else:
            print("Invalid choice. Please choose a number between 0 and 10.")
            pause()


if __name__ == "__main__":
    main()

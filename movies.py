# type: ignore
import random
import os
from statistics import median as get_median
import data.movie_storage_sql as storage
import data.API_communication as api


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
        if movie_name not in storage.list_movies(user_id):
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


def list_movies(user_id: int) -> None:
    """
    Retrieve and display all movies from the database.

    Returns:
        None
    Raises:
        ValueError: If no movies are found in the database.
    """
    movies = storage.list_movies(user_id)
    if not movies:
        raise ValueError("No movies found in the database.")
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def add_movie(movie_name: str, user_id: int) -> None:
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
    movies = storage.list_movies(user_id)
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
    storage.add_movie(movie_title, movie_year, movie_rating, poster_image_url, user_id)


def delete_movie(movie_name: str, user_id: int) -> None:
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
    storage.delete_movie(movie_name, user_id)


def movies_stats(user_id: int) -> tuple:
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

    dict_of_movies = storage.list_movies(user_id)
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


def get_random_movie(user_id: int) -> dict:
    """
    Return a random movie dict from the list of dictionaries of movies.

    Returns:
        dict: A randomly selected movie dict.

    Raises:
        ValueError: If the database is empty.
    """
    dicts_of_movies = storage.list_movies(user_id)
    if not dicts_of_movies:
        raise ValueError("No movies found in the database.")
    title, details = random.choice(list(dicts_of_movies.items()))
    if not details or 'rating' not in details:
        raise ValueError("Movie details are incomplete.")
    return {'title': title, **details}


def search_movie(part_of_movie_name: str, user_id: int) -> list[dict]:
    """
    Return all movies containing the input string, case-insensitive.

    Args:
        part_of_movie_name (str): A substring to search for within movie titles.

    Returns:
        list[dict]: A list of dictionaries with movie titles and ratings.

    Raises:
        ValueError: If the database is empty.
    """
    list_of_movie_dicts = storage.search_movie(part_of_movie_name, user_id)
    if not list_of_movie_dicts:
        raise ValueError("No movies found with that name.")
    return list_of_movie_dicts


def sort_movies_by_rating(user_id: int) -> list[dict]:
    """
    Sort movies by rating in descending order.

    Returns:
        list[dict]: A list of dictionaries with movie titles and ratings.

    Raises:
        ValueError: If the dictionary is empty.
    """
    sorted_movie_list =  storage.sort_movies_by_rating(user_id)
    if not sorted_movie_list:
        raise ValueError("No movies found to sort.")
    return sorted_movie_list


def get_profiles() -> list[str]:
    """
    Get all available profiles in the movie database.

    Returns:
        list[str]: A list of profile names.
    
    Raises:
        ValueError: If no profiles are found.
    """
    with open("data/profiles.txt", "r") as file:
        profiles = [line.strip() for line in file if line.strip()]
    if not profiles:
        return []
    return profiles


def list_profiles() -> list[str]:
    """
    List all available profiles in the movie database.

    Returns:
        list[str]: A list of profile names.
    
    Raises:
        ValueError: If no profiles are found.
    """
    try:
        profiles = get_profiles()
        if not profiles:
            return []
        print("Available profiles:")
        for i, profile in enumerate(profiles, start=1):
            print(f"{i}. {profile}")
    except ValueError as e:
        print(f"Error: {e}")
        return []
    

def create_new_profile() -> None:
    """
    Create a new profile for the movie database.

    Args:
        profile_name (str): The name of the new profile.

    Returns:
        None
    """
    with open("data/profiles.txt", "a") as file:
        new_profile = get_name()
        file.write(f"{new_profile}\n")
        print(f"Profile '{new_profile}' created successfully.")
        return new_profile


def select_profile() -> str:
    """
    Select a profile for the movie database.

    Returns:
        str: The name of the selected profile.
    
    Raises:
        ValueError: If no profile is selected.
    """
    while True:

        profiles = get_profiles()
        list_profiles()
    
        if not profiles:
            print("No profiles found. Please create a new profile.")
            return create_new_profile()
        else:
            choice = input(f"Select a profile by number (0-{len(profiles)}) or 0 to create a new one: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(profiles):
                return profiles[int(choice) - 1]
            elif choice == "0":
                return create_new_profile()
            else:
                print("Invalid choice. Please select a valid profile number.")


def change_profile() -> str:
    profile = select_profile()
    storage.init_storage()
    return profile


def get_name() -> str:
    """
    Get the name of the website from the user.

    Returns:
        str: The name of the website.
    
    Raises:
        ValueError: If the name is empty.
    """
    while True:
        name = input("Enter your name: ").strip()
        if not name:
            raise ValueError("Your name cannot be empty.")
        return name


def generate_website(name: str, user_id: int) -> None:
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
    index_path = os.path.join(base_dir, "website", f"{name}.html")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, "r") as file:
        template = file.read()
    dict_of_movies = storage.list_movies(user_id)

    if not dict_of_movies:
        raise ValueError("No movies found in the database to generate a website.")
    movies_html = ""
    for movie, data in dict_of_movies.items():
        movies_html += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{data['poster_image_url']}" alt="{movie} poster">
                <div class="movie-title">{movie}</div>
                <div class="movie-rating">IMDb: {data['rating']}</div>
                <div class="movie-year">{data['year']}</div>
            </div>
        </li>
        """
    html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movies_html)
    html_content = html_content.replace("__TEMPLATE_TITLE__", f"Movie Database of {name}")
    with open(index_path, "w") as file:
        file.write(html_content)
    print(f"Website generated successfully at /website/{name}.html.")
    pause()
        

def main():
    """
    Main loop for the movie database CLI. Presents options to the user
    and performs operations based on user input.
    """
    print("Welcome to the Movie Database CLI!")

    if not os.path.exists("data/profiles.txt"):
        with open("data/profiles.txt", "w") as file:
            file.write("")
    current_profile = change_profile()
    user_id = storage.get_or_create_user(current_profile)

    while True:
        menu_text = f"""
        ********** Movie Database of {current_profile} **********

        Menu:
        0. Quit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Stats
        5. Random movie
        6. Search movie
        7. Movies sorted by rating
        8. Generate website
        9. Change profile

        Enter choice (0-9):

        """

        user_choice = input(menu_text)

        if user_choice == "0":
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm == "y":
                print("Goodbye!")
                break

        elif user_choice == "1":
            try:
                list_movies(user_id)
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
                add_movie(movie_name, user_id)
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
                delete_movie(movie_name, user_id)

            except KeyError as k_e:
                print(f"Error: {k_e}")

            finally:
                pause()


        elif user_choice == "4":
            try:
                average_rating, best_movies, worst_movies, median_rating = movies_stats(user_id)
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

        elif user_choice == "5":
            try:
                random_movie = get_random_movie(user_id)
                print(f"Your movie for tonight: {random_movie['title']},"
                      f" it's rated {random_movie['rating']}.")

            except ValueError as v_e:
                print(f"Error: {v_e}")
                

            finally:
                pause()

        elif user_choice == "6":
            try:
                while True:
                    part_of_movie_name = input("Enter a part of the movie name: ")
                    if part_of_movie_name:
                        break
                    else:
                        print("You have to enter a part of the movie name.")
                list_of_movies_with_part_in_it = search_movie(part_of_movie_name, user_id)
                for movie in list_of_movies_with_part_in_it:
                    print(f"{movie['title']}: {movie['rating']}")

            except ValueError as v_e:
                print(f"Error: {v_e}.")

            except KeyError as k_e:
                print(f"Error: {k_e}.")

            finally:
                pause()

        elif user_choice == "7":
            try:
                movies_sorted_by_rating = sort_movies_by_rating(user_id)
                for movie in movies_sorted_by_rating:
                    print(f"{movie['title']}: {movie['rating']}")

            except ValueError as v_e:
                print(f"Error: {v_e}.")

            finally:
                pause()

        elif user_choice == "8":
            generate_website(current_profile, user_id)

        elif user_choice == "9":
            current_profile = change_profile()
            user_id = storage.get_or_create_user(current_profile)

        else:
            print("Invalid choice. Please choose a number between 0 and 9.")
            pause()


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import orjson
import random
import string


def generate_large_file(file_name: str, number_of_movies: int) -> None:
    movies = []
    for _ in range(number_of_movies):
        movie = {
            "title": "".join(random.choice(string.ascii_lowercase) for _ in range(10)),
            "year": random.randint(1900, 2020),
            "director": "".join(
                random.choice(string.ascii_lowercase) for _ in range(10)
            ),
            "rating": random.randint(1, 5),
        }
        movies.append(movie)

    with open(file_name, "wb") as f:
        f.write(orjson.dumps(movies))


def main():
    # expose number of movies to generate in the command line
    number_of_movies = int(input("Enter number of movies: "))
    generate_large_file("data/movies.json", number_of_movies)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import argparse
import random
import string
from pathlib import Path
from typing import Final

import orjson

BYTES_PER_MOVIE: Final[int] = 70


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

    file = Path(file_name)
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("wb") as f:
        f.write(orjson.dumps(movies))


def main():
    # expose number of movies to generate in the command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file-size-in-mib", type=int, required=True, help="Desired file size in MiB"
    )
    args = parser.parse_args()

    file_size_in_bytes = args.file_size_in_mib << 20

    generate_large_file(
        file_name="data/movies.json",
        number_of_movies=file_size_in_bytes // BYTES_PER_MOVIE,
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import orjson

from utils import measure


def main() -> None:
    print("Parsing movies with orjson.loads...")

    with measure("orjson.loads"):
        with open("data/movies.json", "rb") as f:
            movies = orjson.loads(f.read())
            print(f"Parsed movies: {len(movies):,}")


if __name__ == "__main__":
    main()

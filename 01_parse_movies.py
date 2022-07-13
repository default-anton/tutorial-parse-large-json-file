#!/usr/bin/env python

import json

from utils import measure


def main() -> None:
    print("Parsing movies with json.loads...")

    with measure("json.loads"):
        with open("data/movies.json") as f:
            movies = json.loads(f.read())
            print(f"Parsed movies: {len(movies):,}")


if __name__ == "__main__":
    main()

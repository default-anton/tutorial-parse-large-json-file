#!/usr/bin/env python

import argparse

import orjson

from utils import measure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch-size", type=int, required=True, help="Batch size in bytes"
    )

    args = parser.parse_args()

    print(
        f"Parsing movies with orjson.loads in batches of size {args.batch_size} bytes..."
    )

    with measure("orjson.loads in batches"):
        parse_movies_in_batches(args.batch_size)


def parse_movies_in_batches(batch_size: int) -> None:
    movie_count: int = 0

    with open("data/movies.json", "rb") as f:
        batch = bytearray()
        batch.extend(f.read(batch_size))
        start_pos = batch.find(b"{")
        end_pos = batch.rfind(b"}")

        while start_pos != -1 and end_pos != -1:
            # parse movies in the batch
            movies = orjson.loads(b"[" + batch[start_pos : end_pos + 1] + b"]")
            movie_count += len(movies)

            carry_over = batch[end_pos + 1 :]
            batch = bytearray(carry_over)
            batch.extend(f.read(batch_size))
            start_pos = batch.find(b"{")
            end_pos = batch.rfind(b"}")

    print(f"Parsed movies: {movie_count:,}")


if __name__ == "__main__":
    main()

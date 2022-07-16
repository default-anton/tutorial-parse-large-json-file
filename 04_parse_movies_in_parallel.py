#!/usr/bin/env python

import argparse
import io
import os
from concurrent.futures import ProcessPoolExecutor

import orjson

from utils import measure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch-size",
        type=int,
        required=True,
        help="Batch size in bytes" "--max-workers",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        required=True,
        help="Maximum number of workers",
    )

    args = parser.parse_args()

    file_size: int = os.path.getsize("data/movies.json")

    max_workers: int = args.max_workers
    batch_size: int = args.batch_size

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        args = [
            (
                batch_size,
                i * file_size // max_workers,
                (i + 1) * file_size // max_workers,
            )
            for i in range(0, max_workers - 1)
        ]
        args.append(
            (batch_size, (max_workers - 1) * file_size // max_workers, file_size)
        )
        futures = executor.map(parse_movies_in_batches, *zip(*args))

        print(
            f"Parsing movies with orjson.loads in batches of size {batch_size} bytes on {max_workers} cores..."
        )

        with measure("orjson.loads in batches on multiple cores"):
            movie_count = sum(futures)
            print(f"Parsed movies: {movie_count:,}")


def parse_movies_in_batches(batch_size: int, start_pos: int, end_pos: int) -> int:
    movie_count: int = 0
    batch = bytearray()

    with open("data/movies.json", "rb") as f:
        f.seek(start_pos, io.SEEK_SET)

        bytes_left = end_pos - f.tell()
        batch[:] = f.read(min(batch_size, bytes_left))
        open_bracket = batch.find(b"{")
        close_bracket = batch.rfind(b"}")

        while open_bracket != -1 and close_bracket != -1:
            # parse movies in the batch
            movies = orjson.loads(b"[" + batch[open_bracket : close_bracket + 1] + b"]")
            movie_count += len(movies)

            bytes_left = end_pos - f.tell()
            carry_over = batch[close_bracket + 1 :]
            batch[:] = carry_over + f.read(min(batch_size, bytes_left))
            open_bracket = batch.find(b"{")
            close_bracket = batch.rfind(b"}")

        # if dangling open bracket, find first close bracket in the next batch
        if open_bracket != -1 and close_bracket == -1:
            batch.extend(f.read(batch_size))
            close_bracket = batch.find(b"}", open_bracket + 1)
            movies = orjson.loads(b"[" + batch[open_bracket : close_bracket + 1] + b"]")
            movie_count += len(movies)

    return movie_count


if __name__ == "__main__":
    main()

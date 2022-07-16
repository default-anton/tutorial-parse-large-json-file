from collections.abc import Generator
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def measure(context: str) -> Generator[None, None, None]:
    perf_start = perf_counter()
    yield
    perf_end = perf_counter()
    print(f"{context}: {perf_end - perf_start:.2f} seconds\n")

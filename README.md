## Prerequisite

Tested on Mac mini (M1 chip with 8-Core CPU, 16GB Memory, 1TB SSD)

- python 3.10
- [pdm](https://pdm.fming.dev/latest/)
- `pdm install --prod --no-lock --no-editable`

## Generating Large JSON File

For example, let's create a 1GiB JSON file:

```bash
./00_generate_large_file.py --file-size-in-mib 1024
```

## Naive Approach: Reading the Entire File Into Memory Using `json.load`

### Performance

```bash
./01_parse_movies.py
```

STDOUT:

```text
Parsing movies with json.loads...
Parsed movies: 15,339,168
json.loads: 7.01 seconds
```

Time to parse 1GiB file: **7.01 seconds**

### Memory Usage

```bash
pdm run fil-profile run 01_parse_movies.py
```

Peak memory usage to parse 1GiB file: **6674.6 MiB**

## Naive Approach but Using `orjson` (the Fastest Python Library for JSON parsing)

### Performance

```bash
./02_parse_movies_with_orjson.py
```

STDOUT:

```text
Parsing movies with orjson.loads...
Parsed movies: 15,339,168
orjson.loads: 3.79 seconds
```

Time to parse 1GiB file: **3.79 seconds**

### Memory Usage

```bash
pdm run fil-profile run 02_parse_movies_with_orjson.py
```

Peak memory usage to parse 1GiB file: **6798.8 MiB**

## Batch Parsing of a JSON File

### Performance

```bash
./03_parse_movies_in_batches.py --batch-size 524288
```

STDOUT:

```text
Parsing movies with orjson.loads in batches of size 524288 bytes...
Parsed movies: 15,339,168
orjson.loads in batches: 3.64 seconds
```

Time to parse 1GiB file: **3.64 seconds**

### Memory Usage

```bash
pdm run fil-profile run 03_parse_movies_in_batches.py --batch-size 524288
```

Peak memory usage to parse 1GiB file: **6.8 MiB**

## Parsing a JSON File In Parallel

### Performance

```bash
./04_parse_movies_in_parallel.py --batch-size 524288 --max-workers 6
```

STDOUT:

```text
Parsing movies with orjson.loads in batches of size 524288 bytes on 6 cores...
Parsed movies: 15,339,168
orjson.loads in batches on multiple cores: 1.04 seconds
```

Time to parse 1GiB file: **1.04 seconds**

### Memory Usage

Peak memory usage to parse 1GiB file: **40.8 MiB**

## Design

### Multiprocessing

1. Start N process where each process reads and parses `i * F / N` bytes of the JSON file.
Where `i` is the process index, `F` is the size of the file in bytes, and `N` is the number of processes.
2. Each process parses a part of the file assigned to it.
3. Reading and parsing should be done in batches of `M` bytes, as we want to avoid reading the entire file into memory.
4. If the batch doesn't have a closing `}`, the program must seek for it in the next batch, potentially reading the first batch of the `(i + 1) * F / N` part of the file.

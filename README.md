Table of Contents
=================

* [Prerequisite](#prerequisite)
* [Generating Large JSON File](#generating-large-json-file)
* [Naive Approach - Reading the Entire File Into Memory](#naive-approach---reading-the-entire-file-into-memory)
* [Naive Approach but Using orjson - the Fastest Python Library for JSON parsing](#naive-approach-but-using-orjson---the-fastest-python-library-for-json-parsing)
* [Batch Parsing of a JSON File](#batch-parsing-of-a-json-file)
* [Parsing a JSON File In Parallel - multiprocessing](#parsing-a-json-file-in-parallel---multiprocessing)
  * [Design](#design)


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

## Naive Approach - Reading the Entire File Into Memory

```bash
./01_parse_movies.py
```

Parsing 1 GiB JSON file takes **7.01 seconds** and uses **6674.6 MiB** of RAM at peak

## Naive Approach but Using orjson - the Fastest Python Library for JSON parsing

```bash
./02_parse_movies_with_orjson.py
```

Parsing 1 GiB JSON file takes **3.79 seconds** and uses **6798.8 MiB** of RAM at peak

## Batch Parsing of a JSON File

```bash
./03_parse_movies_in_batches.py --batch-size 524288
```

Parsing 1 GiB JSON file takes **3.64 seconds** and uses **6.8 MiB** of RAM at peak

## Parsing a JSON File In Parallel - multiprocessing

```bash
./04_parse_movies_in_parallel.py --batch-size 524288 --max-workers 6
```

Parsing 1 GiB JSON file takes **1.04 seconds** and uses **40.8 MiB** of RAM at peak

### Design

1. Start N process where each process reads and parses `i * F / N` bytes of the JSON file.
Where `i` is the process index, `F` is the size of the file in bytes, and `N` is the number of processes.
2. Each process parses a part of the file assigned to it.
3. Reading and parsing should be done in batches of `M` bytes, as we want to avoid reading the entire file into memory.
4. If the batch doesn't have a closing `}`, the program must seek for it in the next batch, potentially reading the first batch of the `(i + 1) * F / N` part of the file.

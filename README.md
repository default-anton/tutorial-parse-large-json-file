## Design

### Multiprocessing

1. Start N process where each process reads and parses `i * F / N` bytes of the JSON file.
Where `i` is the process index, `F` is the size of the file in bytes, and `N` is the number of processes.
2. Each process parses a part of the file assigned to it.
3. Reading and parsing should be done in batches of `M` bytes, as we want to avoid reading the entire file into memory.
4. If the batch doesn't have a closing `}`, the program must seek for it in the next batch, potentially reading the first batch of the `(i + 1) * F / N` part of the file.

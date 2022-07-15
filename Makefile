batch_size  ?= 524288 # 512KiB
max_workers ?= 6

ifdef memory_profile
define run
	pdm run fil-profile run $(1)
endef
else
define run
	python $(1)
endef
endif


all: parse_movies parse_movies_with_orjson parse_movies_in_batches parse_movies_in_parallel

parse_movies:
	$(call run,01_parse_movies.py)

parse_movies_with_orjson:
	$(call run,02_parse_movies_with_orjson.py)

parse_movies_in_batches:
	$(call run,03_parse_movies_in_batches.py --batch-size=$(batch_size))

parse_movies_in_parallel:
	$(call run,04_parse_movies_in_parallel.py --batch-size=$(batch_size) --max-workers=$(max_workers))

.PHONY: parse_movies, parse_movies_with_orjson, parse_movies_in_batches, parse_movies_in_parallel, all

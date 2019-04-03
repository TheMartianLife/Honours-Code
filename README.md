# TODO

* Write a `hydrate.py` that performs hydration but with useful status updates, unlike the command-line version which just hangs for hours while I continually `wc -l` the output file to check it's still working.
* Write a `collate.py` that groups tweets by day and outputs new `.csv` containing total temperature and volume per some period _p_ (likely one day)
* Write a `entropy.py` that calculates some estimation of Shannon entropy over time. This requires some measure of possible microstates, where requisite values for computation must be derived from the macrostate measures we have, such as analogous volume _v_ and temperature _t_ (which should enable some density and/or pressure estimates, for example as _v_ / _p_).

# Files

## classes.py

A utility file of classes used in other scripts hereafter. The classes contained are as follows...

### `FileComponents`

| Attribute | Description |
|:---|:---|
| `absolute_path` | The full path (from OS root, including file) of the init filepath  |
| `path` | The full path (from OS root, excluding file) of the init filepath  |
| `name ` | The file name component (excluding path and extension) of the init filepath |
| `extension` | The file extension component (excluding name and extension) of the init filepath  |

**e.g.** in `/some/path/to/an/imaginary.file`, the whole thing is the absolute path. `/some/path/to/an/` is the path, `imaginary` is the name and `file` is the extension.

### `Tweet`

| Attribute | Description |
|:---|:---|
| `id` | `int` representation of Tweet identifier |
| `text` | `string` representation of Tweet body text (UTF-8 encoded) |
| `likes` | `int` representation of how many times the Tweet has been favourited |
| `retweets` | `int` representation of how many times the Tweet has been retweeted |
| `temperature` | TBD (currently `likes`) |
| `volume` | TBD (currently `retweets` + 1, to include itself) |
| `is_retweet` | `bool` representation of whether the Tweet is a retweet of another |
| `retweeted_id` | if `is_retweet`: `int` representation of original Tweet identifier, else `None` |
| `is_quote_tweet` | `bool` representation of whether the Tweet is a quote tweet of another |
| `quoted_id` | if `is_quote_tweet`: `int` representation of quoted Tweet identifier, else `None`|
| `timestamp` | `string` representation of time Tweet was posted (in %Y-%m-%d %H:%M:%S format)|

## missed-ids.py

### Inputs
| Flag | Description | Default |
|:---|:---|:---|
| `-t`/`--tweets` | the `.jsonl` file of hydrated Tweets (in JSON Lines representation) | None (**required value**) |
| `-i`/`--ids` | the `.txt` file of Tweet IDs the above file was hydrated from | Tweets file with .txt extension instead of .jsonl |
| `-o`/`--output` | the `.txt` file to create with missed Tweet IDs | IDs file with missed- prefix on filename |
| `-c`/`--checkpoint` | the number of IDs to check at a time before printing indication of progress | 100,000 |

### Outputs

A `.txt` file of IDs not successfully fetched from the original hydration request. This may be because the tweet was deleted, posted by a private user the authorising account is not permitted to view content from, or script error. This can be used to re-attempt hydration of remaining IDs, or just as an Appendix to ensure optimal experiment repeatability.

### Example usage

`$ python missed-ids.py --tweets test.jsonl --ids test.txt --checkpoint 10`

```
Executing: missed-ids.py
==> Checking tweets from: test.jsonl
==> Comparing tweet ids from: test.txt
==> Outputting missed ids to: missed-test.txt


CHECKPOINT (line 0)
CHECKPOINT (line 10)
CHECKPOINT (line 20)
CHECKPOINT (line 30)
CHECKPOINT (line 40)
CHECKPOINT (line 50)
CHECKPOINT (line 60)
CHECKPOINT (line 70)
CHECKPOINT (line 80)
CHECKPOINT (line 90)

Complete: found 39 missed ids
```

## split.py

### Inputs

| Flag | Description | Default |
|:---|:---|:---|
| `-i`/`--input` | the `.txt` file of Tweet IDs to split up | None (**required value**) |
| `-o`/`--output` | the directory to output split files to (created if it doesn't exist) | `./`Input filename without extension`/` |
| `-s`/`--split` | the maximum number of IDs to put in each file | 500,000 |
| `-c`/`--checkpoint` | the number of IDs to check at a time before printing indication of progress | 100,000 |

### Outputs

A new set of `.txt` files (in an optional new directory), in which the original file is broken into `split`-sized groups, for ease of hydrating _n_ million-line datasets.

### Example usage

`$ python split.py --input test.txt --split 50 --checkpoint 10`

```
Executing: missed-ids.py
==> Getting ids from: test.txt
==> Splitting into groups of: 50
==> Outputting ids to: test/test1.txt and onward


CHECKPOINT (line 0)
CHECKPOINT (line 10)
CHECKPOINT (line 20)
CHECKPOINT (line 30)
CHECKPOINT (line 40)
CHECKPOINT (line 50)
CHECKPOINT (line 60)
CHECKPOINT (line 70)
CHECKPOINT (line 80)
CHECKPOINT (line 90)

Complete: split into 2 files
```

## tweets.py

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_filename",
					help="JSONL filename to read in", metavar="INPUT", default=None)
parser.add_argument("-o", "--output", dest="output_filename",
					help="CSV filename to write out", metavar="OUTPUT", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
			help="How often to declare progress", metavar="CHECKPOINT", default=100000, type=int)

### Inputs

| Flag | Description | Default |
|:---|:---|:---|
| `-i`/`--input` | the `.jsonl` file of hydrated Tweets (in JSON Lines representation) | None (**required value**) |
| `-o`/`--output` | the `.csv` file to create with derived Tweet values | input file with output- prefix on filename |
| `-c`/`--checkpoint` | the number of Tweet objects to process at a time before printing indication of progress | 100,000 |

### Outputs

a `.csv` file of the values from each initialised Tweet object, laid out as below.

![image of C S V open in spreadsheet program, demonstrating column names and values](output.png)

### Example usage

`$ python tweets.py --input test.jsonl --checkpoint 10`

```
Executing: tweets.py
==> Parsing tweets from: test.jsonl
==> Outputting values to: output-test.csv


CHECKPOINT (line 0)
CHECKPOINT (line 10)
CHECKPOINT (line 20)
CHECKPOINT (line 30)
CHECKPOINT (line 40)
CHECKPOINT (line 50)
CHECKPOINT (line 60)

Complete: processed 60 tweets
```

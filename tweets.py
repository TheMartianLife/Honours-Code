import os
import csv
from classes import Tweet, FileComponents
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("input_filename", metavar="INPUT_FILE", type=str,
					help="JSONL filename to read in", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
        help="How often to declare progress", metavar="CHECKPOINT", default=50000, type=int)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_filename is None:
    print("ERROR: no input file declared.\nAborting...")
    quit()

base_file = FileComponents(args.input_filename)

if base_file.extension != ".jsonl":
    print("ERROR: input file must be valid JSON file.\nAborting...")
    quit()

# INITIALISE REQUIRED VALUES
input_filename = args.input_filename
output_filename = base_file.path + "output-" + base_file.name + ".csv"
checkpoint_value = args.checkpoint_index
tweet_count = 0

checkpoint_value = 100000

print("\nExecuting: tweets.py")
print("==> Parsing tweets from: " + input_filename)
print("==> Outputting values to: " + output_filename)
print("\n")

with open(output_filename, "w+") as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["id", "likes", "retweets", "retweeted_id", "quoted_id", "timestamp"])
    tweet_count = 0

    with open(input_filename, "r") as input_file:

        for line_number, line in enumerate(input_file):

            tweet = Tweet(line)
            csv_writer.writerow(tweet.values())

            if line_number % checkpoint_value == 0:
                print("CHECKPOINT (line " + str(line_number) + ")")

            tweet_count = line_number + 1

    print("\nComplete: processed " + str(tweet_count) + " tweets")

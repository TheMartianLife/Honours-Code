import os
import csv
from classes import Tweet, FileComponents
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_filename",
					help="JSONL filename to read in", metavar="INPUT", default=None)
parser.add_argument("-o", "--output", dest="output_filename",
					help="CSV filename to write out", metavar="OUTPUT", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
			help="How often to declare progress", metavar="CHECKPOINT", default=100000, type=int)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
base_file = FileComponents(args.input_filename)
if args.input_filename is None or base_file.extension != ".jsonl":
	print "ERROR: no valid input JSONL file declared.\nAborting..."
	quit()

# INITIALISE REQUIRED VALUES
input_filename = args.input_filename
output_filename = base_file.path + "output-" + base_file.name + ".csv" if args.output_filename is None else args.output_filename
checkpoint_value = args.checkpoint_index
tweet_count = 0

print "\nExecuting: tweets.py"
print "==> Parsing tweets from: " + input_filename
print "==> Outputting values to: " + output_filename
print "\n"

with open(input_filename, "r") as input_file, open(output_filename, "w+") as output_file:

	csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["id", "tweet", "likes", "retweets", "temperature", "volume", "is_retweet", "retweeted_id", "is_quote_tweet", "quoted_id", "timestamp"])

	for line_number,line in enumerate(input_file):

		tweet = Tweet(line)
		csv_writer.writerow(tweet.values())

		if line_number % checkpoint_value == 0:
			print "CHECKPOINT (line " + str(line_number) + ")"

		tweet_count = line_number

print "\nComplete: processed " + str(tweet_count) + " tweets"

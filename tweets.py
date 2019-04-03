import os
import csv
from classes import Tweet
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_filename",
					help="JSONL filename to read in", metavar="INPUT", default=None)
parser.add_argument("-o", "--output", dest="output_filename",
					help="CSV filename to write out", metavar="OUTPUT", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
			help="How often to declare progress", metavar="CHECKPOINT", default=100000)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_filename is None or os.path.splitext(args.input_filename)[1] != ".jsonl":
	print "ERROR: no valid input JSONL file declared.\nAborting..."
	quit()

# INITIALISE REQUIRED VALUES
input_filename = args.input_filename
base_filename = os.path.splitext(args.input_filename)[0]
output_filename = "output-" + base_filename + ".csv" if args.output_file is None else args.output_file
checkpoint_value = args.checkpoint_index

print "\nExecuting: tweets.py"
print "==> Parsing tweets from: " + input_filename
print "==> Outputting values to: " + output_filename
print "\n"

with open(args.input_file, "r") as input_file, open(output_filename, "w+") as output_file:

	csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["id", "tweet", "likes", "retweets", "temperature", "volume", "timestamp"])

	for line_number,line in enumerate(input_file):

		tweet = Tweet(line)
		csv_writer.writerow(tweet.values())

		if line_number % checkpoint_value == 0:
			print "CHECKPOINT (line " + str(line_number) + ")"

print "\nCSV conversion complete\n"

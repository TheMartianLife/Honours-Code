import os
from classes import Tweet, FileComponents
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("-t", "--tweets", dest="tweets_filename",
					help="JSONL filename to read in", metavar="TWEETS", default=None)
parser.add_argument("-i", "--ids", dest="ids_filename",
						help="TXT filename to check fetch against", metavar="IDS", default=None)
parser.add_argument("-o", "--output", dest="output_filename",
					help="TXT filename to write out", metavar="OUTPUT", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
				help="How often to declare progress", metavar="CHECKPOINT", default=100000, type=int)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
base_file = FileComponents(args.tweets_filename)
if args.tweets_filename is None or base_file.extension != ".jsonl":
	print "ERROR: no valid input JSONL file declared.\nAborting..."
	quit()

# INITIALISE REQUIRED VALUES
tweets_filename = args.tweets_filename
ids_filename = base_file.path + base_file.name + ".txt" if args.ids_filename is None else args.ids_filename
output_filename = base_file.path + "missed-" + base_file.name + ".txt" if args.output_filename is None else args.output_filename
checkpoint_value = args.checkpoint_index
missed_count = 0

print "\nExecuting: missed-ids.py"
print "==> Checking tweets from: " + tweets_filename
print "==> Comparing tweet ids from: " + ids_filename
print "==> Outputting missed ids to: " + output_filename
print "\n"

# EXECUTE
with open(tweets_filename, "r") as tweets_file, open(ids_filename, "r") as ids_file, open(output_filename, "w+") as output_file:

	fetched_tweet_ids = [Tweet(line).id for line in tweets_file]

	for line_number, line in enumerate(ids_file):
		id = int(line.rstrip())

		if id not in fetched_tweet_ids:
			missed_count += 1
			output_file.write(line)

		if line_number % checkpoint_value == 0:
			print "CHECKPOINT (line " + str(line_number) + ")"

print "\nComplete: found " + str(missed_count) + " missed ids"
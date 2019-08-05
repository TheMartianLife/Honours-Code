import os
import json
import codecs
import secrets
import logging
from classes import FileComponents
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("input_filename", metavar="INPUT_FILE", type=str,
					help="TXT filename to read in", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
					help="How often to declare progress", metavar="CHECKPOINT", default=50000, type=int)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_filename is None:
	print("ERROR: no input file declared.\nAborting...")
	quit()

base_file = FileComponents(args.input_filename)

if base_file.extension != ".txt":
	print("ERROR: input file must be valid TXT file.\nAborting...")
	quit()

# INITIALISE REQUIRED VALUES
input_filename = args.input_filename
missed_filename = base_file.path + "missed-" + base_file.name + ".txt"
output_filename = base_file.path + base_file.name + ".jsonl"
split_destination = base_file.path + base_file.name + "/"
split_filenames = split_destination + base_file.name

# SETUP TWARC AND LOGGING OBJECTS
log = logging.getLogger('twarc')
logging.basicConfig(
	filename=base_file.path + "twarc.log",
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(message)s"
)
twarc = secrets.initialised_twarc_object()

if args.checkpoint_index >= 100:
	checkpoint_value = args.checkpoint_index
else:
	print("Checkpoint value must be 100 or more to prevent wasted API calls, defaulting to 100.")
	checkpoint_value = 100

print("\nExecuting: hydrate.py")
print("==> Requesting tweet ids from: %s" % input_filename)
print("==> Outputting fetched tweets to: %s" % output_filename)
print("\n")

# DEFINE LINES GENERATOR FUNCTION
def lines(input_file, n):
	for i in range(0, len(input_file), n):
		yield input_file[i: i + n]

# SPLITTING INPUT FILE INTO MULTIPLE FILES
split_input_filenames = []
total_ids = 0
total_files = 0
with open(input_filename, "r") as input_file:

	try:
		os.makedirs(split_destination)
	except OSError:
		if not os.path.isdir(split_destination):
			raise

	unique_ids = list(set(input_file))
	total_ids = len(unique_ids)
	for index, lines in enumerate(lines(unique_ids, checkpoint_value)):
		new_filename = split_filenames + "-" + str(index + 1) + ".txt"
		split_input_filenames.append(new_filename)
		with open(new_filename, "w+") as new_file:
			new_file.write('\n'.join(lines))

	total_files = len(split_input_filenames)

print("Split input into " + str(total_files) + " files...")

# DEFINE IDS GENERATOR FUNCTION
def ids(ids_list):
    for id in ids_list:
        yield id

iterator = 0

for file_index, split_input_filename in enumerate(split_input_filenames):

	# LOAD IDS INTO MEMORY
	split_input_file = open(split_input_filename, "r")
	ids_list = list(split_input_file)
	missed_ids = set(ids_list)
	split_input_file.close()
	print("Loaded new ids into memory...")

	with open(missed_filename, "a+") as missed_file, open(output_filename, "a+") as output_file:

		for tweet in twarc.hydrate(ids(ids_list)):
			iterator += 1

			if 'id_str' in tweet: # check if valid tweet
				output_file.write(json.dumps(tweet) + '\n')
				missed_ids.discard(tweet['id_str'])

		missed_file.write('\n'.join(missed_ids))

	print("Attempted hydration of batch %d / %d complete (%d tweets fetched)..." % (file_index + 1, total_files, iterator))
	os.remove(split_input_filename) # delete intermediate input file

os.rmdir(split_destination) # delete folder created for intermediate files
print("\nComplete: hydrated %d / %d Tweet ids" % (iterator, total_ids))

import os
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_filename",
					help="TXT filename to read in", metavar="INPUT")
parser.add_argument("-o", "--output", dest="output_destination",
					help="Where to write out created TXT files", metavar="OUTPUT", default=None)
parser.add_argument("-s", "--split", dest="split_index",
			help="How often to start a new file", metavar="SPLIT", default=500000)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
		help="How often to declare progress", metavar="CHECKPOINT", default=100000)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_filename is None or os.path.splitext(args.input_filename)[1] != ".txt":
	print "ERROR: no valid input TXT file declared.\nAborting..."
	quit()

# INITIALISE REQUIRED VALUES
base_filepath = os.path.basename(args.input_filename)
base_filename = os.path.splitext(base_filepath)[0]
input_filename = args.input_filename
output_destination = os.path.dirname(args.input_filename) + "/" + base_filename + "/" if args.output_destination is None else args.output_destination
output_filenames = output_destination + base_filename
split_value = args.split_index
checkpoint_value = args.checkpoint_index
file_count = 0

print "\nExecuting: missed-ids.py"
print "==> Getting ids from: " + input_filename
print "==> Splitting into groups of: " + str(split_value)
print "==> Outputting ids to: " + output_filenames + "1.txt and onward"
print "\n"

# EXECUTE
with open(input_filename, "r") as input_file:

	try:
		os.makedirs(output_destination)
	except OSError:
		if not os.path.isdir(output_destination):
			raise

	for line_number, line in enumerate(input_file):

		if line_number % split_value == 0:
			file_count += 1
			output_filename = output_filenames + str(file_count) + ".txt"
			output_file = open(output_filename, "w+")

		output_file.write(line)

		if line_number % checkpoint_value == 0:
			print "CHECKPOINT (line " + str(line_number) + ")"

print "\nComplete: split into " + str(file_count) + " files"
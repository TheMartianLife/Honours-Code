import os
import csv
from classes import FileComponents
from argparse import ArgumentParser

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument(dest="input_filename", metavar="INPUT_FILE", type=str,
                    help="CSV filename to read in", default=None)
parser.add_argument("-c", "--checkpoint", dest="checkpoint_index",
                    help="How often to declare progress", metavar="CHECKPOINT", default=50000, type=int)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_filename is None:
    print("ERROR: no input file declared.\nAborting...")
    quit()

base_file = FileComponents(args.input_filename)

if base_file.extension != ".csv":
    print("ERROR: input file must be valid CSV file.\nAborting...")
    quit()

# INITIALISE REQUIRED VALUES
input_filename = args.input_filename
output_directory = base_file.path + base_file.name
output_filename = output_directory + "/" + base_file.name
checkpoint_value = args.checkpoint_index

# MAKE OUTPUT DIRECTORY
try:
    os.makedirs(output_directory)
except OSError:
    if not os.path.isdir(output_directory):
        raise

print("\nExecuting: collate.py")
print("==> Getting ids from: " + input_filename)
print("==> Splitting into groups by date")
print("==> Outputting ids to: " + output_filename + "-<date>.csv files")
print("\n")

# EXECUTE
with open(input_filename, "r") as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    next(csv_reader, None)
    input_lines = list(csv_reader)
    total_tweets = len(input_lines)
    total_batches = total_tweets / checkpoint_value

    output_files = {}

    for line_number, line in enumerate(input_lines):
        date = line[5][0:10]

        if date not in output_files:
            output_files[date] = open(output_filename + "-" + date + ".csv","a+")

        output_file = output_files[date]
        output_file.write(",".join(line) + '\n')

        if line_number % checkpoint_value == 0:
            batch_num = line_number / checkpoint_value
            print("Sorting of batch %d / %d complete (%d tweets sorted)..." % (batch_num, total_batches, line_number))


for file_handle in output_files.keys():
    output_files[file_handle].close()

print("\nComplete: split " + str(total_tweets) + " tweets among " + str(len(output_files.keys())) + " files")

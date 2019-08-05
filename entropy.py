import csv, math, numpy, glob
from classes import FileComponents
from argparse import ArgumentParser

def range(x, axis=0):
    return int(numpy.max(x, axis=axis) - numpy.min(x, axis=axis))

def shannon_entropy(s):
    counts = numpy.bincount(s)
    n = float(len(s))
    entropy = 0.0
    for i in counts:
    	p_i = i / n
    	if p_i > 0.0:
            entropy += p_i * math.log(p_i)
    return -entropy

# PARSE COMMAND LINE ARGUMENTS
parser = ArgumentParser()
parser.add_argument(dest="input_directory", metavar="INPUT_FILE", type=str,
                    help="Directory of CSV files to read in", default=None)
args = parser.parse_args()

# TEST COMMAND LINE ARGUMENTS
if args.input_directory is None:
    print("ERROR: no input directory declared.\nAborting...")
    quit()

input_files = sorted(glob.glob(args.input_directory + '/*.csv'))

output_filename = "entropy.csv"
output_file = open(args.input_directory + '/' + output_filename, 'w+')
output_file.write("date,daily_likes,daily_upper_bound,daily_lower_bound,daily_range,daily_entropy,daily_observations,cumulative_likes,overall_upper_bound,overall_lower_bound,overall_range,overall_entropy,overall_observations" + '\n')
overall_likes = []

def csv_values(likes_batch):

	if len(likes_batch) <= 0:
		# Note: this should never happen
		# because why would the last script have
		# created an empty file, but just in case
		return "None,None,None,None,None,None"

	upper_bound = max(likes_batch)
	lower_bound = min(likes_batch)
	batch_range = upper_bound - lower_bound
	entropy = shannon_entropy(likes_batch)
	total = int(numpy.sum(likes_batch))
	count = len(likes_batch)
	return "%d,%d,%d,%d,%.6f,%d" % (total, upper_bound, lower_bound, batch_range, entropy, count)


for input_filepath in input_files:
	input_file = open(input_filepath, 'r')
	input_filename = FileComponents(input_filepath).name

	csv_reader = csv.reader(input_file, delimiter=',')
	likes = [float(row[1]) for row in csv_reader]
	overall_likes += likes

	date = input_filename[-10:]
	batch_values = csv_values(likes)
	cumulative_values = csv_values(overall_likes)

	print("Calculated entropy for %s" % date)

	output_file.write(date + "," + batch_values + "," + cumulative_values + '\n')

	input_file.close()

output_file.close()

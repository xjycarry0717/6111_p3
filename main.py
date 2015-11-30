import sys
from apriori import *


def main(argv):
	# parse input arguments
	filename = sys.argv[1]
	minsupp = float(sys.argv[2])
	minconf = float(sys.argv[3])
	data = apriori(filename, minsupp, minconf)
	data.run()


if __name__ == '__main__':
	main(sys.argv[1:3])
from parameters import *
import os
#import pdb

"""
TODO: Create checkpoint for processing sequences --> so no duplicates in processed file!
"""

file_start_name = "data"

def process_sequences(submission="submission.txt", chunk15=True, extend=False):

	check_point_file = open(directory_name+"/check_point.txt", "r")
	check_point= int(check_point_file.readline())
	print(check_point)
	check_point_file.close()

	batch_files= []
	for i in os.listdir(directory_name):
		if i.startswith(file_start_name):
			batch_files.append(i)

	#pdb.set_trace()
	for batch in batch_files:
		# assumes batches numbered as "data0.fasta", "data1.fasta", etc., can change
		datafile=directory_name+"/"+batch

		# merges each paragraph into a single line
		readfile = open(datafile).readlines()
		for n,line in enumerate(readfile):
			# separate new protein with whitespace
			if line.startswith(">"):
				readfile[n] = "\n\n" + line
			# if part of sequence, strips the whitespace
			else:
				readfile[n] = line.rstrip()

		# saves data processed from above
		data = ''.join(readfile)
		with open(directory_name+"/processed.txt", 'a+') as writefile:
			writefile.write(data)
			print("Processed", datafile)
	if chunk15:
		processchunk15(extend)


def processchunk15(extend=False):
	# writes data in chunks of 15, skipping over 5 each time
	data = open(directory_name+"/processed.txt", 'r')
	with open(directory_name+"/submission.txt", 'w') as writefile:
		for line in data:
			llen = len(line)
			if llen == 0:
				writefile.write("")
			elif line.startswith(">"):
				writefile.write(line)
			# cuts into chunks of 15
			else:
				for i in range(0, llen-10, 5):
					if extend and i+18 > llen:
						writefile.write(line[i:] + "\n")
						break
					writefile.write(line[i:i+15] + "\n")


def main():
	process_sequences()

if __name__ == "__main__":
	main()

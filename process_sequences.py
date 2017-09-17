import os
#import pdb

"""
TODO: Create checkpoint for processing sequences --> so no duplicates in processed file!
"""

def process_sequences(dir_name="data/data.fasta", post1="processed.txt", post2="processed15.txt", chunk15=True, extend=False):

	"""
	Formats FASTA file to display sequences on one line or 15 molecules per line

	ARGUMENTS
	dir: directory of FASTA-format file
	chunk15: whether to split into amino acid sequences chunks of 15 with stride 5
	
	RETURNS
	None
	"""

	# # prints out checkpoint
	# check_point_file = open(directory_name, "r")
	# check_point= int(check_point_file.readline())
	# print(check_point)
	# check_point_file.close()

	#pdb.set_trace()
	dir_folder, _ = os.path.split(dir_name)
	datafile = dir_name

	# merges each paragraph into a single line
	readfile = open(datafile).readlines()
	for n,line in enumerate(readfile):
		# separate new protein with whitespace
		if line.startswith(">"):
			line.replace(" ", "")		# removes all whitespace in id
			readfile[n] = "\n\n" + line
		# if part of sequence, strips the whitespace
		else:
			readfile[n] = line.rstrip()

	# saves data processed from above		
	data = ''.join(readfile)
	with open(dir_folder+"/"+post1, 'a+') as writefile:
		writefile.write(data)
		print("Processed", datafile)

	if chunk15:
		processchunk15(dir_folder, post1, post2, extend)


def processchunk15(dir_folder="data", post1="processed.txt", post2="processed15.txt", extend=False):

	# writes data in chunks of 15, skipping over 5 each time
	data = open(dir_folder+"/"+post1, 'r')
	with open(dir_folder+"/"+post2, 'w') as writefile:
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

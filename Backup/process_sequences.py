batch_size=10
directory_name="data.fasta"

def process_sequences(submission="submission.txt", chunk15=False, extend=False):

	check_point_file = open(directory_name+"/check_point.txt", "r")
	check_point= int(check_point_file.readline())
	print(check_point)
	check_point_file.close()
	
	for batch_num in range(0, check_point//batch_size):
		# assumes batches numbered as "data0.fasta", "data1.fasta", etc., can change
		datafile=directory_name+"/data"+str(batch_num)+".fasta"

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
	data = open("processed.txt", 'r')
	with open("submission.txt", 'w') as writefile:
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
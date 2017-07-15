from Bio import Entrez
from time import sleep
Entrez.email = "hyun9@ucla.edu" 
#searching

webenv=""
query_key=""
database="protein"
parameter="WecB/TagA/CpsF AND membrane"
retmode="text"
datafile="data.fasta"
max_count=100
batch_size=10
out_handle=open(datafile,"w")
id_list=[]

def search():
	print("Searching with parameter \"%s\" in %s database for a maximum of %d ids" % (parameter, database, max_count));
	handle = Entrez.esearch(db=database, term=parameter, idtype="acc",retmax=max_count)
	record=Entrez.read(handle)
	count=int(record["Count"])
	global webenv, query_key, id_list 
	id_list=record["IdList"]
	#print("IDs to obtain: ", id_list)
	search_results = Entrez.read(Entrez.epost("protein", id=",".join(id_list)))
	webenv = search_results["WebEnv"]
	query_key = search_results["QueryKey"]
	#print("Search result is %s" % search_results)

from urllib.error import HTTPError  

def fetch_individual(start, end):
	for num in range(start, end+1, 1):
		print("Going to download record %i individually" % num)
		failure=0
		try:
			fetch_handle = Entrez.efetch(db="protein", rettype="fasta", retmode=retmode,
										retstart=start, retmax=1,
										webenv=webenv, query_key=query_key,
										idtype="acc")
		except HTTPError as err:
			if 500 <= err.code <= 599:
				print("Received error from server %s" % err)
				print("Attempt %i of 3" % attempt)
				sleep(10)
			else:
				print("Failed to download %s individually" % id_list[num])
				failure=1
		if(not failure):
			data = fetch_handle.read()
			fetch_handle.close()
			out_handle.write(data)

def fetch():
	for start in range(0, max_count, batch_size):
		end = min(max_count, start+batch_size)
		print("Going to download record %i to %i" % (start+1, end))
		attempt = 0
		failure = 0
		while attempt < 3:
			attempt += 1
			try:
				fetch_handle = Entrez.efetch(db="protein",
				rettype="fasta", retmode=retmode,
				retstart=start, retmax=batch_size,
				webenv=webenv, query_key=query_key,
				idtype="acc")
			except HTTPError as err:
				print("Got exception")
				if 500 <= err.code <= 599:
					print("Received error from server %s" % err)
					print("Attempt %i of 3" % attempt)
					sleep(10)
				else:
					failure=1
					fetch_individual(start+1,end)
					break;
		if(not failure):
			data = fetch_handle.read()
			fetch_handle.close()
			out_handle.write(data)

def process():
	datafile="data.fasta"
submission="submission.txt"
	readfile = open(datafile).readlines()
	for n,line in enumerate(readfile):
		if line is "":
			data[n] = "\n"
		if line.startswith(">"):
			start = 1
			readfile[n] = "\n"
		else if line is not "":
			data[n] = line.rstrip()


	with open("submission.txt", 'w') as writefile:
		for line in readfile:
			if len(line) == 0:
				writefile.write("")

			if line.startswith(">"):
				writefile.write(line)

			else:
				for i in range(0, len(line)-15, 5):
					writefile.write(line[i:i+15])
					if i + 15 > len(line):
						writefile.write(line[i:])


def process():
	datafile="data.fasta"
	submission="submission.txt"
	extend = False
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
	with open("processed.txt", 'w') as writefile:
		writefile.write(data)
	data = open("processed.txt", 'r')

	# writes data in chunks of 15, skipping over 5 each time
	with open("submission.txt", 'w') as writefile:
		for line in data:
			llen = len(line)
			if llen == 0:
				writefile.write("")
			elif line.startswith(">"):
				writefile.write(line)
			else:
				for i in range(0, llen-10, 5):
					if extend and i+18 > llen:
						writefile.write(line[i:] + "\n")
						break
					writefile.write(line[i:i+15] + "\n")


def main():
	search()
	fetch()
	process()


if __name__ == "__main__":
	main()
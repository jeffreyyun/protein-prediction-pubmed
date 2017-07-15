from Bio import Entrez
from time import sleep
Entrez.email = "jenniezheng321@gmail.com" 
#searching

webenv=""
query_key=""
max_count=100
database="protein"
parameter="WecB/TagA/CpsF AND membrane"
batch_size=10
out_handle=open("data.fasta","w")
id_list=[]

def search():
	print("Searching with parameter %s in %s database for a maximum of %d ids" % (parameter, database, max_count));
	handle = Entrez.esearch(db=database, term=parameter, idtype="acc",retmax=max_count)
	record=Entrez.read(handle)
	count=int(record["Count"])
	global webenv, query_key, id_list 
	id_list=record["IdList"]
	print("IDs to obtain: ", id_list)
	search_results = Entrez.read(Entrez.epost("protein", id=",".join(id_list)))
	webenv = search_results["WebEnv"]
	query_key = search_results["QueryKey"]
	print("Search result is %s" % search_results)

from urllib.error import HTTPError  

def fetch_individual(start, end):
	for num in range(start, end+1, 1):
		print("Going to download record %i individually" % num)
		failure=0
		try:
			fetch_handle = Entrez.efetch(db="protein", rettype="fasta", retmode="text",
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
				rettype="fasta", retmode="text",
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



def main():
	search()
	fetch()
	process()


if __name__ == "__main__":
	main()
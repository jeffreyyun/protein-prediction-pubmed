from Bio import Entrez
from time import sleep
from urllib.error import HTTPError  
import sys
import os

Entrez.email = "jenniezheng321@gmail.com" 

#upper bound ~ 500000 entries
max_count=30
batch_size=3
database="protein"
parameter="all[filter]"

directory_name="default"
webenv=""
query_key=""
id_list=[]
check_point_start=0
list_file_data=[]

def process_arguments():
	if(len(sys.argv)!=2):
		print("Usage: python3 fetcher.py PROJECT_DIRECTORY_NAME")
		exit(1)
	global directory_name
	directory_name=str(sys.argv[1])


def process_check_point():
	try:
		os.stat(directory_name)
	except:
		os.mkdir(directory_name)
		return False
	try:
		list_file = open(directory_name+"/id_list.txt", "r+")
		global start, id_list,check_point_start, list_file_data
		id_list=list_file.readline().split(',')
		check_point_file = open(directory_name+"/check_point.txt", "r+")
		check_point_start=int(check_point_file.readline())
		return True
	except:
		return False
	

#only done if no checkpoint set! 
def collect_ids(): 
	global max_count;
	print("Searching with parameter %s in %s database for a maximum of %d ids" % (parameter, database, max_count));
	handle = Entrez.esearch(db=database, term=parameter, idtype="acc",retmax=max_count)
	print("Passed")
	record=Entrez.read(handle)
	max_count=min(int(record["Count"]),max_count)
	global id_list
	id_list=record["IdList"]
	list_file=open(directory_name+"/id_list.txt","w")
	list_file.write(",".join(id_list))
	check_point_file = open(directory_name+"/check_point.txt", "w")
	check_point_file.write(str(0))
	print("Checkpoint of %d id's saved." % max_count)

#always done
def conduct_websearch():
	global webenv, query_key
	print(id_list[check_point_start:])
	print("Obtaining id's from %s to %s" % (id_list[check_point_start], id_list[len(id_list)-1]))
	search_results = Entrez.read(Entrez.epost("protein", id=",".join(id_list[check_point_start:])))
	webenv = search_results["WebEnv"]
	query_key = search_results["QueryKey"]
	print("Search result is %s" % search_results)


def fetch_data():
	global check_point_start, list_file_data
	check_point_file = open(directory_name+"/check_point.txt", "w")
	fetch_handle = 0

	try:
		for start in range(check_point_start, max_count, batch_size):
			out_handle=open(directory_name+"/data"+str(start//batch_size)+".fasta","w")
			end = min(max_count, start+batch_size)
			print("Downloading record %i to %i" % (start+1, end))
			attempt = 0
			failure = 0
			while attempt < 3:
				attempt += 1
				try:
					fetch_handle = Entrez.efetch(db="protein",
					rettype="fasta", retmode="text",
					id=",".join(id_list[start:end+1]), retmax=batch_size,
					webenv=webenv, query_key=query_key,
					idtype="acc")
				except HTTPError as err:
					failure=1
					print("Received error from server %s" % err)
					if 500 <= err.code <= 599:
						print("Attempt %i of 3" % attempt)
						sleep(10)
					elif err.code==400:
						print("Attempted to obtain id %s" % id_list[start])
						break;
					else:
						break;
			if(not failure):
				data = fetch_handle.read()
				fetch_handle.close()
				out_handle.write(data)
				out_handle.close()
				check_point_file.seek(0)
				check_point_file.write(str(end))
	except KeyboardInterrupt:
		print("Quiting")
		check_point_file.close()
		sys.exit()



def main():
	process_arguments()
	check_point_exists=process_check_point()
	if(not check_point_exists):
		print("No checkpoint found. Collecting ids.")
		collect_ids()
	elif(check_point_start>=len(id_list)):
		print("Nothing to do. Done.")
		return
	else:
		print("Checkpoint found. Starting at %d out of %d." % (check_point_start, len(id_list)))
	conduct_websearch();
	fetch_data()
	print("Done!")

if __name__ == "__main__":
	main()
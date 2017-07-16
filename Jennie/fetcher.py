from Bio import Entrez
from time import sleep
from urllib.error import HTTPError  
import sys
import os

Entrez.email = "jenniezheng321@gmail.com" 


batch_size=1000
database="protein"
parameter="all[filter]"

directory_name=""
check_point=0

def process_arguments():
	if(len(sys.argv)!=2):
		print("Usage: python3 fetcher.py PROJECT_DIRECTORY_NAME")
		exit(1)
	global directory_name
	directory_name=str(sys.argv[1])

#returns checkpoint
def process_check_point():
	try:
		os.stat(directory_name)
	except:
		os.mkdir(directory_name)
		return 0
	global check_point
	if os.path.isfile(directory_name+"/check_point.txt"):
		check_point_file = open(directory_name+"/check_point.txt", "r")
		check_point= int(check_point_file.readline())
		check_point_file.close()
		return check_point
	else:
		check_point_file = open(directory_name+"/check_point.txt", "w")
		check_point_file.write("0")
		return 0
	

#gets offset and count, returns id list
def collect_ids(offset, count): 
	global database, parameter
	try:
		handle = Entrez.esearch(db=database, retstart=offset, term=parameter, idtype="acc",retmax=count)
	except HTTPError as err:
		print("Received error from server %s" % err)
		sys.exit()
	record=Entrez.read(handle)
	return record["IdList"]

#returns webenv and query key
def conduct_websearch(id_list):
	try:
		search_results = Entrez.read(Entrez.epost("protein", id=",".join(id_list)))
	except HTTPError as err:
		print("Received error from server %s" % err)
		sys.exit()
	webenv = search_results["WebEnv"]
	query_key = search_results["QueryKey"]
	return [webenv,query_key]


def fetch_data(webenv, query_key, id_list, checkpoint):
	out_handle=open(directory_name+"/data"+str(checkpoint)+".fasta","w")
	attempt = 0
	while attempt < 3:
		attempt += 1
		failure = 0
		try:
			fetch_handle = Entrez.efetch(db="protein",
			rettype="fasta", retmode="text",
			id=",".join(id_list), retmax=500000,
			webenv=webenv, query_key=query_key,
			idtype="acc")
		except HTTPError as err:
			failure=1
			print("Received error from server %s" % err)
			if 500 <= err.code <= 599:
				print("Attempt %i of 3" % attempt)
				sleep(15)
	if(not failure):
		data = fetch_handle.read()
		fetch_handle.close()
		out_handle.write(data)
		out_handle.close()
	else:
		print("Failed to recover from error")
		sys.exit()

	


def main():
	global database, parameter
	process_arguments()
	check_point=process_check_point()
	#Preliminary check: 
	try:
		handle = Entrez.esearch(db=database, retstart=check_point, term=parameter, idtype="acc",retmax=5)
	except HTTPError as err:
		print("Received error from server %s" % err)
		sys.exit()
	record=Entrez.read(handle)
	max_count=int(record["Count"])
	while (check_point<max_count):
		try:
			print("Retrieving protein sequence from index %d to %d" % (check_point, check_point+batch_size-1))
			id_list=collect_ids(check_point,batch_size)
			webenv, query=conduct_websearch(id_list)
			fetch_data(webenv, query, id_list, check_point)
			check_point+=len(id_list)
			check_point_file = open(directory_name+"/check_point.txt", "w")
			check_point_file.write(str(check_point))
			check_point_file.close()
		except KeyboardInterrupt:
			print("Quiting")
			sys.exit()
	print("Done!")

if __name__ == "__main__":
	main()
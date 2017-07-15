from Bio import Entrez
from time import sleep
Entrez.email = "jenniezheng321@gmail.com" 
#searching


handle = Entrez.esearch(db="protein", term="all[filter]", idtype="acc")
record=Entrez.read(handle)
count=int(record["Count"])
id_list=record["IdList"]
search_results = Entrez.read(Entrez.epost("protein", id=",".join(id_list)))
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]
failed=[]
print(search_results)

from urllib.error import HTTPError  

batch_size = 5
out_handle = open("data.fasta", "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    failure = 0
    while attempt < 4:
        attempt += 1
        try:
            fetch_handle = Entrez.efetch(db="protein",
                                         rettype="fasta", retmode="text",
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key,
                                         idtype="acc")
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 4" % attempt)
                sleep(10)
            else:
            	failed.append(start)
            	failure=1
    if(not failure):
	    data = fetch_handle.read()
	    fetch_handle.close()
	    out_handle.write(data)
   
out_handle.close()
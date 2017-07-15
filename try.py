from Bio import Entrez
Entrez.email = "jenniezheng321@gmail.com" 
#searching

db = "protein"
search_term = "peripheral membrane protein"
return_amount = 10

handle = Entrez.esearch(db="nucleotide", term="all[filter]", idtype="acc")
record=Entrez.read(handle)
handle.close()

count=int(record["Count"])
id_list=record["IdList"]
idlist=record["IdList"]
print("IDList: ")
print(idlist)

search_results = Entrez.read(Entrez.epost("nucleotide", id=",".join(id_list)))
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]
print(search_results)
from urllib.error import HTTPError  


batch_size = 10
out_handle = open("data.fasta", "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    while attempt < 3:
        attempt += 1
        try:
            fetch_handle = Entrez.efetch(db="nucleotide",
                                         rettype="fasta", retmode="text",
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key,
                                         idtype="acc")
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                time.sleep(15)
            else:
                raise
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
out_handle.close()
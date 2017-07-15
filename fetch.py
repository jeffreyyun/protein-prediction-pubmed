from Bio import Entrez
import time
Entrez.email = "hyun9@ucla.edu"

term="WecB/TagA/CpsF[All Fields]"
db="protein"
batch_size=10

search_handle = Entrez.esearch(db=db, term=term, idtype="acc", retmax=batch_size)
record = Entrez.read(search_handle)
search_handle.close()

id_list = ",".join(record["IdList"])
count = int(record["Count"])

record = Entrez.read(Entrez.epost(db, id_list)

webenv = record["WebEnv"]
query_key = record["QueryKey"]

try:
    from urllib.error import HTTPError  # for Python 3
except ImportError:
    from urllib2 import HTTPError  # for Python 2

batch_size = 3
out_handle = open("data.fasta", "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    while attempt < 5:
        attempt += 1
        try:
            fetch_handle = Entrez.efetch(db=db,
                                         rettype="fasta", retmode="text",
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key,
                                         idtype="acc")
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 5" % attempt)
                time.sleep(5)
            else:
            	print("Attempt %i of 5" % attempt)
            	time.sleep(1)
    data = fetch_handle.read()
    fetch_handle.close()
    out_handle.write(data)
out_handle.close()

"""
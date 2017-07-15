import os
from Bio import Entrez
from Bio import SeqIO
Entrez.email = "hyun9@g.ucla.edu"

db = "protein"
search_term = "peripheral membrane protein"
return_amount = 10

handle = Entrez.esearch(db=db, term=search_term, retmax=return_amount)
record = Entrez.read(handle)
handle.close()
idlist=record["IdList"]
print("IDList: ")
print(idlist)

search_results = Entrez.read(Entrez.epost("nucleotide", id=",".join(id_list)))
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]
print(search_results)


filename = "test.gbk"
if not os.path.isfile(filename):
	net_handle = Entrez.efetch(db="nucleotide", id=idlist, rettype="gb", retmode="text")
	out_handle = open(filename, "w")
	out_handle.write(net_handle.read())
	out_handle.close()
	net_handle.close()
	print("Saved")


print("Parsing...")
record = SeqIO.parse(filename, "gb")
for seq_record in record:
	print(repr(record.id))
	print(repr(record.translation))
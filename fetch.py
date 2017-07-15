import os
from Bio import Entrez
from Bio import SeqIO
Entrez.email = "hyun9@g.ucla.edu"

handle = Entrez.esearch(db="nucleotide", term="all", retmax=10)
record = Entrez.read(handle)
handle.close()
idlist=record["IdList"]
print("IDList: ")
print(idlist)

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
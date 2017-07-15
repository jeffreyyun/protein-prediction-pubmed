from Bio import Entrez
Entrez.email = "jenniezheng321@gmail.com" 
handle = handle = Entrez.esearch(db="nucleotide", term="all[filter]", idtype="acc")
record=Entrez.read(handle)
print(record["Count"])
print(record["IdList"])

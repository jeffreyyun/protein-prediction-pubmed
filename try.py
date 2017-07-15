from Bio import Entrez
Entrez.email = "jenniezheng321@gmail.com" 
#searching
handle = Entrez.esearch(db="nucleotide", term="all[filter]", idtype="acc")
record=Entrez.read(handle)
count=record["Count"]
id_list=record["IdList"]

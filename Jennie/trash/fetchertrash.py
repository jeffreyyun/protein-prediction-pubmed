"""
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
"""
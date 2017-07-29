push: 
	git pull
	git add fetcher.py process_sequences.py data
	git commit -am "fix directory"
	git push origin master

push: 
	git pull
	git rm -r --cached .
	git add README.md
	git add fetcher.py process_sequences.py parameters.py
	git add HelicalWheel_files HelicalWheel.html 
	git add data
	git commit -am "helical wheel"
	git push origin master

script=main.py
while true; do
    python3 $script;
    #wait for changes to script
    inotifywait -qe modify $script >> /dev/null;
done
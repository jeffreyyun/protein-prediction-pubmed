
def svm():
    #process_arguments()
    check_point=process_check_point()
    #Preliminary check:
    try:
        handle = Entrez.esearch(db=db, retstart=check_point, term=term, idtype="acc",retmax=5)
    except HTTPError as err:
        print("Received error from server %s" % err)
        sys.exit()
    record=Entrez.read(handle)
    max_count=int(record["Count"])
    while (check_point<max_count):
        try:
            print("Retrieving protein sequence from index %d to %d" % (check_point, check_point+batch_size-1))
            id_list=collect_ids(check_point,batch_size)
            webenv, query=conduct_websearch(id_list)
            file_name=fetch_data(webenv, query, id_list, check_point)
            process_sequences(file_name)
            check_point+=len(id_list)
            check_point_file = open(directory_name+"/check_point.txt", "w")
            check_point_file.write(str(check_point))
            check_point_file.close()
        except KeyboardInterrupt:
            print("Quiting")
            sys.exit()
    print("Done!")

if __name__ == "__main__":
    main()

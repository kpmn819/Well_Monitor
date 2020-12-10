#------------------------- UPDATE_RUN1 ----------------------
# does all the major database work table seq1 has the individual runs and seq100 stores the averages
def update_run1(run_time):
    #print("Update Run1 Table Here")
    global seq_no
    seq_interval = 15 # this is the trigger to summarize and add to run100 becomes 110
    seq_replace = 5 # number of records to replace then renumber the upper group becomes 10
    
    now = datetime.now()
    formatted_date = now.strftime('%y-%m-%d %H:%M:%S')
    formatted_date = sql_access.add_quotes(formatted_date)
     
    q= ("SELECT MAX(seq1) FROM run1")
    #print (q)
    seq_max = sql_access.raw_sql_read(q)
    seq_no = seq_max[0] + 1
    #print("seq_no = " + str(seq_no))
    q= ("INSERT INTO run1(event_time,run_time,seq1) VALUES({},{},{})").format(formatted_date,run_time,seq_no)
    
    sql_access.raw_sql_write(q)
    
    if seq_no == seq_interval:# here we do the data shuffle get the average, delete lower group, renumber upper group, save averages
        # get average of lower group
        q = ("SELECT AVG(run_time) FROM run1 WHERE seq1 < {}").format(seq_interval + 1)
        #print(q)
        seq_a = sql_access.raw_sql_read(q) # this is just a quick place to store the tuple that is returned
        seq_average = seq_a[0] # the sql_read returns a tuple in the form of (data, ) must extract [0] element
        seq_average = round(seq_average,1)
        print("Last Sequence Average Was: ",seq_average)
        # delete lower group
        q = ("DELETE FROM run1 WHERE seq1 < {}").format(seq_replace + 1)
        sql_access.raw_sql_write(q)
        # renumber upper group
        q = ("UPDATE run1 SET seq1 = seq1 - {}").format(seq_replace)
        sql_access.raw_sql_write(q)
        # save average in run100
        q= ("SELECT MAX(seq100) FROM run100")
        #print (q)
        seq_max100 = sql_access.raw_sql_read(q)
        seq_maxadd = seq_max100[0] + seq_replace
        q = ("INSERT INTO run100(avg_time,end_time,seq100) VALUES({},{},{})").format(seq_average,formatted_date,seq_maxadd)
        #print("sql is " + str(q))
        sql_access.raw_sql_write(q)
        #                tables
        # run1      cols = event_time, run_time, seq1
        # run100    c

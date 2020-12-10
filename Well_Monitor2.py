# General info
# operators <,>,==,<=,>=,!=
# data types
#   Tuple_1 = (1,15,3) a list that cannot be changed read access Tuple_1[0]
#   List_1 = [1,15,3] append, pop, insert, sort, extend
#   Dictionary_1 = {"Joe":"Joe Blow","Jim":"Jim Crow"}

# Import Stuff Here

import time
from datetime import datetime
import json
import sql_access
import smtplib
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


# Define Stuff Here
w_log = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]# placeholders
# really need to go to db and get the last 10 entries in case of power outage

something_else=0 # Top level variable can be used as global
t_max = 50 # number of seconds before excess time trigger
w_overrun = 3 # number of times it will retry
seq_no = 0 # set on start up to 0 lets update_run1 know it's a fresh start
# allow entry of seq_interval, should really have code to protect errors but well....
seq_interval = int(input("Enter the interval for averages: "))



def myfunction(something):
    global something_else # referance variable outside function
    something_else = something * 7
    
    return something

def make_json(w_log):# pass the 10 most recent events to encode for JSON
    # The idea here is to make a file that the web server can use to display our log
    # now need to iterate through the list and make a dictionary
    

# I know this code sucks but in order to get the stuff in the proper order
# so it could be encoded to json this works
    data = {}
    
    data["Time0"] = {
        "Time":str(w_log[0][0]),
        "Run_Time":str(w_log[0][1])
        }
    data["Time1"] = {
        "Time":str(w_log[1][0]),
        "Run_Time":str(w_log[1][1])
        }
    data["Time2"] = {
        "Time":str(w_log[2][0]),
        "Run_Time":str(w_log[2][1])
        }
    data["Time3"] = {
        "Time":str(w_log[3][0]),
        "Run_Time":str(w_log[2][1])
        }
    data["Time4"] = {
        "Time":str(w_log[4][0]),
        "Run_Time":str(w_log[4][1])
        }
    data["Time5"] = {
        "Time":str(w_log[5][0]),
        "Run_Time":str(w_log[5][1])
        }
    data["Time6"] = {
        "Time":str(w_log[6][0]),
        "Run_Time":str(w_log[6][1])
        }
    data["Time7"] = {
        "Time":str(w_log[7][0]),
        "Run_Time":str(w_log[7][1])
        }
    data["Time8"] = {
        "Time":str(w_log[8][0]),
        "Run_Time":str(w_log[8][1])
        }
    data["Time9"] = {
        "Time":str(w_log[9][0]),
        "Run_Time":str(w_log[9][1])
        }
    #print(data)
    

    with open('log.json', 'w') as outfile: #save the json file
        json.dump(data, outfile)
    print("json Data encoded and saved to file")
    j_log = data

    return j_log

class Port(): #Capatilize Classes
    ''' This is a docstring for this class '''
    def __init__(self,pnum,ptype,pstat):
        self.pnum = pnum #port number
        self.ptype = ptype #input or output
        self.pstat = pstat #true (high) false (low)
        
    def set_type(self):# sets port as input or output
        if self.ptype == "input":
            GPIO.setup(self.pnum, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        else:
            GPIO.setup(self.pnum,GPIO.OUT)
            GPIO.output(self.pnum, GPIO.HIGH)
            self.pstat = 1
        
    def read_port(self): # check an input port
        if self.ptype == "input":
            self.pstat = GPIO.input(self.pnum)
            
        else:
            pass
            
 
    def change_stat(self):# toggle an output port
        if self.ptype == "output":
            if self.pstat == 1:
                self.pstat = 0
                GPIO.output(self.pnum, GPIO.LOW)
            else:
                self.pstat = 1
                GPIO.output(self.pnum, GPIO.HIGH)
        else:
            pass

#------------------- send_mail text message  -----------------------------------
def send_mail(message): #the texting portion
    TO= "2488778790@vtext.com" #all of the credentials
    GMAIL_USER="roufeshound@gmail.com"
    PASS= 'caesiopkckblufyd'
    SUBJECT = 'Alert!'

    print("Sending text")
    TEXT = message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print(header)
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(GMAIL_USER,TO,msg)
    server.quit()
    time.sleep(1)
    print("Text sent")

#-----------------------------------------------------------

#------------------------- UPDATE_RUN1 ----------------------
# does all the major database work table seq1 has the individual runs and seq100 stores the averages
def update_run1(run_time):
    
    global seq_no
    global seq_interval # this is the trigger to get the average
    
    
    now = datetime.now()
    formatted_date = now.strftime('%y-%m-%d %H:%M:%S')
    formatted_date = sql_access.add_quotes(formatted_date)
     
    q= ("SELECT MAX(seq1) FROM run1")
    
    seq_max = sql_access.raw_sql_read(q)
    seq_no = seq_max[0] + 1
    
    q= ("INSERT INTO run1(event_time,run_time,seq1) VALUES({},{},{})").format(formatted_date,run_time,seq_no)
    
    sql_access.raw_sql_write(q)
    
    if seq_no == seq_interval + 1:# here we do the data shuffle get the average, delete all but one, add average to run100
        # get average of lower group
        q = ("SELECT AVG(run_time) FROM run1 WHERE seq1 >0 AND seq1 < {}").format(seq_interval + 1)
        
        seq_a = sql_access.raw_sql_read(q) # this is just a quick place to store the tuple that is returned
        seq_average = seq_a[0] # the sql_read returns a tuple in the form of (data, ) must extract [0] element
        seq_average = round(seq_average,1)
        print("-------------Last Sequence Average Was: ",seq_average)
        
        # delete all but the last one
        q = ("DELETE FROM run1 WHERE seq1 > 0 AND seq1 < {}").format(seq_interval + 1)
        sql_access.raw_sql_write(q)
        # renumber becomes run number 1 of the next group
        q = ("UPDATE run1 SET seq1 = seq1 - {}").format(seq_interval)
        sql_access.raw_sql_write(q)
        
        # save average in run100
        q= ("SELECT MAX(seq100) FROM run100")
        
        seq_max100 = sql_access.raw_sql_read(q)
        seq_maxadd = seq_max100[0] + seq_interval
        q = ("INSERT INTO run100(avg_time,end_time,seq100) VALUES({},{},{})").format(seq_average,formatted_date,seq_maxadd)
        
        sql_access.raw_sql_write(q)
        #                tables
        # run1      cols = event_time, run_time, seq1
        # run100    cols = event_time, avg_time, seq100

        
#---------------------- INITIALIZE PORTS -----------------------------
w_run = Port(17,'input',1) # low well is running
w_run.set_type()
w_lamp = Port(12,'output',1)# low well is running
w_lamp.set_type()
w_reset = Port(6,'input',1)# will be used as a reset from an overrun condition
w_reset.set_type()
w_power = Port(19,'output',1)# to be used to change the state of a ss relay to kill pump power
w_power.set_type()
wm_stat = Port(13,'output',1)# flashes to indicate pgm running
wm_stat.set_type()
wr_stat = Port(20,'output',1)# flashes to indicate pgm sees well running
wr_stat.set_type()
wr_over = Port(16,'output',1)# well has reached overrun time
wr_over.set_type()
#----------------- END PORT INITIALIZE -----------------------------------




# ------------------ MAIN PROGRAM -----------------------
#--------------------------------------------------------

def main(): # The actual main program
    
    print("Main Well Monitor Loop Running")
    
    
# ------------------ INITIALIZE START ---------------------    







#-------------------- INITIALIZE END --------------------------------
    
# -------------------  OPERATIONAL MAIN CODE ----------------    
    
    while w_run.pstat == 1: #check well every second for start
        time.sleep(1)
        wm_stat.change_stat() # flash led
        w_run.read_port()

        
#<<<<<<<<<<<< well is on >>>>>>>>>>>>>>>>>>
    print("Well is on")
    if wm_stat.pstat == 0: wm_stat.change_stat()# turn off for well run
    t_start = time.time()
    if wm_stat.pnum==0:
        wm_stat.change_stat()# turn off when well runs
    while w_run.pstat == 0:
        w_run.read_port()
        wr_stat.change_stat()# flash the blue run light
        time.sleep(.1)
        t_end = time.time()
         
        t_run = round(t_end - t_start,1) #calculate the run
        t_runstr = str(t_run) # make the string
        # If runtime is excessive alert

        if t_run in range(t_max, t_max+9):
            send_mail('Well run time just exceeded: ' + t_runstr + ' Seconds')
            time.sleep(10)

        if t_run in range(t_max + 10, t_max + 19):
            send_mail('Well run time abnormal high: ' + t_runstr + ' Seconds')
            time.sleep(10)

        if t_run in range(t_max + 20, t_max + 49):
            global w_overrun
            if wr_over.pstat == 1:
                wr_over.change_stat() # turn on the overrun light
            print("Danger excess time exceeded")
            send_mail('WARNINIG: WELL ON TIME EXCESSIVE: '+ t_runstr + ' Seconds')
            time.sleep(5)
            send_mail('WARNINIG: WELL ON TIME EXCESSIVE: '+ t_runstr + ' Seconds') 
            time.sleep(5) # modify this!!!!!!!!!!!!!!!!
            print(w_overrun)
            # turn off pump and wait 

        if t_run > t_max + 50:
            print("Total Shutdown Press Reset to Restart")
            #remove this and add code for reset button!!!!!!!!!!!!!
            send_mail('PROGRAM HALT WELL RUN EXCEEDED ' + t_runstr + ' SECONDS')
            what_now = input("PROGRAM HALT, WAITING FOR INPUT")
            wr_over.change_stat() # turn off the overrun light for any input


                
    #-------------- end of run loop ---------------------
                
    if wr_stat.pstat == 0: wr_stat.change_stat() # turn off the well run light
    #<<<<<<<<<<< end of well run >>>>>>>>>>>>>

                
    t_run = round(t_end - t_start,1) #calculate the run
    #pop first item out of array and append
    localtime = time.asctime( time.localtime(time.time()) )
    w_lastrun = [localtime,t_run]
    w_log.pop(0)#get rid of the oldest data
    w_log.append(w_lastrun)#add the newest
    print("Well on time=",t_run," Seconds")
    
    q = (make_json(w_log)) # q is the return that isn't used
    update_run1(t_run) # this does all the heavy lifting with the database

    
    w_lamp.change_stat()
    w_run.read_port()
    
    localtime = time.asctime( time.localtime(time.time()) )
    print ("Local current time :", localtime)
    
    #time.sleep(2)
    
    
    






# ------------------- MAIN END ------------------------------


  


if __name__ == "__main__":
    # If this is being run stand-alone then execute otherwise it is being
    # imported and the importing program will use the modules it needs
   try:
        
        
        while True:
            2== 2 # guess this is usually true
   
            main() # Invoke the program    
                
            
            

   except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()
else:
    print("Well Monitor Loaded as Module")

    

    

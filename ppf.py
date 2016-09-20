#!/usr/bin/env python

# needed to uses terminal commands and regular expression parsing
import subprocess, re

# global variables go here
counter = 0
router_ip = 0
isp_gateway = 0
google = ""
default_gateway = ""
packets_to_send = None
default_packets = 100
ten_minutes = 600
one_hour = 3600
three_hours = 10800

# def main is required when the script may be loaded as a module. This way, it wont run everything immediately
def main(): 
    # declare globals I am using
    global router_ip
    global isp_gateway
    global google
    global default_gateway
    global packets_to_send

    # Print directions to the console
    print("\n\n\n Welcome to PingProblemFinder! \n This utility will help you inspect latency issues coming from your network.")
    print(" The utility will first find yout gateway/router IP address. \n You will then need to enter the IP address of your ISP gateway.")
    print(" There is a handy guide to doing this @ www.google.com \n\n\n")

    # input() is used to get input from a user in a console, while the router ip is being found by our find_gateway function
    find_gateway()
    router_ip = default_gateway
    isp_gateway = input(' Enter your ISP Gateway: ')
    print("")
    google = "www.google.com"
    print(" How long should we test the connection in seconds? \n Keywords: short = {0}, medium = {1}, long = {2}, xlong = {3}" .format(default_packets, ten_minutes, one_hour, three_hours))
    packets_to_send = (input(" Testing time: "))
    print("")

    try:
        packets_to_send = int(packets_to_send)
    except:
        print("\n Checking keywords...")
    
    if packets_to_send == "medium":
        packets_to_send = ten_minutes
        print(" The utility will test each connection for 10 minutes. \n")
    elif packets_to_send == "long":
        packets_to_send = one_hour
        print(" The utility will test each connection for 1 hour. \n")
    elif packets_to_send == "xlong":
        packets_to_send = three_hours
        print(" The utility will test each connection for 3 hours. \n")
    elif packets_to_send == None or isinstance(packets_to_send, (int)) == False or packets_to_send == "short":
        packets_to_send = default_packets
        print(" Your input was not a number and didn't match any keywords. \n We will just use {} for now. \n" .format(str(default_packets)))
    
    # Use testfunc to find latency values for each ip address. It is recursive, so it only needs to be called here once
    testfunc()


def testfunc():
        # Determine which connection we are testing and set values
        global counter
        global router_ip
        global isp_gateway
        global google
        global packets_to_send

        if counter == 0:
            name = "Router" 
            ip = router_ip
        elif counter == 1:
            name = "ISP"
            ip = isp_gateway
        else: 
            name = "Google"
            ip = google

        # Increment the counter so that we dont use the same connection next time
        counter+=1

        # Ping the connection and create a file with the results
        print(" Pinging {}..." .format(name))
        subprocess.call("ping {0} -n {2} > {1}ping.txt" .format(ip, name, packets_to_send), shell = True)

        # open the file we just created and create a new file for storing data later on
        connection_test = open("{0}ping.txt" .format(name))
        high_value_file = open("{0}_high_values.txt" .format(name), "w")

        # create a list of lines within the file
        ping_list = connection_test.readlines()

        # create lists to store the latency values in after they are parsed
        ms_vals_list = []
        high_vals_list = []

        # parse the connection_test 
        print(" Parsing data.... ")
        for line in ping_list:
            numline = (re.findall(r'\d+', line))
            if len(numline) < 6: continue
            else: ms_vals_list.append(numline[5])
        
        print(" Finding high latency values.... ")
        for item in ms_vals_list:
            if (int(item) < 10): continue
            else: high_vals_list.append(item)

        if high_vals_list != []:
            high_value_file.write("The high latency values were: " + ', '.join(high_vals_list))
        else: high_value_file.write("There were no high latency values detected")

        ################################# TESTING ONLY ##########################################################
        if (len(high_vals_list) != 0):
            print(" High ping values from {}: " .format(name) + ', '.join(high_vals_list) + "\n")
        else: print(" There were no ping spikes to {} \n" .format(name))

        if counter < 3:
            testfunc()
        else: print("\n\n Finished! \n\n")


def find_gateway():
    # Allow us to edit the default gateway variable
    global default_gateway
    print(" Finding your default gateway...")
    # Run ipconfig in background a save to a file
    subprocess.call("ipconfig > ipconfig.txt", shell = True)
    # Read the lines from the config file into a variable for parsing
    ip_file_lines = open("ipconfig.txt").readlines()
    # Parsing goes here
    for line in ip_file_lines:
        match = re.search("(Default Gateway.*)", line)
        if match:
            nums = re.search('\d+\.\d+\.\d+\.\d+', match.group(1))
            default_gateway = nums.group(0)
            print(" Your default gateway is: {}" .format(default_gateway))
            break


# below code is used to run main() when not a module
if __name__ == "__main__":
    main()


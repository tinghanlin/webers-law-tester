#import the libraries
import matplotlib.pyplot as plt
import numpy as np
import random, time
from termcolor import colored

#helper function that calculates average of a list
def lst_avg(lst): 
    return sum(lst) / len(lst) 

#helper function that draws the random dot plots
def draw_plots(n1, n2, pause_second, block):
    order = [n1,n2]
    #shuffle the order of the subplots, so the subplot that has more dots will not always be on the right
    random.shuffle(order)
    
    #find out which subplot has more dots
    find_ind = n2
    if n1 > n2:
        find_ind = n1
    index = order.index(find_ind) 

    #plot the subplots
    plt.ion()
    x1 = np.random.rand(order[0])
    y1 = np.random.rand(order[0])
    x2 = np.random.rand(order[1])
    y2 = np.random.rand(order[1])

    plt.subplot(1, 2, 1)
    plt.scatter(x1,y1)
    plt.xticks([])
    plt.yticks([])
    plt.title('Press 1')

    plt.subplot(1, 2, 2)
    plt.scatter(x2,y2)
    plt.xticks([])
    plt.yticks([])
    plt.title('Press 0')

    #block bit can control whether the subplots will disappear automatically
    if block ==1:
        plt.show()
    else:
        plt.pause(pause_second)
        plt.ioff()
        plt.close("all")
    return index

#helper function that collects user response
def response(index):
    while True:
        try:
            ans = int(raw_input("Press 1 for Left\nPress 0 for Right\nInsert your answer: "))
        except ValueError:
            print (colored("Try again! Please press 1 or press 0\n","red"))
        else:
            if ans is not 1 and ans is not 0:
                print (colored("Try again! Please press 1 or press 0\n", "red"))
            else:
                #detect if the response if correct or not
                if int(ans) != int(index):
                    return True
                else:
                    return False

#small case 
#staircase(number_of_dot, reaction_time, 2, 4, 3, 10)
def staircase(number_of_dot, reaction_time, start, mis_num, increment, recover):
    #store the just-noticeable difference
    jnd = []
    #count the mistake in each trial
    mistake_counter=0

    #initialize the subplots with an excess of dots
    init = int(number_of_dot*start)

    #trial will stop when the participants make a certain number of mistakes
    while mistake_counter<mis_num:
        print "Which plot has more dots?"
        #decrease the number of one subplot by staircase
        index = draw_plots(number_of_dot, init-increment, reaction_time, 0)
        init=init-increment
        res=response(index)

        if res == False: 
            #we see that the participant made a mistake
            mistake_counter+=1
            #print("mistake_counter ", mistake_counter)
            jnd.append(abs(init-number_of_dot))
            init=init+recover
        
        #deal with the special case when the participants always get the right answer
        #so that we are not infinitely decreasing the dots in one subplot
        if init < number_of_dot:
            init=init+recover
    
    #output the avergae of just-noticeable difference
    #print("list of jnd", jnd)
    return lst_avg(jnd)

#helper function that calculates just-noticeable difference with different number of dots
#it uses staircase experiment to conduct each trial
#it will output a list of "number of dots" and the corresponding "just-noticeable difference" 
def trail(number_of_dot, reaction_time):
    #for different number of dots, we use different staircase study
    if (number_of_dot < 50):
        # 20, 40
        jnd_mean = staircase(number_of_dot, reaction_time, 1.5, 4, 3, 10)
        ret = [number_of_dot, jnd_mean]
        return ret
    elif(number_of_dot > 50 and number_of_dot < 150):
        #60, 80, 100, 120, 140
        jnd_mean = staircase(number_of_dot, reaction_time, 1.3, 4, 5, 20)
        ret = [number_of_dot, jnd_mean]
        return ret
    else:
        #160, 180, 200
        jnd_mean = staircase(number_of_dot, reaction_time, 1.2, 4, 10, 80)
        ret = [number_of_dot, jnd_mean]
        return ret

    return

#start of the study
#text for introduction
print(colored("Hello!", "red"))
time.sleep(1.5)
print(colored("We are going to test out the Weber's Law on vision.", "red"))
time.sleep(3)
print(colored("Before starting the study, please adjust the position of your terminal window,\n"+ 
              "so that it is not blocking the plots shown.", "red"))
time.sleep(6)
draw_plots(20, 30, 3, 1)
get_ready = raw_input(colored("Please press ENTER key to continue!\n", "red"))
get_ready = raw_input(colored("Later, we will ask you to pick which subplot has more dots.\n"+
                              "Press 1 if the left subplot has more dots.\n"+
                              "Press 0 if the right subplot has more dots.\n"+
                              "You will only have 1 second to answer each question.\n"
                              "Please press ENTER key when you are ready to start!", "red"))
print(colored("Section 1/10", "red"))
time.sleep(1)

#store the final output
final = []

#randomize the list of different number of dots
trail_list = [20,140,60,180,100,120,40,160,80,200]

section_counter = 1
for i in trail_list:

    result = trail(i, 1)
    final.append(result)
    section_counter += 1
    if i !=200:
        print(colored("\nSection "+str(section_counter)+"/10", "red"))
        get_ready = raw_input(colored("Please press ENTER key when you are ready to start!", "red"))

#show the study results
print(colored("\nThanks!", "red"))
print(colored("\nHere are study results", "red"))
for i in range(len(final)):
    print "You are able to tell which subplot has "+str(final[i][0])+" dots, when the difference between the number of dots is around "+str(final[i][1])+" dots"

print(colored("\nHere are the raw data for researchers: ", "red"))
print str(final)
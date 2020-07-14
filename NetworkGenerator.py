import numpy as np
import os
class NetworkGenerator():
    
    def __init__(self, filename, N):
        #Open File
        try:
            os.remove(filename)
        except OSError:
            pass
        file = open(filename,"w+")
        
        #Set Network Size 
        people_list = []
        for i in range(0,N):
            people_list.append(i)
        
        
        #Source https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/Page.cfm?Lang=E&Geo1=PR&Code1=13&Geo2=&Code2=&Data=Count&SearchText=New%20Brunswick&SearchType=Begins&SearchPR=01&B1=All&GeoLevel=PR&GeoCode=13
        #Average Household Size = 2.3
        i = 0
        housecount = 0
        workcount = 0
        while (i < N):
            num = round(np.random.normal(loc = 2.3, scale = 0.5))
            housecount = housecount + num
            if num > N - i:
                num = N - i
            if (num == 2 ):
                file.write("{} {} {{}} \n".format(i, i+1))
                i = i+num
            elif (num == 3 ):
                file.write("{} {} {{}} \n".format(i, i+1))
                file.write("{} {} {{}} \n".format(i, i+2))
                file.write("{} {} {{}} \n".format(i+1, i+2))
                i = i+num
            elif (num == 4 ):
                file.write("{} {} {{}} \n".format(i, i+1))
                file.write("{} {} {{}} \n".format(i, i+2))
                file.write("{} {} {{}} \n".format(i, i+3))
                file.write("{} {} {{}} \n".format(i+1, i+2))
                file.write("{} {} {{}} \n".format(i+1, i+3))
                file.write("{} {} {{}} \n".format(i+2, i+3))
                i = i+num
            elif (num >= 5):
                file.write("{} {} {{}} \n".format(i, i+1))
                file.write("{} {} {{}} \n".format(i, i+2))
                file.write("{} {} {{}} \n".format(i, i+3))
                file.write("{} {} {{}} \n".format(i, i+4))
                file.write("{} {} {{}} \n".format(i+1, i+2))
                file.write("{} {} {{}} \n".format(i+1, i+3))
                file.write("{} {} {{}} \n".format(i+1, i+4))
                file.write("{} {} {{}} \n".format(i+2, i+3))
                file.write("{} {} {{}} \n".format(i+2, i+4))
                file.write("{} {} {{}} \n".format(i+3, i+4))
                i = i+num
            else:
                i = i+1
        #print("Step 1 done")
        k = 0
        while (k < N):
            #print(k)
            if len(people_list) <= 1:
                break
            num = round(np.random.normal(loc = 9.7, scale = 2))
            i = 0
            j = 0
            if num > N - k and N - k > 1:
                num = N - k
            elif N-k == 1:
                break
            elif num < 2:
                num = 2
            elif num > 20:
                num = 20
            workcount = workcount + num
            worklist = [] 
            count = 0
            
            while count < num:
                #print("Part 2: Loop 1")
                person = np.random.choice(people_list)
                worklist.append(person)
                people_list.remove(person)
                count = count + 1
                
            while i < len(worklist) - 1:
                #print("Part 2: Loop 2")
                j = i
                while j < len(worklist):
                    #print("Part 2: Loop 3")
                    file.write("{} {} {{}} \n".format(worklist[i], worklist[j]))
                    j = j + 1
                i = i + 1
            k = k + num
            #print(k)
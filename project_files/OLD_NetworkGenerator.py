import numpy as np
import os
class NetworkGenerator():
    
    def __init__(self, filename1, filename2, N):
        #Open File
        try:
            os.remove(filename1)
        except OSError:
            pass
        
        try:
            os.remove(filename2)
        except OSError:
            pass
        
        file = open(filename1,"w+")
        file2 = open(filename2, "w+")
        
        #Set Network Size 
        people_listW = []
        people_listH = []
        for i in range(0,N):
            people_listW.append(i)
            people_listH.append(i)
         
        agelist1 = []
        agelist2 = []
        connectlist = []
        housecount = 0
        workcount = 0
        carecount = 0
        
        #Care Home Source:https://www.nbanh.com/
        #68 homes, 4700 residents, ~69 people / home
        #68 homes / 776827 (NB Pop) = 0.00008753557
        #6000 employees, in Ontario 58% are personal workers (https://www.ontario.ca/page/long-term-care-staffing-study)
        #Therefore, 6000 * 0.58 / 68 = 51 employees
        homes_per_person = 0.00008753557
        care_homes = np.ceil(homes_per_person * N)

        print("-----Generating Care Homes-----")
        k = 0
        while (k < care_homes):
            if len(people_listW) <= 1 or len(people_listH) <= 1:
                break
            num = 69
            employees = 51
            i = 0
            j = 0
            carecount = carecount + num
            carelist = []
            carelist2 = []
            count = 0
            
            while count < num:
                person = np.random.choice(people_listH)
                carelist.append(person)
                people_listW.remove(person)
                people_listH.remove(person)
                count = count + 1
            
            count = 0
            while count < employees:
                person = np.random.choice(people_listW)
                carelist2.append(person)
                people_listW.remove(person)
                count = count + 1
            
            i = 0
            while i < len(carelist):
                agelist1.append("{}, ".format(carelist[i]))
                agelist2.append("Old, ")
                i += 1
            
            i = 0
            while i < len(carelist) - 1:
                j = i
                while j < len(carelist):
                    connectlist.append("{} {} {{}} \n".format(carelist[i], carelist[j]))
                    j = j + 1
                i = i + 1
            
            i = 0
            while i < len(carelist2) - 1:
                j = i
                while j < len(carelist2):
                    connectlist.append("{} {} {{}} \n".format(carelist[i], carelist[j]))
                    j = j + 1
                i = i + 1
                
            i = 0
            while i < len(carelist2):
                j = i
                while j < len(carelist):
                    connectlist.append("{} {} {{}} \n".format(carelist[i], carelist[j]))
                    j = j + 1
                i = i + 1  
            k = k + num
            
        #For people remaining in the house list, give an age while assigning a house
        #Age Source: https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/Page.cfm?Lang=E&Geo1=PR&Code1=13&Geo2=&Code2=&Data=Count&SearchText=New%20Brunswick&SearchType=Begins&SearchPR=01&B1=All&GeoLevel=PR&GeoCode=13
        #14.79% Young,  65.29% Adult, 19.9% Old    
        
        #For household data
        #Source https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/Page.cfm?Lang=E&Geo1=PR&Code1=13&Geo2=&Code2=&Data=Count&SearchText=New%20Brunswick&SearchType=Begins&SearchPR=01&B1=All&GeoLevel=PR&GeoCode=13
        #Average Household Size = 2.3
        print("-----Generating Households-----")
        k = 0
        M = len(people_listH)
        while (k < M):
            #print(k)
            if len(people_listH) <= 1:
                break
            num = round(np.random.normal(loc = 2.3, scale = 0.5))
            i = 0
            j = 0
            if num > M - k and N - k > 1:
                num = M - k
            elif M-k == 1:
                break
            elif num < 2:
                num = 2
            elif num > 8:
                num = 20
            housecount = housecount + num
            houselist = [] 
            count = 0
            
            while count < num:
                person = np.random.choice(people_listH)
                houselist.append(person)
                people_listH.remove(person)
                
                if person in people_listW:
                    randvar = np.random.random_sample()
                    if randvar <= 0.1479:
                        agelist1.append("{}, ".format(person))
                        agelist2.append("Young, ")
                        people_listW.remove(person)
                    elif randvar > 0.8008:
                        agelist1.append("{}, ".format(person))
                        agelist2.append("Old, ")
                        randvar2 = np.random.random_sample()
                        if randvar2 >= 0.2:
                            people_listW.remove(person)
                    else:
                        agelist1.append("{}, ".format(person))
                        agelist2.append("Adult, ")
                else:
                    agelist1.append("{}, ".format(person))
                    agelist2.append("Old, ")
                    
                count = count + 1
                
            while i < len(houselist) - 1:
                #print("Part 2: Loop 2")
                j = i
                while j < len(houselist):
                    #print("Part 2: Loop 3")
                    connectlist.append("{} {} {{}} \n".format(houselist[i], houselist[j]))
                    j = j + 1
                i = i + 1
            k = k + num
            #print(k)
            
        i = 0
        for i in connectlist:
            file.write(i)
        
        i = 0
        while i < len(agelist1):
            file2.write(agelist1[i])
            i += 1
        file2.write("\n")   
        i = 0
        while i < len(agelist2):
            file2.write(agelist2[i])
            i += 1
        
        connectlist = []
        #Work data, this is more common sense than anything, note, though, that 20% of seniors still work
        #Source: https://www12.statcan.gc.ca/census-recensement/2016/as-sa/98-200-x/2016027/98-200-x2016027-eng.cfm
        print("-----Generating Businesses-----")
        k = 0
        M = len(people_listW)
        while (k < M):
            #print(k)
            if len(people_listW) <= 1:
                break
            num = round(np.random.normal(loc = 9.7, scale = 2))
            i = 0
            j = 0
            if num > M - k and N - k > 1:
                num = M - k
            elif M-k == 1:
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
                person = np.random.choice(people_listW)
                worklist.append(person)
                people_listW.remove(person)
                count = count + 1
                
            while i < len(worklist) - 1:
                #print("Part 2: Loop 2")
                j = i
                while j < len(worklist):
                    #print("Part 2: Loop 3")
                    connectlist.append("{} {} {{}} \n".format(worklist[i], worklist[j]))
                    j = j + 1
                i = i + 1
            k = k + num
            #print(k)
            
            i = 0
        for i in connectlist:
            file.write(i)
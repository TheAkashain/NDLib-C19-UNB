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
        work_list = np.arange(N, dtype = int) #List of those needing a job
        np.random.shuffle(work_list) #Randomize it
        house_list = np.copy(work_list) #List of those needing a house
            
        connections = np.zeros(shape=(N,N), dtype = int)
        ages = np.zeros(N, dtype = float)
         
        #Care Home Source:https://www.nbanh.com/
        #68 homes, 4700 residents, ~69 people / home
        #68 homes / 776827 (NB Pop) = 0.00008753557
        #6000 employees, in Ontario 58% are personal workers (https://www.ontario.ca/page/long-term-care-staffing-study)
        #Therefore, 6000 * 0.58 / 68 = 51 employees
        homes_per_person = 0.00008753557
        care_homes = np.ceil(homes_per_person*N)
        
        print("-----Generating Care Homes-----")
        k = 0
        carecount = 0
        while (k < care_homes):
            if len(work_list) <= 1 or len(house_list) <= 1:
                break
            num = 69
            employees = 51
            i = 0
            j = 0
            carecount = carecount + num
            carelist = np.zeros(num, dtype = int)
            carelist_employee = np.zeros(employees, dtype = int)
            count = 0
            
            while count < num:
                carelist[count] = house_list[0]
                house_list = np.delete(house_list, 0)
                work_list = np.delete(work_list, 0)
                count = count+1   
            count = 0
            while count < employees:
                carelist_employee[count] = work_list[0]
                work_list = np.delete(work_list, 0)
                count = count+1
                
            i = 0
            while i < carelist.size - 1:
                ages[i] = 2
                j = i+1
                while j < carelist.size :
                    connections[carelist[i]][carelist[j]] = 1
                    j = j+1
                i = i + 1
            ages[i+1] = 2
            
            i = 0
            while i < carelist_employee.size - 1:
                ages[i] = 1
                j = i+1
                while j < carelist_employee.size:
                    connections[carelist_employee[i]][carelist_employee[j]] = 1
                    j = j + 1
                i = i + 1
            ages[i+1] = 1
            
            i = 0
            while i < carelist_employee.size:
                j = i+1
                while j < carelist_employee.size:
                    connections[carelist_employee[i]][carelist_employee[j]] = 1
                    j = j + 1
                i = i + 1
            
            k = k + 1
                
        #For people remaining in the house list, give an age while assigning a house
        #Age Source: https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/Page.cfm?Lang=E&Geo1=PR&Code1=13&Geo2=&Code2=&Data=Count&SearchText=New%20Brunswick&SearchType=Begins&SearchPR=01&B1=All&GeoLevel=PR&GeoCode=13
        #14.79% Young,  65.29% Adult, 19.9% Old    
        
        #For household data
        #Source https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/Page.cfm?Lang=E&Geo1=PR&Code1=13&Geo2=&Code2=&Data=Count&SearchText=New%20Brunswick&SearchType=Begins&SearchPR=01&B1=All&GeoLevel=PR&GeoCode=13
        #Average Household Size = 2.3
        print("-----Generating Ages-----")
        childlist = np.empty(0)
        num = house_list.size
        
        person = 0            
        while person < ages.size:
            if ages[person] == 0:
                randvar = np.random.random_sample()
                if randvar <= 0.1479:
                    ages[person] = 0.5
                    work_list = np.delete(work_list, np.argwhere(work_list == person))
                    childlist = np.append(childlist, person)
                elif randvar > 0.8008:
                    ages[person] = 2
                    randvar2 = np.random.random_sample()
                    if randvar2 > 0.2:
                        work_list = np.delete(work_list, np.argwhere(work_list == person))
                else:
                    ages[person] = 1
            
            person = person + 1
                
        print("-----Generating Households-----")
        k = 0
        M = house_list.size
        while (k<M):
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
                num = 8
                
            houselist = np.zeros(num, dtype = int)
            count = 0
            
            while count < num:
                person = house_list[0]
                houselist[count] = person
                house_list = np.delete(house_list, 0)
                count = count + 1
            
            while i < houselist.size - 1:
                j = i + 1
                while j < houselist.size:
                    connections[houselist[i]][houselist[j]] = 1
                    j = j + 1
                i = i + 1
            k = k + num
            
        print("-----Generating Schools-----")
        k = 0
        M = childlist.size
        while(k < M):
            num = round(np.random.normal(22, 5))
            i = 0
            j = 0
            if num > M - k and N - k > 1:
                num = M - k
            elif M-k == 1:
                break
            elif num < 2:
                num = 2
            elif num > 8:
                num = 8
                
            classlist = np.zeros(num, dtype = int)
            count = 0
            
            while count < num:
                person = childlist[0]
                classlist[count] = person
                childlist = np.delete(childlist, 0)
                count = count + 1
                
            while i < classlist.size - 1:
                j = i+1
                while j < classlist.size:
                    connections[classlist[i]][classlist[j]] = 1
                    j = j + 1
                i = i + 1
            k = k + num
            
        
        #Work data, this is more common sense than anything, note, though, that 20% of seniors still work
        #Source: https://www12.statcan.gc.ca/census-recensement/2016/as-sa/98-200-x/2016027/98-200-x2016027-eng.cfm

        print("-----Generating Businesses-----")
        k = 0
        M = work_list.size
        while (k < M):
            num = round(np.random.normal(loc = 11.7, scale = 2))
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

            worklist = np.zeros(num, dtype = int)
            count = 0
            
            while count < num:
                person = work_list[0]
                worklist[count] = person
                work_list = np.delete(work_list, 0)
                count = count + 1
                
            while i < worklist.size - 1:
                j = i+1
                while j < worklist.size:
                    connections[worklist[i]][worklist[j]] = 1
                    j = j + 1
                i = i + 1
            k = k + num
        
        print("-----Storing Connection Results-----")
        array1, array2 = np.nonzero(connections)
        for i in range(0, array1.size):
            file.write("{} {} {{}}\n".format(array1[i], array2[i]))
                
        print("-----Storing Age Results-----")
        for i in range(0, np.size(ages)):
            file2.write("{}, {}\n".format(i, ages[i]))
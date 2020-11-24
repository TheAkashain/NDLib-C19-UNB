#!/usr/bin/env python
# coding: utf-8

# # Build Network with Group Labels

# ### Construct Nodes with Age Labels

# In[1]:


from myGroupNetwork import myGroupNetwork

N = 20000 # Total Population

youngPercent = 0.15 # Percentage of each age group
adultPercent = 0.65
oldPercent = 1 - youngPercent - adultPercent # = 0.20

nYoung = int(youngPercent * N)
nMiddle = int(adultPercent * N)
nSenior = N - nYoung - nMiddle
data = myGroupNetwork(size={'Young': nYoung, 'Middle': nMiddle, 'Senior': nSenior})


# ### Add Groups

# In[ ]:


data.addGroup(groupType='CareHome', n=3, size={'Middle':20, 'Senior': 30}, contactPercentage=.7)


# In[ ]:


data.addGroup(groupType='School', n=3, size={'Young':50, 'Middle': 20}, contactPercentage=.7)


# In[ ]:


data.addGroup(groupType='Work', n=N//20, size={'Middle': 12}, exclude=['CareHome','School'], contactPercentage=.4)


# In[ ]:


data.addGroup(groupType='Home', n=N//4, size= 3 , exclude=['CareHome'], contactPercentage=1)


# ### Export Data

# In[ ]:


data.save( filename='network_data.json' )


# ### Inspect the result

# In[ ]:


for i in range(0, N, N//40): # List 40 nodes
    print(i,data.nodes[i])


# In[ ]:





# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 18:39:59 2018

@author: wanly
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dailyforwardrate(discountfactor):
    """
    Calculate daily forward rate
    :type discountfactor List[float]
    :rtype List[float]
    """
    dailyforwardrate0=[]
    daycount=[x/365 for x in range(len(discountfactor)-1)]
    for i in range(len(discountfactor)-1):
        dailyforwardrate0.append((discountfactor[i]-discountfactor[i+1])/(discountfactor[i+1]*(1/365)))
    plt.plot(daycount,dailyforwardrate0)
    plt.show()
    return dailyforwardrate0

def myFun(X,t1,t2,discountfactor,swaprate):
    """
    Construct function to solve by binary search
    X variable to solve
    t1 is the time of known discountfactor
    t2 is the time of X
    :type X float
    :type t1,t2 int
    :type discountfactor List[float]
    :type swaprate List[float]
    """
    #t1,t2 strat from 0!!!
    presentvalue=0
    dist=discountfactor
    #if(X==0.5):
        #print(dist)

    for i in range(t1+1,t2+1):
        
        #dist 0:t1 should be already calculated
        #print(dist[t1])
        
        dist[i]=np.exp(((t2-i)/(t2-t1))*np.log(dist[t1])+((i-t1)/(t2-t1))*np.log(X))
        
        discountfactor[i]=dist[i]
    for i in range(1,t2+1):
        presentvalue=presentvalue+dist[i]*(swaprate[t2]/2)
 #0.0       print(dist)

    return presentvalue+dist[t2]-1

def solveforx(t1,t2,discountfactor,swaprate):
    """
    Do binary search on MyFun
    t1 is the time of known discountfactor
    t2 is the time of X
    :type t1,t2 int
    :type discountfactor List[float]
    :type swaprate List[float]
    
    """
    high=1.0
    low=0.0
    mid=(high+low)/2.0
    #print(t1,t2,discountfactor,swaprate,mid)
    while(abs(myFun(mid,t1,t2,discountfactor,swaprate))>0.000001):
     #   print (mid,myFun(mid,t1,t2,discountfactor,swaprate))
        if myFun(mid,t1,t2,discountfactor,swaprate)*myFun(high,t1,t2,discountfactor,swaprate)>0:
            low,high=low,mid
        else:
            low,high=mid,high
        mid =(high+low)/2.0
       # print(mid,myFun(mid,t1,t2,discountfactor,swaprate))
    return mid,myFun(mid,t1,t2,discountfactor,swaprate)

#print(solveforx(0,2,discountfactor,swaprate))


def yieldcurveconstructorI(knowndepositrate,knowndeposityrs,knownswaprate,knownswapyrs):
    """
    Construct yield curve using interpolation
    :type knowndepositrate,knownswaprate List[float] 第一年swaprate为deposit rate
    :type knownswapyrs knowndeposityrs List[float] 已知swaprate的年
    """
    if (knowndeposityrs[0]!=0) and (knowndepositrate[0]!=0):
        knownsrate=[0]
        knownsyrs=[0]
        for i in range(len(knowndepositrate)):
            knownsrate.append(knowndepositrate[i])
            knownsyrs.append(knowndeposityrs[i])      
    else:
        knownsrate=knowndepositrate
        knownsyrs=knowndeposityrs   

    knownsyrs=[int(2*x) for x in knownsyrs]


    discountfactor=list(np.zeros(int(knownswapyrs[-1]*2+1)))
    discountfactor[0]=1
    for i in range(len(knownsyrs)):
        discountfactor[knownsyrs[i]]=1/np.power((1+knownsrate[i]),knownsyrs[i]/2)
        #warning here ,year count ambiguious
#    print(discountfactor,len(discountfactor))
    for t in range(0,knownsyrs[-1]):
        for i in range(knownsyrs[t-1],knownsyrs[t]):
            t1=knownsyrs[t-1]
            t2=knownsyrs[t]
            discountfactor[i]=np.exp(((t2-i)/(t2-t1))*np.log(discountfactor[t1])+((i-t1)/(t2-t1))*np.log(discountfactor[t2]))  
#    print(discountfactor,len(discountfactor))
    swaprate=np.zeros(int(knownswapyrs[-1]*2+1))
    swaprate[:]=np.nan
    knownswapyrs2=[int(2*yrs) for yrs in knownswapyrs]
    for i in range(len(knownswaprate)):
    #always remember yrs count start from 0 and now is 0
        swaprate[int(knownswapyrs2[i])]=knownswaprate[i]
#    known=dict(zip(knownyrs,knownrate))
   # print(swaprate,len(swaprate))
    knownind=[int(yrs*2) for yrs in knownswapyrs] 
  #  print(knownind)
    for i in knownind:
        i=int(i)
        if(i==knownind[0]):
     #       print(knownsyrs[-1],i)
            solveforx(knownsyrs[-1],i,discountfactor,swaprate)
        else:
            solveforx(knownind[knownind.index(i)-1],i,discountfactor,swaprate)
            
            
    print('discount factors\n')
    print(discountfactor)
    print('=======================================================================')
    print('if at par presentvalue should be 1\n')   
    print('present values')
    for j in range(len(knownind)):
        presentvalue=0    
        for i in range(1,knownind[j]+1):
        
            presentvalue=presentvalue+swaprate[knownind[j]]/2*discountfactor[i]

        print(presentvalue+discountfactor[knownind[j]])
    
    daycountfactor=1.0/365.0
    knownyrs=knownind
    daycount=[x*daycountfactor for x in range(int(365*knownyrs[-1]/2))]
    dailydiscountfactor=list(np.zeros(int(365*(knownyrs[-1]/2))))
    dailydiscountfactor[0]=1
    for i in range(len(discountfactor)):
        dailydiscountfactor[int(i*365/2)-1]=discountfactor[i]
    for t in range(1,len(discountfactor)):
        for i in range(dailydiscountfactor.index(discountfactor[t-1])+1,dailydiscountfactor.index(discountfactor[t])):
        #dist 0:t1 should be already calculated
            t1=dailydiscountfactor.index(discountfactor[t-1])
            t2=dailydiscountfactor.index(discountfactor[t])
            dailydiscountfactor[i]=np.exp(((t2-i)/(t2-t1))*np.log(discountfactor[t-1])+((i-t1)/(t2-t1))*np.log(discountfactor[t]))

    plt.plot(daycount,dailydiscountfactor)
    rate=np.zeros(len(dailydiscountfactor))
#can be improved
    for i in range(1,len(dailydiscountfactor)):
        rate[i]=np.power((1/dailydiscountfactor[i]),1/daycount[i])-1
    plt.show()
    plt.plot(daycount[1:],rate[1:])
    plt.show()
    instantforward=dailyforwardrate(dailydiscountfactor)
    return discountfactor,dailydiscountfactor,instantforward
    





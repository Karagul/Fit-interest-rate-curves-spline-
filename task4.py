# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 10:19:46 2018

@author: wanly
"""

import discountcurveconstructor as dc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def yieldcurvechanger(knowndepositrate,knowndeposityrs,knownswaprate,knownswapyrs):
    dailydiscountfactor=[]
    dailydiscountfactor.append(dc.yieldcurveconstructorI(knowndepositrate,knowndeposityrs,knownswaprate,knownswapyrs)[1])
    for i in range(len(knowndepositrate)):
        knowndepositrate0=knowndepositrate.copy()
        knowndepositrate0[i]=knowndepositrate0[i]+0.0001
        dailydiscountfactor.append(dc.yieldcurveconstructorI(knowndepositrate0,knowndeposityrs,knownswaprate,knownswapyrs)[1])
    for i in range(len(knownswaprate)):
        knownswaprate0=knownswaprate.copy()
        knownswaprate0[i]=knownswaprate0[i]+0.0001
        dailydiscountfactor.append(dc.yieldcurveconstructorI(knowndepositrate,knowndeposityrs,knownswaprate0,knownswapyrs)[1])
    return dailydiscountfactor
    
k1=[0.05]

k2=[1]

k3=[5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9]
k3=[x/100 for x in k3]
k4=[2,3,4,5,7,10,15,20,30]
def simplebondpricer(dailydiscountfactor,maturity,facevalue):
    paymentday=maturity*365
    price=[]
    for i in range(len(dailydiscountfactor)):
        price.append(facevalue*dailydiscountfactor[i][paymentday-1])
    return price

price=simplebondpricer(yieldcurvechanger(k1,k2,k3,k4),10,100000000)
priceimpact=[]
for i in range(1,len(price)):
    priceimpact.append(price[i]-price[0])
print(priceimpact)
print('\n')
print(k4[priceimpact.index(max(priceimpact))-1])
price=pd.DataFrame(price)
writer = pd.ExcelWriter('output2.xlsx', engine='xlsxwriter')
price.to_excel(writer)
writer.save()
# =============================================================================
# d11=[]
# d12=[]
# d13=[]
# 
# =============================================================================
# =============================================================================
# d11,d12,d13=dc.yieldcurveconstructorI(k1,k2,k3,k4)
# =============================================================================

  
# =============================================================================
# k1=[0.05]
# k2=[1]
# k3=[0.0505,
# 0.051,
# 0.0515,
# 0.052,
# 0.0525,
# 0.053,
# 0.0535,
# 0.054,
# 0.05425,
# 0.0545,
# 0.05475,
# 0.055,
# 0.055166667,
# 0.055333333
# ,0.0555
# ,0.055666667
# ,0.055833333
# ,0.056
# ,0.0561
# ,0.0562
# ,0.0563
# ,0.0564
# ,0.0565
# ,0.0566
# ,0.0567
# ,0.0568
# ,0.0569
# ,0.057
# ,0.0571
# ,0.0572
# ,0.0573
# ,0.0574
# ,0.0575
# ,0.0576
# ,0.0577
# ,0.0578
# ,0.0579
# ,0.058
# ,0.05805
# ,0.0581
# ,0.05815
# ,0.0582
# ,0.05825
# ,0.0583
# ,0.05835
# ,0.0584
# ,0.05845
# ,0.0585
# ,0.05855
# ,0.0586
# ,0.05865
# ,0.0587
# ,0.05875
# ,0.0588
# ,0.05885
# ,0.0589
# ,0.05895
# ,0.059
# ]
# k4=[float(x) for x in np.arange(1.5,30.5,0.5)]
# d21,d22,d23=dc.yieldcurveconstructorI(k1,k2,k3,k4)   
# 
# d=[d12[i]-d22[i] for i in range(len(d12))]
# daycount=[x/365 for x in range(len(d))]
# plt.plot(daycount,d)
# 
# plt.show()
# =============================================================================

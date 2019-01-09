# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 10:19:46 2018

@author: wanly
"""

import discountcurveconstructor as dc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
k1=[0.05]

k2=[1]

k3=[5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9]
k3=[x/100 for x in k3]
k4=[2,3,4,5,7,10,15,20,30]
#不构造新的产品，对仅对已知swap插值计算
d11,d12,d13=dc.yieldcurveconstructorI(k1,k2,k3,k4)

k1=[0.05]
k2=[1]
k3=[0.0505,
0.051,
0.0515,
0.052,
0.0525,
0.053,
0.0535,
0.054,
0.05425,
0.0545,
0.05475,
0.055,
0.055166667,
0.055333333
,0.0555
,0.055666667
,0.055833333
,0.056
,0.0561
,0.0562
,0.0563
,0.0564
,0.0565
,0.0566
,0.0567
,0.0568
,0.0569
,0.057
,0.0571
,0.0572
,0.0573
,0.0574
,0.0575
,0.0576
,0.0577
,0.0578
,0.0579
,0.058
,0.05805
,0.0581
,0.05815
,0.0582
,0.05825
,0.0583
,0.05835
,0.0584
,0.05845
,0.0585
,0.05855
,0.0586
,0.05865
,0.0587
,0.05875
,0.0588
,0.05885
,0.0589
,0.05895
,0.059
]
k4=[float(x) for x in np.arange(1.5,30.5,0.5)]
#上述数据为构造了新的利率掉期之后产生的已知利率及其年份
d21,d22,d23=dc.yieldcurveconstructorI(k1,k2,k3,k4)   

d=[d12[i]-d22[i] for i in range(len(d12))]
daycount=[x/365 for x in range(len(d))]
plt.plot(daycount,d)

plt.show()

d11=pd.DataFrame(d11)
d12=pd.DataFrame(d12)
d21=pd.DataFrame(d21)
d22=pd.DataFrame(d22)
d13=pd.DataFrame(d13)
d23=pd.DataFrame(d23)
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
d11.to_excel(writer,sheet_name='11')
d12.to_excel(writer,sheet_name='12')
d13.to_excel(writer,sheet_name='13')
d21.to_excel(writer,sheet_name='21')
d22.to_excel(writer,sheet_name='22')
d23.to_excel(writer,sheet_name='23')

writer.save()
pp=[]
for i in range(41):
    pp.append(d12.iloc[i*90,0])

















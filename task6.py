# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:27:52 2018

@author: wanly
"""

from QuantLib import *
from pandas import DataFrame
import numpy as np
import utils
import matplotlib.pyplot as plt

depo_maturities = [Period(12, Months)]
depo_rates = [5.0]
# Bond rates
bond_maturities = [Period(24, Months),Period(36, Months),Period(48, Months),Period(60, Months),Period(84, Months),Period(120, Months),Period(180, Months),Period(240, Months),Period(360, Months)]
bond_rates = [5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9]
maturities = depo_maturities+bond_maturities
rates = depo_rates+bond_rates
DataFrame(list(zip(maturities, rates)),columns=["Maturities","Curve"],index=['']*len(rates))

calc_date = Date(21, 10, 2018)
Settings.instance().evaluationDate = calc_date
calendar = UnitedStates()
business_convention = Unadjusted
day_count = Thirty360()
end_of_month = True
settlement_days = 0
face_amount = 100
coupon_frequency = Period(Semiannual)
settlement_days = 0

depo_helpers = [DepositRateHelper(QuoteHandle(SimpleQuote(r/100.0)),m,
settlement_days,calendar,business_convention,end_of_month,day_count ) for r, m in zip(depo_rates, depo_maturities)]

bond_helpers = []
for r, m in zip(bond_rates, bond_maturities):
    termination_date = calc_date + m
    schedule = Schedule(calc_date,
                        termination_date,
                        coupon_frequency,
                        calendar,
                        business_convention,
                        business_convention,
                        DateGeneration.Backward,
                        end_of_month)
    
    bond_helper = FixedRateBondHelper(QuoteHandle(SimpleQuote(face_amount)),
                                      settlement_days,
                                      face_amount,
                                      schedule,
                                      [r/100.0],
                                      day_count,
                                      business_convention,
                                      )
    bond_helpers.append(bond_helper)
    
rate_helpers = depo_helpers + bond_helpers

def get_spot_rates(
        yieldcurve, day_count,
        calendar=UnitedStates(), days=10*360):
    spots = []
    tenors = []
    ref_date = yieldcurve.referenceDate()
    calc_date = ref_date
    for day in range(0, days):
        yrs = day/360.0
        d = calendar.advance(ref_date, Period(day, Days))
        compounding = Compounded
        freq = Semiannual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(
                day_count,compounding,freq,calc_date,d).rate()
        spots.append(100*eq_rate)
    return DataFrame(list(zip(tenors, spots)),
                     columns=["Maturities","Curve"],
                     index=['']*len(tenors))

yc_logcubicdiscount = PiecewiseLogCubicDiscount(calc_date,
rate_helpers,
day_count)

splcd = get_spot_rates(yc_logcubicdiscount, day_count)
splcd.tail()

yc_linearzero = PiecewiseLinearZero(
        calc_date,rate_helpers,day_count)
yc_cubiczero = PiecewiseCubicZero(
        calc_date,rate_helpers,day_count)
splz = get_spot_rates(yc_linearzero, day_count)
spcz = get_spot_rates(yc_cubiczero, day_count)
splz.tail()
#输出三种插值方法构造的曲线
plt.plot(splcd["Maturities"],splcd["Curve"], '.',
        label="LogCubicDiscount")

plt.show()
plt.plot(splz["Maturities"],splz["Curve"],'--',
        label="LinearZero")
plt.show()
plt.plot(spcz["Maturities"],spcz["Curve"],
        label="CubicZero")
plt.show()
timelz=list(spcz['Maturities'])
timelz=timelz[1:]
rate=list(spcz['Curve'])
rate=rate[1:]
discountf=[1/(1+rate[x])**timelz[x] for x in range(len(rate))]
fow=[(discountf[x-1]-discountf[x])/discountf[x-1] for x in range(1,len(discountf))]
plt.plot(timelz[1:],fow)
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 16:20:36 2013

@author: Ari Ramdial
"""
import numpy as np
import scipy as sp
from scipy.optimize import fsolve as solver
from scipy.integrate import ode
import math as math
import sys


X = np.zeros((1440,1))    
    
def CobelliWrap(x,u,D,p,modelData):
    xdot = Cobelli(0,x,u,D,p,modelData)
    return xdot.T[0]
        
def Cobelli(t,x,u,D,p,modelData):
    x = x
    xdot = np.zeros((12,1))
    G_p = x[0] 
    G_t = x[1] 
    I_l = x[2] 
    I_p = x[3] 
    Q_sto1 = x[4]
    Q_sto2 = x[5] 
    Q_gut = x[6] 
    I_1 = x[7] 
    I_d = x[8] 
    X = x[9] 
    Y = x[10] 
    I_po = x[11] 
    
    
    # Constants
    V_G = p[0] 
    k_1 = p[1] 
    k_2 = p[2] 
    V_I = p[3] 
    m_1 = p[4] 
    m_2 = p[5] 
    m_4 = p[6] 
    m_5 = p[7] 
    m_6 = p[8] 
    HE_b = p[9] 
    k_max = p[10] 
    k_min = p[11] 
    k_abs = p[12] 
    k_gri = p[13] 
    f = p[14] 
    a = p[15] 
    b = p[16] 
    c = p[17] 
    d = p[18] 
    k_p1 = p[19] 
    k_p2 = p[20] 
    k_p3 = p[21] 
    k_p4 = p[22] 
    k_i = p[23] 
    F_cns = p[24] 
    V_m0 = p[25] 
    V_mx = p[26] 
    K_m0 = p[27] 
    p_2U = p[28] 
    K = p[29] 
    alpha = p[30] 
    beta = p[31] 
    gamma = p[32] 
    k_e1 = p[33] 
    k_e2 = p[34] 
    BW = modelData[0]
    
    #------------------------------------------------------------------
    #------------------------------------------------TYPE 2 -------------
    S = gamma*I_po 
    S_b =(m_6 - HE_b)/m_5 
    # Insulin basal state
    I_b = 4.4 #basal insulin levels above 60pmol/l is considered insulin resistant.
    h = 70 # = G_b = 4.4mmol/l
    # Certain useful parameters are defined
    HE = -m_5*S + m_6  #0.012243
    m_3 = HE*m_1/(1- HE)
    #GI Tract
   
    Ra = (f*k_abs*Q_gut)/BW
    Q_sto = Q_sto1 + Q_sto2 
    k_emptQ_sto = k_min +((k_max - k_min)/2)*((math.tanh(a*(Q_sto -b* D)) - math.tanh(c*(Q_sto -d*D))+2))
    # Liver
    EGP = sp.maximum(2.4, k_p1 - k_p2*G_p - k_p3*I_d - k_p4*I_po )# CHange 0 to 2.01 for test
    
    # Muscle and Adipose Tissue
    V_m = V_m0 + V_mx*X
    K_m = K_m0
    U_id = V_m*G_t/(K_m +G_t)
    # Kidneys - Glucose Renal Excretion
    if(G_p > k_e2):
        E = k_e1*(G_p -k_e2)
    else:
        E = 0
    
    # Brain - CNS Glucose Utilization
    U_ii = F_cns 
    # Mass balances/ differential equations
    xdot[0] = EGP + Ra - U_ii - E - k_1*G_p + k_2*G_t  # dG_p
    
    xdot[1] = -U_id + k_1*G_p - k_2*G_t  # dG_t
    xdot[2] = -(m_1 +m_3 )*I_l + m_2*I_p + S #dI_l
    xdot[3] = -(m_2 +m_4 )*I_p + m_1*I_l #+ u #dI_p
    G = G_p/V_G #G(t)
    I = I_p/V_I
    
    xdot[4] = D*d - k_gri*Q_sto1  #dQ_sto1
    xdot[5] = k_gri*Q_sto1 - k_emptQ_sto*Q_sto2  #dQ_sto2
    xdot[6] = k_emptQ_sto*Q_sto2 - k_abs*Q_gut  #dQ_gut
    xdot[7] = -k_i*(I_1 -I) #dI_1
    xdot[8] = -k_i*(I_d -I_1 ) #dI_d
    xdot[9] = p_2U*(I-I_b )-p_2U*X #dX
    
    if(beta*(G-h) >= -S_b):
        xdot[10] = -alpha*(Y-beta*(G-h)) #dY_t
    else:
        xdot[10] = -alpha*(Y+S_b)
    
    # Pancreas/ Beta -Cell
    if(xdot[0]/V_G > 0):
        S_po = Y + S_b + K*(xdot[0]/V_G)
    else:
        S_po = Y + S_b 
        
    xdot[11] = S_po - S #dI_po
    
    return xdot
    
    
def SimulateCobelliDay(modelData):
    
   # modelData = np.zeros((22,1))
    eatingTime = 30 # [min ]
    # Data is unpacked
    
    bHour = modelData[1]
    bMin = modelData[2]
    bCHO = 1000*modelData[3]*18.018  # converted to mg
    bInsulin = 6.945*modelData[4]/1000  # converted from IU/L to pmol/L
    lHour = modelData[5] 
    lMin = modelData[6] 
    lCHO = 1000*modelData[7]*18.018  # converted to mg
    lInsulin = 6.945*modelData[8]/1000  # converted to pmol/L
    dHour = modelData[9]
    dMin = modelData[10]
    dCHO = 1000*modelData[11]*18.018 # converted to mg
    dInsulin = 6.945*modelData[12]/1000 # converted to pmol/L
    insulinTime = modelData[13]
    
    # Initialize the time vector
    t = np.zeros((11,1)) 
    # Relevant moments are calculated
    t[0] = 0
    t[1] = bHour*60 + bMin - insulinTime 
    t[2] = bHour*60 + bMin 
    t[3] = bHour*60 + bMin + eatingTime 
    t[4] = lHour*60 + lMin - insulinTime 
    t[5] = lHour*60 + lMin 
    t[6] = lHour*60 + lMin + eatingTime 
    t[7] = dHour*60 + dMin - insulinTime 
    t[8] = dHour*60 + dMin 
    t[9] = dHour*60 + dMin + eatingTime 
    t[10] = 24*60
    V_G = 1.88 #1.49 # [dL/kg]
    k_1 = 0.065 #0.042 # [min ^-1]
    k_2 = 0.079 #0.071 # [min ^-1]
    V_I = 0.05 #0.04 # [L/kg]
    m_1 = 0.190 #0.379 # [min ^-1]
    m_2 = 0.484 #0.673 # [min ^-1]
    m_4 = 0.194 #0.269 # [min ^-1]
    m_5 = 0.0304 #0.0526 # [min *kg/pmol ]
    m_6 = 0.6471 #0.8118 # [-]
    HE_b = 0.6  # [-]
    k_max = 0.0558 #0.0465 # [min ^-1]
    k_min = 0.0080 #0.0076 # [min ^-1]
    k_abs = 0.057 #0.023 # [min ^-1]
    k_gri = 0.0558 #0.0465 # [min ^-1]
    f = 0.90 # [-]
    a = 0.00013 #0.00006 # [mg ^-1]
    b = 0.82 #0.68 # [-]
    c = 0.00236 #0.00023 # [mg ^-1]
    d = 0.010 # 0.09 # [-]
    k_p1 = 2.70 #3.09 # [mg/kg/min ]
    k_p2 = 0.0021 #0.0007 # [min ^-1]
    k_p3 = 0.009 #0.005 # [mg/kg/min per pmol/L]
    k_p4 = 0.0618 #0.0786 # [mg/kg/min per pmol/kg]
    k_i = 0.0079 #0.0066 # [min ^-1]
    F_cns = 1 # [mg/kg/min ]
    V_m0 = 2.50 #4.65 # [mg/kg/min ]
    V_mx = 0.047 #0.034 # [mg/kg/min per pmol/L]
    K_m0 = 225.59 #466.21 # [mg/kg]
    p_2U = .0331 #0.084 # [min ^-1]
    K = 2.30 #0.99 # [pmol/kg per mg/dL]
    alpha = 0.050 #0.013 # [min ^-1]
    beta = 0.11 #0.05 # [pmol/kg/min per mg/dL]
    gamma = 0.5 # [min ^-1]
    k_e1 = 0.0005 #0.0007 # [min ^-1]
    k_e2 = 339 #269 # [mg/kg]
     
    p = [V_G ,k_1 ,k_2 , V_I ,m_1 ,m_2 ,m_4 ,m_5 ,m_6 ,HE_b, k_max , k_min , k_abs , 
         k_gri,f,a,b,c,d, k_p1,k_p2, k_p3, k_p4,k_i , F_cns , V_m0,V_mx ,K_m0, p_2U,K,
        alpha,beta, gamma , k_e1, k_e2]
    
    
    u = 0 #0.0954119*BW, #7.15
    X = []
    # Calculate the steady state values
    xStart = [90,90,54.18,54.18,0,0,0,4.4,4.4,0,0,0] #zeros(16,1) ,
    
    # (xStart,u,0,p,modelData)
    xInitial0 = solver(CobelliWrap,xStart,args=(u,0,p,modelData))
    
    
    # Midnight to first insulinshot
    
    r = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial0, t[0]).set_f_params(u ,0,p,modelData)
    while r.successful() and r.t < t[1]:
        r.integrate(r.t+1)
        X.append(r.y[0])
       
    # Insulinshot before breakfast
    xInitial1 = r.y.T
    xInitial1[2] = xInitial1[2] + bInsulin
    r1 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial1, t[1]).set_f_params(u ,0,p,modelData)
    while r1.successful() and r1.t < t[2]:
        r1.integrate(r1.t+1)
        X.append(r1.y[0])
     
    # Breakfast start
    xInitial2 = r1.y.T
    r2 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial2, t[2]).set_f_params(u ,bCHO/(eatingTime),p,modelData)
    while r2.successful() and r2.t < t[3]:
        r2.integrate(r2.t+1)
        X.append(r2.y[0])
     
    # Breakfast stop
    xInitial3 = r2.y.T
    r3 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial3, t[3]).set_f_params(u ,0,p,modelData)
    while r3.successful() and r3.t < t[4]:
        r3.integrate(r3.t+1)
        X.append(r3.y[0])
       
    # Insulinshot before lunch
    xInitial4 = r3.y.T
    xInitial4[2] = xInitial4[2] + lInsulin 
    r4 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial4, t[4]).set_f_params(u ,0,p,modelData)
    while r4.successful() and r4.t < t[5]:
        r4.integrate(r4.t+1)
        X.append(r4.y[0])
       
    # Lunch start
    xInitial5 = r4.y.T
    r5 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial5, t[5]).set_f_params(u ,lCHO/(eatingTime),p,modelData)
    while r5.successful() and r5.t < t[6]:
        r5.integrate(r5.t+1)
        X.append(r5.y[0])
      
    # Lunch stop
    xInitial6 = r5.y.T
    r6 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial6, t[6]).set_f_params(u ,0,p,modelData)
    while r6.successful() and r6.t < t[7]:
        r6.integrate(r6.t+1)
        X.append(r6.y[0])
     
    # Insulinshot before dinner
    xInitial7 = r6.y.T
    xInitial7[2] = xInitial7[2] + dInsulin 
    r7 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial7, t[7]).set_f_params(u ,0,p,modelData)
    while r7.successful() and r7.t < t[8]:
        r7.integrate(r7.t+1)
        X.append(r7.y[0])
    
    # Dinner start
    xInitial8 = r7.y.T
    r8 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial8, t[8]).set_f_params(u ,dCHO/(eatingTime),p,modelData)
    while r8.successful() and r8.t < t[9]:
        r8.integrate(r8.t+1)
        X.append(r8.y[0])
       
    
    # Dinner stop
    xInitial9 = r8.y.T
    r9 = ode(Cobelli).set_integrator('vode', method='bdf', order=15).set_initial_value(xInitial9, t[9]).set_f_params(u ,0,p,modelData)
    while r9.successful() and r9.t < t[10]:
        r9.integrate(r9.t+1)
        X.append(r9.y[0])
        #sys.exit(0)
    
    # Collects all the simulated intervals
  
    G = [x / V_G for x in X]
    T = r.t
   
    return (T,G,t)    
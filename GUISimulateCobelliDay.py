@mfunction("T, G, t")
def GUISimulateCobelliDay(modelData=None):
    # GUISIMULATECOBELLIDAY models Cobelli for a day
    # GUISimulateCobelliDay is used in modelSimulator when simulating
    # the Cobelli model for a whole day . This isn 't meant to be run as
    # a single function , but ONLY as an assistant function for
    # modelSimulator.
    #
    # See also : COBELLI , MODELSIMULATOR
    eatingTime = 30# [min ]
    # Data is unpacked
    BW = modelData(1)
    bHour = modelData(2)
    bMin = modelData(3)
    bCHO = 1000 * modelData(4) * 18.018# converted to mg
    bInsulin = 6.945 * modelData(5) / 1000# converted from IU/L to pmol/L
    lHour = modelData(6)
    lMin = modelData(7)
    lCHO = 1000 * modelData(8) * 18.018# converted to mg
    lInsulin = 6.945 * modelData(9) / 1000# converted to pmol/L
    dHour = modelData(10)
    dMin = modelData(11)
    dCHO = 1000 * modelData(12) * 18.018# converted to mg
    dInsulin = 6.945 * modelData(13) / 1000# converted to pmol/L
    insulinTime = modelData(14)
    fatMetabolism = modelData(22)
    # Initialize the time vector
    t = zeros(11, 1)
    # Relevant moments are calculated
    t(1).lvalue = 0
    t(2).lvalue = bHour * 60 + bMin - insulinTime
    t(3).lvalue = bHour * 60 + bMin
    t(4).lvalue = bHour * 60 + bMin + eatingTime
    t(5).lvalue = lHour * 60 + lMin - insulinTime
    t(6).lvalue = lHour * 60 + lMin
    t(7).lvalue = lHour * 60 + lMin + eatingTime
    t(8).lvalue = dHour * 60 + dMin - insulinTime
    t(9).lvalue = dHour * 60 + dMin
    t(10).lvalue = dHour * 60 + dMin + eatingTime
    t(11).lvalue = 24 * 60
    V_G = 1.88#1.49; % [dL/kg]
    k_1 = 0.065#0.042; % [min ^-1]
    k_2 = 0.079#0.071; % [min ^-1]
    V_I = 0.05#0.04; % [L/kg]
    m_1 = 0.190#0.379; % [min ^-1]
    m_2 = 0.484#0.673; % [min ^-1]
    m_4 = 0.194#0.269; % [min ^-1]
    m_5 = 0.0304#0.0526; % [min *kg/pmol ]
    m_6 = 0.6471#0.8118; % [-]
    HE_b = 0.6# [-]
    k_max = 0.0558#0.0465; % [min ^-1]
    k_min = 0.0080#0.0076; % [min ^-1]
    k_abs = 0.057#0.023; % [min ^-1]
    k_gri = 0.0558#0.0465; % [min ^-1]
    f = 0.90# [-]
    a = 0.00013#0.00006; % [mg ^-1]
    b = 0.82#0.68; % [-]
    c = 0.00236#0.00023; % [mg ^-1]
    d = 0.010#0.09; % [-]
    k_p1 = 2.70#3.09; % [mg/kg/min ]
    k_p2 = 0.0021#0.0007; % [min ^-1]
    k_p3 = 0.009#0.005; % [mg/kg/min per pmol/L]
    k_p4 = 0.0618#0.0786; % [mg/kg/min per pmol/kg]
    k_i = 0.0079#0.0066; % [min ^-1]
    F_cns = 1# [mg/kg/min ]
    V_m0 = 2.50#4.65; % [mg/kg/min ]
    V_mx = 0.047#0.034; % [mg/kg/min per pmol/L]
    K_m0 = 225.59#466.21; % [mg/kg]
    p_2U = .0331#0.084; % [min ^-1]
    K = 2.30#0.99; % [pmol/kg per mg/dL]
    alpha = 0.050#0.013; % [min ^-1]
    beta = 0.11#0.05; % [pmol/kg/min per mg/dL]
    gamma = 0.5# [min ^-1]
    k_e1 = 0.0005#0.0007; % [min ^-1]
    k_e2 = 339#269; % [mg/kg]
    #-------------------------------------------------TYPE 1-----------------
    k_d = 0.0164#min^-1
    k_a1 = 0.0018#min^-1
    k_a2 = 0.0182#min^-1
    K_p = 0.032#pmol/kg/min per mg/dl
    T_l = 450#min
    T_d = 66#min
    T_s = 10#min

    #--------------------------------------------------------------------------



    p = mcat([V_G, OMPCSEMI, k_1, OMPCSEMI, k_2, OMPCSEMI, V_I, OMPCSEMI, m_1, OMPCSEMI, m_2, OMPCSEMI, m_4, OMPCSEMI, m_5, OMPCSEMI, m_6, OMPCSEMI, HE_b, OMPCSEMI, k_max, OMPCSEMI, k_min, OMPCSEMI, k_abs, OMPCSEMI, k_gri, OMPCSEMI, f, OMPCSEMI, a, OMPCSEMI, b, OMPCSEMI, c, OMPCSEMI, d, OMPCSEMI, k_p1, OMPCSEMI, k_p2, OMPCSEMI, k_p3, OMPCSEMI, k_p4, OMPCSEMI, k_i, OMPCSEMI, F_cns, OMPCSEMI, V_m0, OMPCSEMI, V_mx, OMPCSEMI, K_m0, OMPCSEMI, p_2U, OMPCSEMI, K, OMPCSEMI, alpha, OMPCSEMI, beta, OMPCSEMI, gamma, OMPCSEMI, k_e1, OMPCSEMI, k_e2, OMPCSEMI, BW, OMPCSEMI, k_d, OMPCSEMI, k_a1, OMPCSEMI, k_a2, OMPCSEMI, K_p, OMPCSEMI, T_l, OMPCSEMI, T_d, OMPCSEMI, T_s])
    odeOptions = mcat([])
    options = optimset(mstring('Display '), mstring('off '))
    u = 0#0.0954119*BW; %7.15----------------------------------------------------------------------------------------------////////////////////////////
    # Calculate the steady state values
    xStart = mcat([130, OMPCSEMI, 130, OMPCSEMI, 54.18, OMPCSEMI, 54.18, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 4.4, OMPCSEMI, 4.4, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0, OMPCSEMI, 0])#zeros(16,1) ;
    xInitial0 = fsolve(@, xStart, options, u, 0, p, modelData)
    # A progress bar is created
    #waitbarHandle = waitbar(0, 'Modelling Cobelli , please wait ... ');
    # Midnight to first insulinshot
    [T1, X1] = ode15s(@, mcat([t(1), t(2)]), xInitial0, odeOptions, u, 0, p, modelData)
    #waitbar(1/10 , waitbarHandle);
    # Insulinshot before breakfast
    xInitial1 = X1(end, mslice[:]).cT
    xInitial1(3).lvalue = xInitial1(3) + bInsulin
    [T2, X2] = ode15s(@, mcat([t(2), t(3)]), xInitial1, odeOptions, u, 0, p, modelData)
    #waitbar(2/10 , waitbarHandle);
    # Breakfast start
    xInitial2 = X2(end, mslice[:]).cT
    [T3, X3] = ode15s(@, mcat([t(3), t(4)]), xInitial2, odeOptions, u, bCHO / (eatingTime), p, modelData)
    #waitbar(3/10 , waitbarHandle);
    # Breakfast stop
    xInitial3 = X3(end, mslice[:]).cT
    [T4, X4] = ode15s(@, mcat([t(4), t(5)]), xInitial3, odeOptions, u, 0, p, modelData)
    #waitbar(4/10 , waitbarHandle);
    # Insulinshot before lunch
    xInitial4 = X4(end, mslice[:]).cT
    xInitial4(3).lvalue = xInitial4(3) + lInsulin
    [T5, X5] = ode15s(@, mcat([t(5), t(6)]), xInitial4, odeOptions, u, 0, p, modelData)
    #waitbar(5/10 , waitbarHandle);
    # Lunch start
    xInitial5 = X5(end, mslice[:]).cT
    [T6, X6] = ode15s(@, mcat([t(6), t(7)]), xInitial5, odeOptions, u, lCHO / (eatingTime), p, modelData)
    #waitbar(6/10 , waitbarHandle);
    # Lunch stop
    xInitial6 = X6(end, mslice[:]).cT
    [T7, X7] = ode15s(@, mcat([t(7), t(8)]), xInitial6, odeOptions, u, 0, p, modelData)
    #waitbar(7/10 , waitbarHandle);
    # Insulinshot before dinner
    xInitial7 = X7(end, mslice[:]).cT
    xInitial7(3).lvalue = xInitial7(3) + dInsulin
    [T8, X8] = ode15s(@, mcat([t(8), t(9)]), xInitial7, odeOptions, u, 0, p, modelData)
    #waitbar(8/10 , waitbarHandle);
    # Dinner start
    xInitial8 = X8(end, mslice[:]).cT
    [T9, X9] = ode15s(@, mcat([t(9), t(10)]), xInitial8, odeOptions, u, dCHO / (eatingTime), p, modelData)
    #waitbar(9/10 , waitbarHandle);
    # Dinner stop
    xInitial9 = X9(end, mslice[:]).cT
    [T10, X10] = ode15s(@, mcat([t(10), t(11)]), xInitial9, odeOptions, u, 0, p, modelData)
    #waitbar(95/100 , waitbarHandle);
    # Collects all the simulated intervals
    T_concat = mstring('T = [')
    X_concat = mstring('X = [')
    for n in mslice[1:(length(t) - 1)]:
        T_concat = mcat([T_concat, mstring('T'), int2str(n), mstring(';')])
        X_concat = mcat([X_concat, mstring('X'), int2str(n), mstring('(: ,1) ;')])
        end
        T_concat = mcat([T_concat, mstring(']; ')])
        X_concat = mcat([X_concat, mstring(']; ')])
        eval(T_concat)
        eval(X_concat)

        G = X / V_G
        #waitbar(1, waitbarHandle);
        #close( waitbarHandle);

@mfunction("xdot")
def Cobelli(t=None, x=None, u=None, D=None, p=None, modelData=None):
    # COBELLI is a model for absorption of CHO in a human body.
    # Cobelli is a mathematical model , based on various differential
    # equations , representing different parts of the human body .
    #
    # The parametric inputs means the following .
    # t: The time window for the simulation
    # x: The initial conditions
    # u: Administration of short - acting insulin
    # D: CHO eating rate
    # p: Vector containing the 36 constants necessary for the model
    #
    # Syntax :
    # [T,X]= ode15s(@Cobelli ,[t0 t1], xInitial0 ,odeOptions ,u,D,p);
    # Functions are defined
    G_p = x(1, 1)
    G_t = x(2, 1)
    I_l = x(3, 1)
    I_p = x(4, 1)
    Q_sto1 = x(5, 1)
    Q_sto2 = x(6, 1)
    Q_gut = x(7, 1)
    I_1 = x(8, 1)
    I_d = x(9, 1)
    X = x(10, 1)
    Y = x(11, 1)
    I_po = x(12, 1)
    B = x(13, 1)
    FFA = x(14, 1)
    G_fat = x(15, 1)
    I_fat = x(16, 1)
    # Constants
    V_G = p(1, 1)
    k_1 = p(2, 1)
    k_2 = p(3, 1)
    V_I = p(4, 1)
    m_1 = p(5, 1)
    m_2 = p(6, 1)
    m_4 = p(7, 1)
    m_5 = p(8, 1)
    m_6 = p(9, 1)
    HE_b = p(10, 1)
    k_max = p(11, 1)
    k_min = p(12, 1)
    k_abs = p(13, 1)
    k_gri = p(14, 1)
    f = p(15, 1)
    a = p(16, 1)
    b = p(17, 1)
    c = p(18, 1)
    d = p(19, 1)
    k_p1 = p(20, 1)
    k_p2 = p(21, 1)
    k_p3 = p(22, 1)
    k_p4 = p(23, 1)
    k_i = p(24, 1)
    F_cns = p(25, 1)
    V_m0 = p(26, 1)
    V_mx = p(27, 1)
    K_m0 = p(28, 1)
    p_2U = p(29, 1)
    K = p(30, 1)
    alpha = p(31, 1)
    beta = p(32, 1)
    gamma = p(33, 1)
    k_e1 = p(34, 1)
    k_e2 = p(35, 1)
    BW = p(36, 1)
    #------------------------------------TYPE 1----------------------
    k_d = p(37, 1)
    k_a1 = p(38, 1)
    k_a2 = p(39, 1)
    K_p = p(40, 1)
    T_l = p(41, 1)
    T_d = p(42, 1)
    #-------------------------------------------------------------------
    #--------------------FAT METABOLISM--------------------------------
    a_fat = 864
    b_fat = 1.44
    S_IO = 0.72
    c_fat = 0.72
    tau_fat = 10000000000
    d_fat = 43.2
    e_fat = 43.2
    f_fat = 432
    g_fat = 0.06
    h_fat = 0.00084
    m_fat = 0.0000024
    j_fat = 0.1
    k_fat = 270
    p_fat = 50
    lambda_fat = 0.09
    t_fat = 1

    #------------------------------------------------------------------
    #------------------------------------------------TYPE 2 -------------
    S = gamma * I_po
    S_b = (m_6 - HE_b) / m_5
    # Insulin basal state
    I_b = 4.4#basal insulin levels above 60pmol/l is considered insulin resistant.
    h = 70# = G_b = 4.4mmol/l
    # Certain useful parameters are defined
    HE = -m_5 * S + m_6#0.012243;
    m_3 = HE * m_1 / (1 - HE)
    #GI Tract
    Ra = f * k_abs * Q_gut / BW
    Q_sto = Q_sto1 + Q_sto2
    k_emptQ_sto = k_min + ((k_max - k_min) / 2) * ((tanh(a * (Q_sto - b * D)) - tanh(c * (Q_sto - d * D)) + 2))
    # Liver
    EGP = max(2.4, k_p1 - k_p2 * G_p - k_p3 * I_d - k_p4 * I_po)# CHange 0 to 2.01 for test

    # Muscle and Adipose Tissue
    V_m = V_m0 + V_mx * X
    K_m = K_m0
    U_id = V_m * G_t / (K_m + G_t)
    # Kidneys - Glucose Renal Excretion
    if (G_p > k_e2):
        E = k_e1 * (G_p - k_e2)
    else:
        E = 0
        end
        # Brain - CNS Glucose Utilization
        U_ii = F_cns
        # Mass balances/ differential equations
        xdot = zeros(16, 1)
        #-------------------------FAT METABOLISM MODEL EQUATIONS-------------------
        if (modelData(22) == 1):
            xdot(1, 1).lvalue = EGP + Ra - U_ii - E - k_1 * G_p + k_2 * G_t        # dG_p
            xdot(2, 1).lvalue = -U_id + k_1 * G_p - k_2 * G_t        # dG_t
            xdot(3, 1).lvalue = -(m_1 + m_3) * I_l + m_2 * I_p + S        #dI_l
            xdot(4, 1).lvalue = -(m_2 + m_4) * I_p + m_1 * I_l        #+ u; %dI_p
            xdot(13, 1).lvalue = B * G_fat * (h_fat - m_fat * G_fat) - g_fat * B
            xdot(14, 1).lvalue = (G_fat * j_fat) / (1 + lambda_fat * I_fat) - p_fat * FFA
            xdot(15, 1).lvalue = a_fat - (b_fat + (S_IO * I_fat) / (1 + tau_fat * FFA)) * G_fat
            xdot(16, 1).lvalue = (d_fat * FFA * (1 - (FFA / k_fat)) * B * G_fat ** 2) / (e_fat + G_fat ** 2) - f_fat * I_fat

            G = (G_p) / V_G + G_fat        #G(t)
            I = (I_p - I_fat) / V_I
            #---------------------------END--------------------------------------------    
        else:
            xdot(1, 1).lvalue = EGP + Ra - U_ii - E - k_1 * G_p + k_2 * G_t        # dG_p

            xdot(2, 1).lvalue = -U_id + k_1 * G_p - k_2 * G_t        # dG_t
            xdot(3, 1).lvalue = -(m_1 + m_3) * I_l + m_2 * I_p + S        #dI_l
            xdot(4, 1).lvalue = -(m_2 + m_4) * I_p + m_1 * I_l        #+ u; %dI_p
            G = G_p / V_G        #G(t)
            I = I_p / V_I
            end

            xdot(5, 1).lvalue = D * d - k_gri * Q_sto1        #dQ_sto1
            xdot(6, 1).lvalue = k_gri * Q_sto1 - k_emptQ_sto * Q_sto2        #dQ_sto2
            xdot(7, 1).lvalue = k_emptQ_sto * Q_sto2 - k_abs * Q_gut        #dQ_gut
            xdot(8, 1).lvalue = -k_i * (I_1 - I)        #dI_1
            xdot(9, 1).lvalue = -k_i * (I_d - I_1)        #dI_d
            xdot(10, 1).lvalue = p_2U * (I - I_b) - p_2U * X        #dX
            if (beta * (G - h) >= -S_b):            #dY
                xdot(11, 1).lvalue = -alpha * (Y - beta * (G - h))            #dY_t
            else:
                xdot(11, 1).lvalue = -alpha * (Y + S_b)
                end
                # Pancreas/ Beta -Cell
                if (xdot(1, 1) / V_G > 0):
                    S_po = Y + S_b + K * (xdot(1, 1) / V_G)
                else:
                    S_po = Y + S_b
                    end
                    xdot(12, 1).lvalue = S_po - S                #dI_po

                    #--------------------------------------END TYPE 2---------------------------

                    #For TYPE 1 DIABETES:-------------------------------------------------------
                    #I_sc1 = x(3,1);
                    #I_sc2 = x(4,1);
                    #G_s = x(1,1);
                    #xdot(3,1) = -(k_d+k_a1)*I_sc1 + IIR;  % k_d = 0.0164 min^-1 , k_a1 = 0.0018 min^-1
                    #xdot(4,1) = k_d*I_sc1 - k_a2*I_sc2; % k_a2 = 0.0182 min^-1
                    #R_i = k_a1*I_sc1 + k_a2*I_sc2;
                    # IIR = Pro + Int + Der;
                    #Pro = K_p*(G_s - G_tar); % K_p = 0.032 pmol/kg/min per mg/dl
                    #Int = (K_p/T_l)*int(G_s-G_tar,o,t); %T_l = 450 min
                    #Der = K_p*T_d*xdot(1,1); %T_d = 66 min
                    #xdot(1,1) = -1/T_s*G_s + 1/T_s*G; %dG_s/dt
                    #K_p1 = EGP_b + k_p2*G_pb + k_p3*I_b;

                    #I_lb = I+pb*(m_2/(m_1+m_3));
                    #I_pb = IIR_b/(m_2+m_4-((m_1*m_2)/(m_1+m_3)));
                    #i
                    #   I_sc1ss = (I_pb/(k_d+k_a1))*(m_2+m_4-((m_1*m_2)/(m_1+m_3)));
                    # I_sc2ss = (k_d/k_a2)*I_sc1ss;  


                    #IIR_b = 7.58e-4 % basal insulin infusion rate = 1 U/h = 1/(60*22) mg/min
                    #EGP = 2.4; %mg/kg/min 
                    #G_tar = 130; %mg/dl
                    #G_pb = 1.92; %mg/kg/min
                    #G_b = 91.76; %mg/dl 
                    #I_b = 25.49; %pmol/l  

                    #------------------------------------------END TYPE 1-----------------------

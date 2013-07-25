@mfunction("xdot")
def CobelliWrap(x=None, u=None, D=None, p=None, modelData=None):
    # COBELLIWRAP is used to find steady state for Cobelli
    # This is a helping function to Cobelli , used to calculate the
    # steady state values . This function only makes sense in
    # combination with Cobelli .
    #
    # See also : COBELLI , GUISIMULATECOBELLIDAY , GUISIMULATECOBELLIWEEK
    xdot = Cobelli(0, x, u, D, p, modelData)

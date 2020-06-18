"""
#TODO utf coding for ö 
constants for pyLAR

these may be modified, are not intended to be modified.

zs. elter 2020
"""

import numpy as np

organnames={'1': 'bladder',
            '2': 'skeleton',
            '3': 'stomach',
            '4': 'colon',
            '5': 'liver',
            '6': 'lung',
            '7': 'bone marrow',
            '8': 'skin',
            '9': 'testes',
            '10': 'thyroid',
            '11': 'uterus',
            '12': 'breast',
            '13': 'ovaries',
            '14': 'whole body',
            '15': 'kidney',
            '16': 'remainder'} #TODO check these

#TODO check
#TODO what is 'solid' in table. solid vs leukemia cancer, does not cause issues here
#TODO why is in excel the whole body slightly different? Because non-fatal skin is excluded.
#TODO prostate and testes used interchangably? basically, yes
#TODO, this needs to be nicer somehow
#TODO, again, excel sheet has a 0.5 year shift!! that is a bug in the spreadsheet.
LARt=[0,5,10,15,20,30,40,50,60,70,80]
def getLAR(age,gender,organ):
    """
    interpolates tabulated LAR values
    """
    
    gender = genderTest(gender)

    LARt=[0,5,10,15,20,30,40,50,60,70,80]
    
    LAR={'1': {'male': [219,188,159,135,116,84,84,81,71,50,24], 
               'female' : [221,189,161,137,116,84,83,78,67,48,24]},
         '2': {'male': [10.4,8.0,6.1,4.6,3.5,2.0,1.1,0.6,0.3,0.1,0.0], 
               'female' : [10.4,8.0,6.1,4.7,3.6,2.1,1.2,0.6,0.3,0.1,0.0]},
         '3': {'male': [168,139,114,94,77,51,48,43,35,24,12], 
               'female' : [212,175,144,118,97,64,61,55,46,33,18]},
         '4': {'male': [342,292,248,210,179,129,126,117,97,65,29], 
               'female' : [225,193,164,139,118,84,82,76,65,46,23]},
         '5': {'male': [103,86,71,59,49,34,33,29,24,17,9], 
               'female' : [57,47,39,32,26,18,18,16,14,10,6]},
         '6': {'male': [320,268,222,185,154,108,107,104,90,65,35], 
               'female' : [785,660,552,462,387,272,269,255,217,150,79]},
         '7': {'male': [193,142,112,97,89,78,79,83,88,87,64], 
               'female' : [173,117,88,75,69,60,61,63,65,63,47]},
         '8': {'male': [1720,917,484,256,136,38,10,3,1,0,0],  #TODO use 8->to15 keep same indexing
               'female' : [972,517,273,144,76,21,6,2,0,0,0]},
         '9': {'male': [198,172,148,127,110,82,83,80,61,30,9], 
               'female' : [0]*11},
         '10': {'male': [123,107,58,32,23,11,5,2,1,0,0], 
               'female' : [386,352,196,106,73,30,12,4,1,0,0]},
         '11': {'male': [0]*11, 
               'female' : [66,55,46,38,31,21,19,16,12,8,4]},
         '12': {'male': [0]*11, 
               'female' : [1260,982,761,588,454,265,146,72,32,12,4]},
         '13': {'male': [0]*11, 
               'female' : [91,77,64,53,45,31,28,24,17,11,5]},
         '14': {'male': [2950,2110,1680,1370,1140,801,761,699,580,402,208], 
               'female' : [5020,3620,2800,2210,1780,1160,981,827,659,456,242]},
         '15': {'male': [102,55,44,37,31,22,20,16,11,6,2], 
               'female' : [133,53,41,34,28,20,17,14,10,5,2]},
         '16': {'male': [1180,653,498,394,313,199,174,142,101,58,24], 
               'female' : [1410,707,534,422,336,213,184,151,112,69,31]}
         }
    #TODO is linear interpolation really good?   
    #TODO is this /100000/0.1 correct?
    return np.interp(age,LARt,LAR[organ][gender])/100000/0.1

kSEQOrganExt={'1': {'male': 0.696, 'female': 0.720},
              '2': {'male': 0.824, 'female': 0.804},
              '3': {'male': 0.708, 'female': 0.731},
              '4': {'male': 0.686, 'female': 0.708},
              '5': {'male': 0.711, 'female': 0.730},
              '6': {'male': 0.762, 'female': 0.770},
              '7': {'male': 0.706, 'female': 0.721},
              '8': {'male': 0.879, 'female': 0.883},
              '9': {'male': 0.800, 'female': 0.0},
              '10': {'male': 0.756, 'female': 0.814},
              '11': {'male': 0.0, 'female': 0.665},
              '12': {'male': 0.0, 'female': 0.829},
              '13': {'male': 0.0, 'female': 0.706},
              '14': {'male': 0.686, 'female': 0.708}, #whole body same as colon
              '15': {'male': 0.723, 'female': 0.7305},
              '16': {'male': 0.716, 'female': 0.716}}

kOrganInt={'1': {'Cs-137':1.5/1.4,'Cs-134':2.6/2.1},
           '2': {'Cs-137':1.0,'Cs-134':2.2/2.1},
           '3': {'Cs-137':1.0,'Cs-134':2.4/2.1},
           '4': {'Cs-137':(1.6+1.6+1.5)/3/1.4,'Cs-134':(2.7+2.7+2.6)/3/2.1},
           '5': {'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '6': {'Cs-137':1.0,'Cs-134':2.2/2.1},
           '7': {'Cs-137':1.0,'Cs-134':2.3/2.1},
           '8': {'Cs-137':0.79,'Cs-134':0.76},
           '9': {'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '10': {'Cs-137':1.0,'Cs-134':2.2/2.1},
           '11': {'Cs-137':1.6/1.4,'Cs-134':2.8/2.1},
           '12': {'Cs-137':(0.79+1)/2,'Cs-134':(0.76+1)/2},
           '13': {'Cs-137':1.0,'Cs-134':2.2/2.1},
           '14': {'Cs-137':1.0,'Cs-134':1.0},
           '15': {'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '16': {'Cs-137':1.0,'Cs-134':1.0}}

#TODO not used
T12={'urban':[1,0.75,0.1,15,1,1,0.1],
     'hunter':[0.9,1.2,0.11,30,0.9,1.1,0.11]}

T12Cs134=2.06 #years

T12Cs137=30.08 #years #TODO CHange to 30.05 but why?

def eCs137(age,gender):
    """Effective dose rate conversion factor
    in (mSv/y)/(Bq/kg) units for Cs137
    
    Parameters
    ----------
    age : float
        age of a person
    gender : str
        gender of a person
    
    Returns
    -------
    float
        effective dose rate conversion factor in (mSv/y)/(Bq/kg)
    """
    return 0.0014*weightFunc(age,gender)**0.111

#TODO test
#TODO this might be part of Person? or inherit age from there?
def eCs134(age,gender):
    """Effective dose rate conversion factor
    in (mSv/y)/(Bq/kg) units for Cs134
    
    Parameters
    ----------
    age : float
        age of a person in years
    gender : str
        gender of a person
    
    Returns
    -------
    float
        effective dose rate conversion factor in (mSv/y)/(Bq/kg)
    """
    return 0.00164*weightFunc(age,gender)**0.188

def CsRatio(t):
    """
    Change in the Cs ratio after time t
    
    Parameters
    ----------
    
    t : float
        time in years
    """
    
    return np.exp(((np.log(2)/T12Cs137)-(np.log(2)/T12Cs134))*t)

def kSEQK(age):
    """Age-dependent organ-specificabsorbeddoserateperunitkermarate,normalizedagainstthecorresponding valueforanadul
    """
    k=[]
    if (not isinstance(age,list)) and (not isinstance(age,np.ndarray)):
            age=[age]
    
    for a in age:
        if a<20: #TODO is that /1017 actually correct?
            k.append((0.0015*a**5 - 0.1214*a**4 + 3.473*a**3 - 40.28*a**2 + 136.3*a + 1233)/1017)
            #TODO k.append((0.00124*a**4 - 0.5364*a**3 + 7.4882*a**2 – 44.88*a*1 + 136.3*a + 1209.8)/1000)
        else:
            k.append(1.0)
    
    if len(k) == 1:
        return k[0]
    else:
        return np.array(k)



def weightFunc(age,gender):
    """gender: 0 or 1
    age float or list
    
    return weight kg        
    """
    weight=[]
    gender = genderTest(gender)
    if (not isinstance(age,list)) and (not isinstance(age,np.ndarray)):
            age=[age]
            
    for a in age:
        if gender=='female':
            if a<20:
                weight.append(-0.0000057*a**6+0.000552*a**5-0.0199*a**4+0.3191*a**3-2.1579*a**2+7.4423*a+3.9529)
            else:
                weight.append(63.0)
        else:
            if a<20: #=IF(D8=1,(-0.0021*B8^6+0.2623*B8^5-11.799*B8^4+230.5*B8^3-1875.9*B8^2+8076.6*B8+3887.2)/1000,78)
                weight.append((-0.0021*a**6+0.2623*a**5-11.799*a**4+230.5*a**3-1875.9*a**2+8076.6*a+3887.2)/1000)
            else:
                weight.append(78.0)
    if len(weight) == 1:
        return weight[0]
    else:
        return np.array(weight)
    
    
#TODO: 'F'and 'M' and 0/1
def genderTest(gender):
    if gender == 'female' or gender == 'Female' or gender == 'FEMALE':
        return 'female'
    elif gender == 'male' or gender == 'Male' or gender == 'MALE':
        return 'male'
    else:
        raise TypeError("Gender is either 'female' or 'male'")
        
def step(t,a,b):
    #TODO for t time vector as well
    if (not isinstance(a,list)) and (not isinstance(a,np.ndarray)):
            a=np.array([a])
    else:
        a=np.array(a)
    
            
    if (not isinstance(b,list)) and (not isinstance(b,np.ndarray)):
            b=np.array([b])
    else:
        b=np.array(b)
    
    return b[np.where(a<=t)[0][-1]]
    
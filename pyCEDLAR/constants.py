"""
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
              #'14': {'male': -, 'female': -}, #TODO whole body needs special attention
              '15': {'male': 0.723, 'female': 0.7305},
              '16': {'male': 0.716, 'female': 0.716}}

kOrganInt={'1': {'name': 'Blasa', 'Cs-137':1.5/1.4,'Cs-134':2.6/2.1},
           '2': {'name': 'Benvävnad', 'Cs-137':1.0,'Cs-134':2.2/2.1},
           '3': {'name': 'Stomach', 'Cs-137':1.0,'Cs-134':2.4/2.1},
           '4': {'name': 'Colon', 'Cs-137':(1.6+1.6+1.5)/3/1.4,'Cs-134':(2.7+2.7+2.6)/3/2.1},
           '5': {'name': 'Lever', 'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '6': {'name': 'Lunga', 'Cs-137':1.0,'Cs-134':2.2/2.1},
           '7': {'name': 'Röd benmärg', 'Cs-137':1.0,'Cs-134':2.3/2.1},
           '8': {'name': 'skin', 'Cs-137':0.79,'Cs-134':0.76},
           '9': {'name': 'Testes', 'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '10': {'name': 'Thyroid', 'Cs-137':1.0,'Cs-134':2.2/2.1},
           '11': {'name': 'Uterus', 'Cs-137':1.6/1.4,'Cs-134':2.8/2.1},
           '12': {'name': 'Bröst', 'Cs-137':(0.79+1)/2,'Cs-134':(0.76+1)/2},
           '13': {'name': 'Ovaries', 'Cs-137':1.0,'Cs-134':2.2/2.1},
           '14': {'name': 'Helkropp', 'Cs-137':1.0,'Cs-134':1.0},
           '15': {'name': 'Njure', 'Cs-137':1.5/1.4,'Cs-134':2.5/2.1},
           '16': {'name': 'Remainder', 'Cs-137':1.0,'Cs-134':1.0}}


T12={'urban':[1,0.75,0.1,15,1,1,0.1],
     'hunter':[0.9,1.2,0.11,30,0.9,1.1,0.11]}

T12Cs134=2.06 #years

T12Cs137=30.2 #years

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

def kSEQK(age):
    """Age-dependent organ-specificabsorbeddoserateperunitkermarate,normalizedagainstthecorresponding valueforanadul
    """
    if age<20:
        k=(0.0015*age**5 - 0.1214*age**4 + 3.473*age**3 - 40.28*age**2 + 136.3*age + 1233)/1017
    else:
        k=1
    return k



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
    
    
    
def genderTest(gender):
    if gender == 'female' or gender == 'Female' or gender == 'FEMALE':
        return 'female'
    elif gender == 'male' or gender == 'Male' or gender == 'MALE':
        return 'male'
    else:
        raise TypeError("Gender is either 'female' or 'male'")
"""
Person() and Model() class

zs. elter 2020
"""

import numpy as np
import scipy.integrate as integrate

from constants import *  #TODO from pyCEDLAR


class Model(object):
    """
    collection of model parameters
    
    these are not necessarily intended to be modified, but can be
            
    TODO: eCs134 and eCs137 logically come here?
    
    TODO: t1 t2 t3 depends on urban or hunter! maybe that should be called here?
    """
    
    def __init__(self,dCs=0.636,t1=1,t2=0.75,t3=15,
                 c1=1,c2=0.1,
                 r0=0.96,r1=36.89025,
                 r2=0.1082,r3=2.447175,
                 r4=0.0796,r5=0.668408,
                 r6=0.0314,r7=0.125646):
        self.dCs=dCs
        self.t1=t1
        self.t2=t2
        self.t3=t3
        self.c1=c1
        self.c2=c2
        self.r0=r0
        self.r1=r1
        self.r2=r2
        self.r3=r3
        self.r4=r4
        self.r5=r5
        self.r6=r6
        self.r7=r7
        
    def r(self,t):
        """r(t) function
        
        Parameters
        ----------
        t : float or numpy.ndarray"""
        
        return self.r0*np.exp(-self.r1*t) + self.r2*np.exp(-self.r3*t) + self.r4*np.exp(-self.r5*t) + self.r6*np.exp(-self.r7*t)
    
    def functc(self,t):
        """calculate the first term of the sencond integral
           in Eq 1
        """
        term1=1-np.exp((-np.log(2)/self.t1)*t)
        term2=self.c1*np.exp((-np.log(2)/self.t2)*t)
        term3=self.c2*np.exp((-np.log(2)/self.t3)*t)
        return term1*(term2+term3)
        

class Person(object):
    """
    A class used to represent a Person.
    Parameters
    ----------
    Aloc : float
        lorumipsum
    Areg : float
        lorumipsum
        
    Attributes
    ----------
    Aloc : float
        lorumipsum
    Areg : float
        lorumipsum
    TODO
    TODO model should be "Chernobyl" "Fukushima", or a userdefined Model() if elif elif isinstance, else warning
    TODO Tagmax may depend on being hunter or urban?
    TODO CEK is rather part of Model?
    """
    
    def __init__(self, Areg=1000, Aloc=1000,
                 PhiKH=0.82,fshield=0.4,fout=0.2,fsnow=1,
                 CEK=0.73, FR=0.56,Tagmax=6.7,
                 Saliment=1,Sdecont=1, 
                 age=2, gender='female',model=Model()):
        self.Areg = Areg
        self.Aloc = Aloc
        self.PhiKH = PhiKH
        self.fshield = fshield
        self.fout = fout
        self.fsnow = fsnow
        self.CEK = CEK
        self.FR = FR
        self.Tagmax = Tagmax
        if isinstance(age,(float,int)) and age>=0:
            self.age = age #todo test positive
        else:
            raise ValueError('Age has to be a positive number')

        self.points=[t - self.age for t in LARt] #TODO check this is to make sure the breaks are at right place
        if isinstance(Saliment,tuple) and len(Saliment)==2 and isinstance(Saliment[0], (int, float)) and isinstance(Saliment[1], (int, float)):
            self.Saliment = Saliment
        elif isinstance(Saliment,tuple) and len(Saliment)==2 and \
                  len(Saliment[0]) == len(Saliment[1]) and \
                  all((isinstance(x, (int, float)) and x>=0) for x in Saliment[0]) and \
                  all((isinstance(x, (int, float)) and x>=0 and x<=1) for x in Saliment[1]) and \
                  all(i < j for i, j in zip(Saliment[0], Saliment[0][1:])):
            if Saliment[0][0]>0:
                Saliment[0].insert(0,0)
                Saliment[1].insert(0,Saliment[1][0])
            self.Saliment = Saliment
            self.points=np.append(self.points,Saliment[0])
        elif isinstance(Saliment,(int,float)):
            self.Saliment = Saliment
        else:
            raise ValueError('Saliment is either float or tuple of lists')

        if isinstance(Sdecont,tuple) and len(Sdecont)==2 and isinstance(Sdecont[0], (int, float)) and isinstance(Sdecont[1], (int, float)):
            self.Sdecont = Sdecont
        elif isinstance(Sdecont,tuple) and len(Sdecont)==2 and \
                  len(Sdecont[0]) == len(Sdecont[1]) and \
                  all((isinstance(x, (int, float)) and x>=0) for x in Sdecont[0]) and \
                  all((isinstance(x, (int, float)) and x>=0 and x<=1) for x in Sdecont[1]) and \
                  all(i < j for i, j in zip(Sdecont[0], Sdecont[0][1:])):
            if Sdecont[0][0]>0:
                Sdecont[0].insert(0,0)
                Sdecont[1].insert(0,Sdecont[1][0])
            self.Sdecont = Sdecont
            self.points=np.append(self.points,Sdecont[0])
        elif isinstance(Sdecont,(int,float)):
            self.Sdecont = Sdecont
        else:
            raise ValueError('Sdecont is either float or tuple of lists')
            
        self.points=np.unique(self.points) #TODO maybe not here, or should be a _points
        self.gender = genderTest(gender)
        
        if model == 'Chernobyl':
            self.model=Model()
#TODO figure out proper values here, and include Fukushima case
#        elif model == 'Fukushima':
#            self.model = Model(dCs=0.999,t1=1,t2=0.75,t3=15,
#                 c1=1,c2=0.1,
#                 r0=0.758,r1=36.89025,
#                 r2=0.1082,r3=2.447175,
#                 r4=0.0796,r5=0.668408,
#                 r6=0.0314,r7=0.125646)
        elif isinstance(model, Model):
            self.model = model
        else:
            raise TypeError('Model() is expected')
    
    def __repr__(self):
        return "%.1f old %s" % (self.age, self.gender)
    
    def Salimentf(self,t):
        """
        Time dependent function of a factor representing the relative decrease
        in proportion to the standard radioecological transfer factor of foodstuffs
        brought on by various counter measures.
        
        The function is a wrapper for :meth:`constants.step()`.
        
        Parameters
        ----------
        t : float
            time when the Saliment factor is evaluated
        """
        if isinstance(self.Saliment,(int,float)):
            return self.Saliment
        else:
            return step(t,self.Saliment[0],self.Saliment[1])
    
    def Sdecontf(self,t):
        """
        Time dependent function of the factor representing the ratio between the ambient
        dose rate in the area after and before a decontamination procedure.
        
        The function is a wrapper for :meth:`constants.step()`.
        
        Parameters
        ----------
        t : float
            time when the Saliment factor is evaluated
        """
        if isinstance(self.Sdecont,(int,float)):
            return self.Sdecont
        else:
            return step(t,self.Sdecont[0],self.Sdecont[1])
    
    
    def fsex(self,age):
        """
        Empirical factor accounting for lower observed radiocaesium concentraction
        per unit body mass in women compared with adult males
        
        Parameters
        ----------
        age : float or list
            Age at which the fsex factor is evaluated.
            
        """
        #TODO: in article it says some 0.81 mean was used what is that?
        fsex=[]
        if (not isinstance(age,list)) and (not isinstance(age,np.ndarray)):
            age=[age]
            
        for a in age:
            if self.gender == 'male' or a<20:
                fsex.append(1)
            else:
                fsex.append(0.61)
        if len(fsex) == 1:
            return fsex[0]
        else:
            return np.array(fsex)
    
        
    def getCED(self, t0=0, tacc=70):
        """
        Function calculates the cumulative effective dose after fallout happenned 
        at t0 over a period of accummulation time tacc.
        
        Parameters
        ----------
        t0 : float
            time after fallout. Default is 0 year.
        tacc : float
            accumulation time. Default is 50 years.
        
        Returns
        -------
        CED : float
            cumulative effective dose
        """
                
        C1 = self.Aloc*self.model.dCs*self.PhiKH*self.CEK
        C2 = self.Areg*self.Tagmax

        result1 = integrate.quad(lambda t: C1*self.Sdecontf(t)*self.model.r(t)*self.fsnow*(self.fout + (1-self.fout)*self.fshield), t0, t0+tacc,points=self.points)
        result2 = integrate.quad(lambda t: C2*self.Salimentf(t)*self.model.functc(t)*self.fsex(self.age+t)*(eCs137(self.age+t,self.gender)+self.FR*CsRatio(t)*eCs134(self.age+t,self.gender)), t0, t0+tacc,points=self.points)
        
        return result1[0]+result2[0]
    
    def getDorgDot(self, t,organ='14'):
        """Function that calculates the external and internal contribution at a given time
        to a specific organ dose rate
        
        Parameters
        ----------
        t : float or ndarray
            time or time vector
        organ : str
            the type of organ. Default '14', which is whole body
            
        Returns
        -------
        dorgDot : float
            External and internal contribution at a given time to a specific organ dose rate
        """
        
        C1 = self.Aloc*self.model.dCs*self.PhiKH*kSEQOrganExt[organ][self.gender]
        C2 = self.Areg*self.Tagmax
        
        dorgDot=C1*self.Sdecontf(t)*self.model.r(t)*kSEQK(self.age+t)*self.fsnow* \
                (self.fout + (1-self.fout)*self.fshield) \
                + C2*self.Salimentf(t)*self.model.functc(t)*self.fsex(self.age+t)* \
                (kOrganInt[organ]['Cs-137']*eCs137(self.age+t,self.gender)+ \
                 kOrganInt[organ]['Cs-134']*self.FR*CsRatio(t)*eCs134(self.age+t,self.gender))
                
        
        return dorgDot
    
    def getDorg(self, t0=0, tacc=70,organ='14'):
        """
        Function calculates the the sum of the external and the internal contributions 
        to a specific organ dose.
        
        Parameters
        ----------
        t0 : float
            time after fallout. Default is 0 year.
        tacc : float
            accumulation time. Default is 50 years.
        organ : str
            type of organ. 
        
        
        Returns
        -------
        dorg : float
            organ dose
        """

        result=integrate.quad(self.getDorgDot,t0,t0+tacc,args=(organ),points=self.points)
        dorg = result[0]
        return dorg
    
    def getCUMLAR(self,t0=0, tacc=70,organ='14'):
        """
        Function to evaluate CUMLAR, the cumulative life-time attributable risk of cancer
        in a certain organ.
        
        Parameters
        ----------
        t0 : float
            time after fallout. Default is 0 year.
        tacc : float
            accumulation time. Default is 50 years.
        organ : str
            type of organ. 
        
        
        Returns
        -------
        cumlar : float
            Cumulative life-time attributable risk of cancer in percantage. 
        """
        result = integrate.quad(lambda t: self.getDorgDot(t,organ=organ) * \
                                getLAR(self.age+t,self.gender,organ), t0, t0+tacc,points=self.points)
        cumlar = result[0]/1000*100
        return cumlar
    
        
        
        
        
        
if __name__ == "__main__":
    sari = Person(age=2,gender='female',Saliment=([0,5,10,20],[0.7,0.7,0.4,0.1]),
                  Sdecont=([0,5,10,20],[1.0,0.9,0.8,0.7]))
    #sari = Person(age=2,gender='female',Saliment=1)
    #              Sdecont=([0,6,12,20],[0.1,0.2,0.4,1]))
    print(sari.getCED(t0=0.5,tacc=70)) #163.689
    print(sari.getCED(t0=0.0,tacc=70)) #163.689
    print(sari.getCED()) #213.808
    print(sari.getDorg(organ='14'))
    print(sari.getCUMLAR(organ='14'))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
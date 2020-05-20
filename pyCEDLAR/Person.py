"""Person class described here

zs. elter 2020
"""

import numpy as np
import scipy.integrate as integrate

from constants import *  #TODO from pyLAR


class Model(object):
    """
    collection of model parameters
    
    these are not necessarily intended to be modified, but can be
    
    TODO: pdf?
    
    TODO: eCs134 and eCs137 logically come here?
    
    TODO: t1 t2 t3 depends on urban or hunter! maybe that should be called here?
    """
    
    def __init__(self,t1=1,t2=0.75,t3=15,
                 c1=1,c2=0.1,
                 r0=0.96,r1=36.89025,
                 r2=0.1082,r3=2.447175,
                 r4=0.0796,r5=0.668408,
                 r6=0.0314,r7=0.125646):
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
        """r(t) function"""
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
    TODO Tagmax may depend on being hunter or urban?
    TODO CEK is rather part of Model?
    TODO what is dCs in the excelsheet?
    """
    
    def __init__(self, Areg=1000, Aloc=1000, dCs=0.636,
                 PhiKH=0.82,fshield=0.4,fout=0.2,fsnow=1,
                 CEK=0.73, FR=0.56,Tagmax=6.7,
                 Saliment=1,Sdecont=1, 
                 age=2, gender='female',model=Model()):
        self.Areg = Areg
        self.Aloc = Aloc
        self.dCs = dCs
        self.PhiKH = PhiKH
        self.fshield = fshield
        self.fout = fout
        self.fsnow = fsnow
        self.CEK = CEK
        self.FR = FR
        self.Tagmax = Tagmax
        self.Saliment = Saliment
        self.Sdecont = Sdecont
        self.age = age #todo test positive
        self.gender = genderTest(gender)
        
        if isinstance(model, Model):
            self.model = model
        else:
            raise TypeError('Model() is expected')
    
    def __repr__(self):
        return "%.1f old %s" % (self.age, self.gender)
    
    def fsex(self,age):
        """
        empirical factor accounting for lower observed radiocaesium concentraction
        TODO: maybe part of person?
        TODO: in article it says some 0.81 mean was used what is that?
        TODO, maybe age is not a property of the class?
        """
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
    
        
    def getCED(self, t0=0, tacc=70, dt=0.5):
        """
        Function calculates the cumulative effective dose t years after fallout
        over a period of accummulation time tacc.
        
        Parameters
        ----------
        t0 : float
            time after fallout. Default is 0 year.
        tacc : float
            accumulation time. Default is 50 years.
        dt : float
            time step for integration. Default is 0.5 years.
        
        Returns
        -------
        CED : float
            cumulative effective dose
        """
        
#        t = np.linspace(t0,t0+tacc,int(tacc/dt)+1) #TODO, check this int thing
#        age = self.age + t
#        
        C1 = self.Aloc*self.Sdecont*self.dCs*self.PhiKH*self.CEK
#        IntF1 = self.model.r(t)*self.fsnow*(self.fout + (1-self.fout)*self.fshield)
#        Int1 = np.trapz(IntF1, t) #TODO does dt change anything?
#        
#        
        C2 = self.Areg*self.Tagmax*self.Saliment
#        
#        IntF2 = self.model.functc(t)*self.fsex(age)*(eCs137(age,self.gender)+self.FR*np.exp(((np.log(2)/T12Cs137)-(np.log(2)/T12Cs134))*t)*eCs134(age,self.gender)) #TODO give better name
#        Int2 = np.trapz(IntF2, t)
        
        #TODO integration goes now from t0 to tacc. shouldnt it go from t0 to t0+tacc?
        #result = integrate.quad(lambda t: C1*self.model.r(t)*self.fsnow*(self.fout + (1-self.fout)*self.fshield)+C2*self.model.functc(t)*self.fsex(self.age+t)*(eCs137(self.age+t,self.gender)+self.FR*np.exp(((np.log(2)/T12Cs137)-(np.log(2)/T12Cs134))*t)*eCs134(self.age+t,self.gender)), t0, tacc)
        result1 = integrate.quad(lambda t: C1*self.model.r(t)*self.fsnow*(self.fout + (1-self.fout)*self.fshield), t0, t0+tacc)
        result2 = integrate.quad(lambda t: C2*self.model.functc(t)*self.fsex(self.age+t)*(eCs137(self.age+t,self.gender)+self.FR*CsRatio(t)*eCs134(self.age+t,self.gender)), t0, t0+tacc)
#        CED=C1*Int1 + C2*Int2
        
        #TODO, the integrate.quad makes dt obsolate!
        
        return result1[0]+result2[0]
    
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
        
        C1 = self.Aloc*self.Sdecont*self.dCs*self.PhiKH*kSEQOrganExt[organ][self.gender]
        C2 = self.Areg*self.Tagmax*self.Saliment
#        
#        IntF2 = self.model.functc(t)*self.fsex(age)*(eCs137(age,self.gender)+self.FR*np.exp(((np.log(2)/T12Cs137)-(np.log(2)/T12Cs134))*t)*eCs134(age,self.gender)) #TODO give better name
#        Int2 = np.trapz(IntF2, t)
        
        #TODO integration goes now from t0 to tacc. shouldnt it go from t0 to t0+tacc?
        #result = integrate.quad(lambda t: C1*self.model.r(t)*self.fsnow*(self.fout + (1-self.fout)*self.fshield)+C2*self.model.functc(t)*self.fsex(self.age+t)*(eCs137(self.age+t,self.gender)+self.FR*np.exp(((np.log(2)/T12Cs137)-(np.log(2)/T12Cs134))*t)*eCs134(self.age+t,self.gender)), t0, tacc)
        result1 = integrate.quad(lambda t: \
                C1*self.model.r(t)*kSEQK(self.age+t)*self.fsnow* \
                (self.fout + (1-self.fout)*self.fshield), \
                t0, t0+tacc)
        result2 = integrate.quad(lambda t: \
                C2*self.model.functc(t)*self.fsex(self.age+t)* \
                (kOrganInt[organ]['Cs-137']*eCs137(self.age+t,self.gender)+ \
                 kOrganInt[organ]['Cs-134']*self.FR*CsRatio(t)*eCs134(self.age+t,self.gender)), \
                 t0, t0+tacc)
#        CED=C1*Int1 + C2*Int2
        
        #TODO, the integrate.quad makes dt obsolate!
        
        return result1[0]+result2[0]
    
    def getCUMLAR(self,t0=0, tacc=70,organ='14'):
        """
        calculate CUMLAR
        """
        #TODO, is this really a sum, or rather an integrate?
        result1 = integrate.quad(lambda t: self.getDorg(t0=t0,tacc=tacc,organ=organ)* \
                                 getLAR(self.age+t,self.gender,organ), t0, t0+tacc)
        #TODO this doesnt work yet!!! apparently getLAR messes up the integration.
        
        return result1[0]
    
        
        
        
        
        
if __name__ == "__main__":
    sari = Person(age=2,gender='female',Saliment=1)
    print(sari.getCED(t0=0.5,tacc=70)) #163.689
    print(sari.getCED(dt=1.0)) #213.808
    print(sari.getDorg(organ='14'))
    print(sari.getCUMLAR(organ='14'))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
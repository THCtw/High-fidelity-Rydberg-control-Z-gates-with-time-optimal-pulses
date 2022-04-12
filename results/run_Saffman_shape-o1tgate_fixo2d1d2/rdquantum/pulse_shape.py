import math
import numpy as np

def Saffman_shape(t, T_gate, num_seg, pulse_coe, phase_coe=None, conjugate=False):
    dt = T_gate/num_seg     # Duration of each segment
    ith = int( (t - dt/2) // dt )
    ti = dt/2 + dt*ith
    ti1 = ti + dt
    
    if phase_coe==None:
        phase_coe = np.zeros(len(pulse_coe))
    
    if t < dt/2 or t > (T_gate - dt/2):
        fi = pulse_coe[0]
        pi = phase_coe[0]
        pt = pi
        ft = np.exp(1j*pt) * fi

    else:
        if ith < 5:
            ith1 = ith + 1
            fi = pulse_coe[ith]
            fi1 = pulse_coe[ith1]
            pi = phase_coe[ith]
            pi1 = phase_coe[ith1]
            pt = ( (pi + pi1)/2 + ( (pi1-pi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )
            ft = np.exp(1j*pt) * ( (fi + fi1)/2 + ( (fi1-fi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )

        elif ith == 5:
            ith1 = ith
            fi = pulse_coe[ith]
            fi1 = pulse_coe[ith1]
            pi = phase_coe[ith]
            pi1 = phase_coe[ith1]
            pt = ( (pi + pi1)/2 + ( (pi1-pi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )
            ft = np.exp(1j*pt) * ( (fi + fi1)/2 + ( (fi1-fi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )

        elif ith > 5:
            ith1 = ith + 1
            fi = pulse_coe[num_seg-ith-1]
            fi1 = pulse_coe[num_seg-ith1-1]
            pi = phase_coe[num_seg-ith-1]
            pi1 = phase_coe[num_seg-ith1-1]
            pt = ( (pi + pi1)/2 + ( (pi1-pi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )
            ft = np.exp(1j*pt) * ( (fi + fi1)/2 + ( (fi1-fi)/2 ) * math.erf( (5/dt) * ( t - (ti + ti1)/2 ) ) )

    if conjugate == True:
        ft = np.conjugate(ft)

    return ft


def MS_pulse_shape(times, Tg, beta_series, n):
    n=n[0]//1
    # defined Berstein polynomial basis
    def bvn(x,n,v):  
        cvn=math.factorial(n)/math.factorial(v)/math.factorial(n-v)
        f=cvn*(x**v)*((1-x)**(n-v))
        return f
    
# create Omega1 pulse
    Omega1_t=beta_series[0]*(bvn(times/Tg,n,1)+bvn(times/Tg,n,n-1))\
            +beta_series[1]*(bvn(times/Tg,n,2)+bvn(times/Tg,n,n-2))\
            +beta_series[2]*(bvn(times/Tg,n,3)+bvn(times/Tg,n,n-3))\
            +beta_series[3]*(bvn(times/Tg,n,4)+bvn(times/Tg,n,n-4))
    return Omega1_t

# Angle Calculators
import math 
import numpy as np
import scipy 
from scipy import optimize

class Calculations():
    def __init__(self) -> None:
        pass

    def calcAngle_3pts(self,a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle >180.0:
            angle = 360-angle
        return angle 
    
    def calcAngle_2lines(self,line1, line2):        
        d1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
        d2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
        # Compute dot product
        p = d1[0] * d2[0] + d1[1] * d2[1]
        # Compute norms
        n1 = math.sqrt(d1[0] * d1[0] + d1[1] * d1[1])
        n2 = math.sqrt(d2[0] * d2[0] + d2[1] * d2[1])
        # Compute angle
        ang = math.acos(p / (n1 * n2))
        # Convert to degrees if you want
        ang = math.degrees(ang)
        return ang

    def calcAngle_Horizontal(self,point1, point2):
        """ Calculate angle of a single line """
        x_diff = point2[0] - point1[0]
        y_diff = point2[1] - point1[1]
        return math.degrees(math.atan2(y_diff, x_diff))
    
    def dist_xy(self,point1, point2):
        """ Euclidean distance between two points point1, point2 """
        diff_point1 = (point1[0] - point2[0]) ** 2
        diff_point2 = (point1[1] - point2[1]) ** 2
        return (diff_point1 + diff_point2) ** 0.5

    def point_position(self,point, line_pt_1, line_pt_2):
        """
        Left or Right position of the point from a line
        """
        value = (line_pt_2[0] - line_pt_1[0]) * (point[1] - line_pt_1[1]) - \
                    (line_pt_2[1] - line_pt_1[1]) * (point[0] - line_pt_1[0])
        if value >= 0:
            return "left"
        return "right"
    
    def fit_sin(self,tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = np.array(tt)
        yy = np.array(yy)
        ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(np.fft.fft(yy))
        guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
        guess_amp = np.std(yy) * 2.**0.5
        guess_offset = np.mean(yy)
        guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

        def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
        A, w, p, c = popt
        f = w/(2.*np.pi)
        fitfunc = lambda t: A * np.sin(w*t + p) + c
        return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}
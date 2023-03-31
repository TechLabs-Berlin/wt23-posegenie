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
   
def textGenerator(val_amp, val_minmax, val_time):
	 if abs(val_minmax - val_amp) <= 20 and val_amp > 50:
        	txtAngleComment = ' Great result! Your exercise has a harmonic rhythm, which resulted in a good fitting.'
        	txtAngleFeedback = 'A great form was detected in the metrics. Make sure to feel the exercise in your quads and hamstrings!.'
	 elif abs(val_minmax - val_amp) <= 25 and 15 <= val_amp < 50:
        	txtAngleComment = ' Great result! Your exercise has a harmonic rhythm. One or two things can be improved.'
        	txtAngleFeedback =  'A good form was detected in the metrics. You may want to focus on your flexibility and increasing range of motion. Make sure to feel the exercise in your quads and hamstrings!'
	 elif abs(val_minmax - val_amp) > 25 and 15 <= val_amp < 50:
        	txtAngleComment = ' Good result! A rhtyhm was detected in the red curve.'
        	txtAngleFeedback = ' A big difference between min and max angle, but not so great harmonicity.'
     elif abs(val_minmax - val_amp) > 25 and val_amp < 15:
        	txtAngleComment = ' Max-min angle vary, but no harmonicity detected.'
        	txtAngleFeedback = ' Something looks fishy. Please check the general guidelines and suggestions first.'

	if val_time < 1.0:
        	txtTimeComment = ' No need to rush! An optimal time period per rep would be 1-3 seconds.'
        	txtTimeFeedback = ' Try to spend more time in one rep. This will increase your endurance!'
	elif 1.0 <= val_time < 3.0:
        	txtTimeComment = ' Great timing per rep!'
        	txtTimeFeedback = ' You can increase your time per rep to increase your endurance, or use weights to add challenge!'
	elif val_time > 3.0:
        	txtTimeComment = ' You stay a bit long during each rep.'
        	txtTimeFeedback = ' As long as there is no pain, it is OK to have long reps.'
	txtMaxMin  = 'The maximum - minimum angle reached throughout the exercise is ' + str(val_minmax) + '.'
	txtFitting = 'Your harmonic angle progression throughout the exercise is ' + str(val_amp) + '.'
	txtTime = 'The time spent on one rep:' + str(val_time)

	txt1 = r"$\bf{" + 'Definition:' + "}$" + '\nHere is a recording of your hip-knee angle. When you perform a lunge exercise, your hip and knee joints move in a rhythmic pattern. This harmonic up and down motion of your joints over time can be mapped onto the curve of a sine wave. By analyzing the angle of your hip and knee joints throughout the workout and fitting a sine wave to that data, we can see how consistent your movements are and how well you are maintaining the correct form. This information can help you improve your technique and get the most out of your workouts.'
	txt2 =  r"$\bf{" + 'Analysis:' + "}$" + '\nHere I fit your recording to a sine wave. This is an estimation for your workout.\n' + txtMaxMin + txtFitting + txtAngleComment + txtTime + txtTimeComment
	txt3 = r"$\bf{" + 'Feedback:' + "}$" + "\n"+  txtAngleFeedback + txtTimeFeedback
	return txt1, txt2, txt3

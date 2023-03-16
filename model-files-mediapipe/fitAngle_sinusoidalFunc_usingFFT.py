import cv2
import mediapipe as mp
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import scipy.optimize

#################################################
#################################################

def calcAngle_3pts(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360-angle
    return angle


def calcAngle_2lines(line1, line2):
    # Get directional vectors
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
  
  def fit_sin(tt, yy):
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

#################################################
#################################################

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(sys.argv[1])

if cap.isOpened() == False:
    print("Error opening video stream or file")
    raise TypeError

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

outdir, inputflnm = sys.argv[1][:sys.argv[1].rfind(
    '/')+1], sys.argv[1][sys.argv[1].rfind('/')+1:]
inflnm, inflext = inputflnm.split('.')
out_filename = f'{outdir}{inflnm}_annotated.{inflext}'
#out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
#    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
    'm', 'p', '4', 'v'), 10, (frame_width, frame_height))

angle_list     = []
timeStamp_list = []

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        # I ll make it a one-liner soon
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        # Calculate angle
        lineRight = [right_hip, right_knee]
        lineLeft  = [left_hip, left_knee]
        angle = calcAngle_2lines(lineRight, lineLeft)
        angle_list.append(angle)
        timeStamp_list.append(round(float(cap.get(cv2.CAP_PROP_POS_MSEC))/1000, 5))


        #Add a rectangle

        # Visualize angle
        cv2.putText(image, str(np.round(angle, 2)),
                           tuple(np.multiply(right_hip, [frame_width, frame_height]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA
                                )

    except:
        pass

    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(255,255,255), thickness=3, circle_radius=3), mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
    out.write(image)

pose.close()
cap.release()
out.release()

angleTotalArray = np.array(angle_list)
timeTotalArray  = np.array(timeStamp_list)

res = fit_sin(timeStamp_list, angle_list)
#print(res["fitfunc"](timeTotalArray))
plt.plot(timeTotalArray, angleTotalArray, color="navy", label='FirstTrial', linewidth=2.0)
plt.plot(timeTotalArray, res["fitfunc"](timeTotalArray), "r-", label="y fit curve", linewidth=2)
plt.title('Lunge Progression (raw)')
plt.xlabel('Timestamp (sec)')
plt.ylabel('HipKneeAngle')
plt.show()

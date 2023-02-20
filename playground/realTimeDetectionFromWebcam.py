import mediapipe as mp
import cv2

cap=cv2.VideoCapture(0)
mp_pose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
pose=mp_pose.Pose()


while True:
           success,frame=cap.read()
           if success==False:
               break
#           frame=cam()
           frame=cv2.resize(frame,(640,480))
           rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
           result=pose.process(rgb_frame)
           mpDraw.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
           if not result.pose_landmarks:
               print("nothing")
           else:
               for id,lm in enumerate (result.pose_landmarks.landmark):
                    x=int(lm.x*640)
                    y=int(lm.y*480)
                    cv2.circle(frame,(x,y),1,(255,0,255),-1)
                    cv2.putText(frame,str(id),(x,y -1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
                    list.append([x,y])
            print(list[12])
            x1 = list[12][0]
            y1 = list[12][1]
            cv2.circle(frame,(x1,y1),5,(255,0,0),-1)
            cv2.imshow("Frame", frame);
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
stage=None
def findPosition(image, draw=True):
    lmList = []
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList

cap = cv2.VideoCapture(0)
print("No.of push_up: ",end="")
with mp_pose.Pose(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("empty camera")
            break
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        lmList = findPosition(image, draw=True)


        if len(lmList) != 0:
            if (lmList[12][2] and lmList[11][2] >= lmList[14][2] and lmList[13][2]):
                stage = "down"
            if (lmList[12][2] and lmList[11][2] <= lmList[14][2] and lmList[13][2]) and stage == "down":
                stage = "up"
                counter += 1
                print(counter,end=" ")

        cv2.imshow("push_up",cv2.flip(image,1))
        key = cv2.waitKey(1) & 0xFF
        if key == ord("e"):
            break

cv2.destroyAllWindows()


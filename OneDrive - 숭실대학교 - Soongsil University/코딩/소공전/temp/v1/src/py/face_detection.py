from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')


class FacePartDetection:

    def __init__(self,image):

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        self.image=cv2.imread(image)

        # eyebrow
        self.right_eyebrow = []
        self.left_eyebrow = []

        # eye
        self.right_eye = []
        self.left_eye = []

        # skin
        self.nose=[]
        self.left_cheek = []
        self.right_cheek = []

        self.draw_individual_detections(self.detector,self.predictor)


    def draw_individual_detections(self, detector, predictor):

        face_parts=[[],[],[],[],[],[],[],[],[]]

        # detect faces in the grayscale image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)

        # loop over the face detections
        for (i, rect) in enumerate(rects):

            
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            index=0

            for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                # clone the original image so we can draw on it, then
                # display the name of the face part on the image
                clone = self.image.copy()
                cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)

                face_parts[index]=shape[i:j]
                index+=1

                # loop over the subset of facial landmarks, drawing the
                # specific face part
                for (x, y) in shape[i:j]:
                    cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)

                    # extract the ROI of the face region as a separate image
                (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
                roi = self.image[y:y + h, x:x + w]
                roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)

                # show the particular face part
                #cv2.imshow("ROI", roi)
                #cv2.imshow("Image", clone)
                #cv2.waitKey(1000)
                #cv2.destroyAllWindows()

                # visualize all facial landmarks with a transparent overlay
            output = face_utils.visualize_facial_landmarks(self.image, shape)
                
            cv2.imshow("FINAL Image", output)
            cv2.waitKey(500)
            cv2.destroyAllWindows()

        nose=face_parts[6]
        r_eyebrow=face_parts[2]
        l_eyebrow=face_parts[3]
        r_eye=face_parts[4]
        l_eye=face_parts[5]
        l_cheek=self.image[shape[29][1]:shape[33][1], shape[4][0]:shape[48][0]]
        r_cheek=self.image[shape[29][1]:shape[33][1], shape[54][0]:shape[12][0]]

        self.right_eyebrow=self.extract_face_part(r_eyebrow)
        self.left_eyebrow = self.extract_face_part(l_eyebrow)
        self.right_eye = self.extract_face_part(r_eye)
        self.left_eye = self.extract_face_part(l_eye)
        self.left_cheek = l_cheek
        self.right_cheek = r_cheek
        self.nose=self.extract_face_part(nose)

    
    def extract_face_part(self, face_part_points):

        (x, y, w, h) = cv2.boundingRect(face_part_points)
        #print('face_part={}, x={}, y={}, w={}, h={}'.format(face_part_points,x,y,w,h))

        crop = self.image[y:y+h, x:x+w]
        adj_points = np.array([np.array([p[0]-x, p[1]-y]) for p in face_part_points])

        # Create an mask
        mask = np.zeros((crop.shape[0], crop.shape[1]))
        cv2.fillConvexPoly(mask, adj_points, 1)
        mask = mask.astype(np.bool)
        crop[np.logical_not(mask)] = [255, 0, 0]
        
        return crop


# mouth
# inner mouth
# right eyebrow
# left eyebrow
# right eye
# left eye
# nose
# jaw
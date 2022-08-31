import dlib
import numpy as np
import face_detection
import dominant_color
import exam_personal_color
import recommendation


################################
######## 1. 얼굴 인식 ##########
################################

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

image = './test_img/spring_light2.jpg'

df=face_detection.FacePartDetection(image)

face = [df.left_cheek, df.right_cheek,
        df.left_eyebrow, df.right_eyebrow,
        df.left_eye, df.right_eye,df.nose]


# 2. 색상 추출

clusters = 4

# 여기서부터 베낌
face_color = []

for face_part in face:
    dc = dominant_color.GetDominantColor(face_part, clusters)
    face_part_color, _ = dc.getHistogram()
    face_color.append(np.array(face_part_color[0]))

# skin=cheek+nose
skin = np.mean([face_color[0], face_color[1],face_color[6]], axis=0)
eyebrow = np.mean([face_color[2], face_color[3]], axis=0)
eye = np.mean([face_color[4], face_color[5]], axis=0)

print("skin", skin)
# skin [215.         199.66666667 189.        ]

# 3. 퍼스널컬러 진단

print('피부는 ',end=' ')
exam_personal_color.GetPersonalColor(skin)

# 4. 상세 정보 및 추천

recommendation.Recommendation(exam_personal_color.GetPersonalColor.personal_tone, exam_personal_color.GetPersonalColor.personal_season)



# 퍼스널컬러 웜/쿨
# 퍼스널컬러 봄/여름/가을/겨울
# 내 퍼스널컬러와 같은 퍼스널컬러를 가진 연예인
# 추천색상(입술,머리색) 
# 추천색상 화장품 보여주기
# 퍼스널컬러에 대한 간단한 설명

from pickle import NONE
import cv2
import numpy as np
from colormath.color_objects import LabColor, XYZColor, sRGBColor
from colormath.color_conversions import convert_color
import colorsys

class GetPersonalColor:

    personal_tone=NONE
    personal_season=NONE
    

    def __init__(self,RGB):
        

        # 웜톤 / 쿨톤 진단
        Lab=self.RGB_to_LAB(RGB)
        self.examine_tone(Lab)

        # 봄 / 여름 / 가을 / 겨울 진단
        HSV=self.RGB_to_HSV(RGB)
        self.examine_season(HSV)



    def RGB_to_LAB(self,RGB):
        
        R=RGB[0]
        G=RGB[1]
        B=RGB[2]

        rgb= sRGBColor(R,G,B,is_upscaled=True)
        lab= convert_color(rgb,LabColor)

        (l,a,b)=lab.get_value_tuple()
        Lab_color=[l,a,b]

        return Lab_color

    def RGB_to_HSV(self,RGB):

        R=RGB[0]
        G=RGB[1]
        B=RGB[2]

        (r, g, b) = (R, G, B)
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        print('HSV : ', h, s, v)
        HSV=[h,s,v]

        return HSV



    def examine_tone(self,face_part):

        a=face_part[1]
        b=face_part[2]


        # lab의 a값이 b보다 크면 쿨톤, 작으면 웜톤
        # 출처
        # https://koreascience.kr/article/CFKO201629368424847.pdf

        if(a>b):
            print('쿨톤입니다')
            self.personal_color='cool'
        else:
            print('웜톤입니다')
            self.personal_color='warm'

        return self.personal_color 
    


    # 봄, 여름, 가을, 겨울 판정
    # 출처
    # https://aic-color.org/resources/Documents/jaic_v1_05.pdf

    def examine_season(self,face_part):
        
        h=face_part[0]
        s=face_part[1]
        v=face_part[2]

        # 알고리즘 다시 만들어야 함..
        # 
        print("H={} ,S={}, V={}".format(h,s,v))
        if(self.personal_color=='warm'):
            
            if(v>=128):
                self.personal_season='spring'
            else:
                self.personal_season='autumn'

        else:
            self.personal_season='winter'

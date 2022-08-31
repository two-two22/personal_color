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
        print("Lab", Lab)
        personal_tone=self.examine_tone(Lab)

        # 봄 / 여름 / 가을 / 겨울 진단
        HSV=self.RGB_to_HSV(RGB)
        print("HSV", HSV)
        VbS=[(HSV[2] / 255) * 100, Lab[2], HSV[1]]
        print(VbS)
        # self.examine_season(HSV)
        personal_season = self.examine_season(VbS)


    def RGB_to_LAB(self,RGB):
        
        R=RGB[0]
        G=RGB[1]
        B=RGB[2]
        print("RGB to LAB", R, G, B)

        # is_upscaled=True 일 경우 값 범위 0-1
        # sRGBColor (rgb_r:0.8431 rgb_g:0.7830 rgb_b:0.7412)
        rgb= sRGBColor(R,G,B,is_upscaled=True)
        print(rgb)
        # LabColor (lab_l:81.4432 lab_a:3.5609 lab_b:7.2526)
        # b -128~128
        lab= convert_color(rgb,LabColor)
        print(lab)

        (l,a,b)=lab.get_value_tuple()
        # 81.4431601143589 3.5609461851980884 7.252648741303891
        print(l, a, b)
        Lab_color=[l,a,b]

        return Lab_color

    def RGB_to_HSV(self,RGB):

        R=RGB[0]
        G=RGB[1]
        B=RGB[2]

        (r, g, b) = (R, G, B)
        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        # H=0.06837606837606831 ,S=0.12093023255813953, V=215.0
        # 0-360 0-1 0-255
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

    # def examine_season(self,face_part):
    #
    #     # 보고서 - S = 0.33, V = 65.2 기준
    #     # hsv 색공간 h 0~360 s 0~100 v 0~100
    #     # https://ko.wikipedia.org/wiki/HSV_%EC%83%89_%EA%B3%B5%EA%B0%84
    #     # in OpenCV h 0~180 s 0~255 v 0~255
    #     # colorsys 모든 공간에서 좌표는 0과 1 사이
    #     # https://docs.python.org/ko/3.7/library/colorsys.html#colorsys.rgb_to_hls
    #
    #     h=face_part[0]
    #     s=face_part[1]
    #     v=face_part[2]
    #
    #     # 알고리즘 다시 만들어야 함..
    #     #
    #     print("H={} ,S={}, V={}".format(h,s,v))
    #     if(self.personal_color=='warm'):
    #
    #         if(v>=128):
    #             self.personal_season='spring'
    #         else:
    #             self.personal_season='autumn'
    #
    #     else:
    #         self.personal_season='winter'

    def examine_season(self, face_part):
        v = face_part[0]
        b = face_part[1]
        s = face_part[2]

        # 215.0 7.252648741303891 0.12093023255813953
        # scaled 84.31372549019608 7.252648741303891 0.12093023255813953
        # 255 -> 100 으로 V 범위 변경
        print("V(0~100) b(-128~128) S(0~1)", v, b, s)

        # 판단 기준  65.20 18.50 0.33

        if (self.personal_color == 'warm'):
            print("웜-")
            # high s
            if (s >= 0.27):
                # high v
                if (v >= 85):
                    print("봄 브라이트")
                    self.personal_color='spring_bright'
                else:
                    print("가을 딥")
                    self.personal_color='fall_deep'
            # low s
            else:
                # high v
                if (v >= 85):
                    print("봄 라이트")
                    self.personal_color='spring_light'
                else:
                    print("가을 뮤트")
                    self.personal_color='fall_mute'

        elif (self.personal_color == 'cool'):
            print("쿨-")
            # high s
            if (s >= 0.27):
                # high v
                if (v >= 85):
                    print("겨울 브라이트")
                    self.personal_color='winter_bright'
                else:
                    print("겨울 딥")
                    self.personal_color='winter_deep'
            # low s
            else:
                # high v
                if (v >= 85):
                    print("여름 라이트")
                    self.personal_color='summer_light'
                else:
                    print("여름 뮤트")
                    self.personal_color='summer_mute'

        return self.personal_color
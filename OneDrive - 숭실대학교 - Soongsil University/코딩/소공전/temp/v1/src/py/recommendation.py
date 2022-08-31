


class Recommendation :

    def __init__(self,personal_tone,personal_season):
        
        self.personal_tone=personal_tone
        self.personal_season=personal_season

        self.description(personal_tone, personal_season)
        self.AI_keyword(personal_tone, personal_season)
        self.recommend_palette(personal_tone, personal_season)
        self.recommend_hair(personal_tone, personal_season)
        self.recommend_cosmetics(personal_tone, personal_season)
        self.same_star(personal_tone, personal_season)

    def description(self, personal_tone, personal_season):
        print('설명')
        if (personal_tone=='warm'):
            print('웜톤의 특징')
        
    def same_star(self,personal_tone,personal_season):

        print('나의 퍼스널 컬러와 같은 연예인 찾기')


    def AI_keyword(self,personal_tone,personal_season):

        print('AI가 추천하는 키워드 나타내기')

    
    def recommend_palette(self,personal_tone,personal_color):

        print('추천하는 색상 나타내기')



    def recommend_hair(self,personal_tone,personal_color):

        print('추천하는 머리 색 나타내기')




    def recommend_cosmetics(self,personal_tone,personal_color):

        print('추천하는 화장품 나타내기')

        


    
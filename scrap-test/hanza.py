from konlpy.tag import Okt

#Okt(Open Korea Text, 이전에는 Twitter 형태소 분석기)
#Okt는 트위터에서 만든 한국어 형태소 분석기로, 한국어 텍스트를 형태소 단위로 분석해주는 도구입니다.
#Okt는 형태소 분석과 품사 태깅을 지원하며, KoNLPy 라이브러리에서 제공하는 형태소 분석기 중에서 가장 성능이 좋은 편에 속합니다.

#Okt 객체를 생성하고, pos() 메서드를 사용하면 입력한 텍스트에 대해 형태소 분석을 수행할 수 있습니다.

def extract_and_replace_nouns(text, hanja_dict):
    okt = Okt()
    words = okt.pos(text)
    result = []

    for word, pos in words:
        if pos == 'Noun' and word in hanja_dict:
            result.append(hanja_dict[word])  # 한자로 변환
        else:
            result.append(word)  # 변환하지 않고 그대로

    return ''.join(result)

# 예제
text = "자동차가 고속도로를 달리고 있다"
hanja_dict = {"자동차": "自動車", "고속도로": "高速道路"}
print(extract_and_replace_nouns(text, hanja_dict))
# 결과: "自動車가 高速道路를 달리고 있다"

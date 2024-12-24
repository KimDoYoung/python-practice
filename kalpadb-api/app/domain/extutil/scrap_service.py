from http.client import HTTPException
from bs4 import BeautifulSoup
import requests
from app.core.logger import get_logger

logger = get_logger(__name__)

class ScrapService:
    def __init__(self):
        pass

    # emoji finder
    def fetch_emojis_with_labels(self, keyword: str):
        try:
            url = f"https://emojipedia.org/ko/search?q={keyword}"
            max_count = 10  # 최대 개수
            # URL에서 HTML 가져오기
            response = requests.get(url)
            response.raise_for_status()

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 이모지 리스트를 포함하는 div를 검색 (보다 일반적인 클래스명 사용)
            emojis_wrapper = soup.find('div', class_='EmojisList_emojis-list-wrapper__A8gKQ')
            if not emojis_wrapper:
                logger.error("이모지 리스트를 포함한 적합한 div를 찾을 수 없습니다.")
                return {}

            # aria-label을 가진 a 태그 검색
            emoji_dict = {}
            anchors = emojis_wrapper.find_all('a', attrs={'aria-label': True})
            for anchor in anchors:
                label = anchor['aria-label']
                emoji = anchor.contents[0].strip()
                if label and emoji:
                    emoji_dict[label] = emoji
                if len(emoji_dict) >= max_count:  # 최대 개수 초과 시 중단
                    break

            if not emoji_dict:
                # raise HTTPException(status_code=404, detail="No emojis found.")
                return {}

            return emoji_dict

        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch the URL: {str(e)}")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
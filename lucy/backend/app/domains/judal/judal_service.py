# judal_service.py
"""
모듈 설명: 
    - judal 관련 서비스
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-08-21
버전: 1.0
"""
from typing import List
import pandas as pd
import numpy as np
import os

from backend.app.domains.judal.judal_model import JudalCsvData, JudalStock, JudalTheme, QueryCondition
from backend.app.core.logger import get_logger
from backend.app.core.exception.lucy_exception import JudalException
from backend.app.core.config import config


logger = get_logger(__name__)


class JudalService:

    async def get_my_filted_stocks(self, csv_files : list[str], query_condition: QueryCondition) -> pd.DataFrame:
        '''csv_files 목록에서 내용을 모두 가져와서 붙인다. 그리고 조건에 맞는 것을 골라서  dataframe으로 리턴'''
        dataframes = [pd.read_csv(file, dtype={'종목코드': str}) for file in csv_files]
        df = pd.concat(dataframes, ignore_index=True)

        # 필터 조건
        market = query_condition.시장종류
        if market == 'all' or market == None:
            condition1 = True
        else:
            condition1 = df['시장종류'] == query_condition.시장종류
            
        condition2 = df['시가총액'] >= query_condition.시가총액
        cost1 = query_condition.현재가[0]
        cost2 = query_condition.현재가[1]
        condition3 = (df['현재가'] >= cost1) & (df['현재가'] <= cost2)

        # 조건을 모두 만족하는 데이터 필터링
        filtered_df = df[condition1 & condition2 & condition3]

        # 결과 출력
        return filtered_df

    async def get_last_scraped_folder(self) -> str:
        '''judal 폴더하위의  가장 최근 폴더를 찾아서 반환한다.'''
        folder_path = config.DATA_FOLDER + '/judal'   # 'c:/tmp/data/judal'
        list_folder_names = os.listdir(folder_path)
        sorted_folder_names = sorted(list_folder_names, reverse=True)

        if len(sorted_folder_names) > 0:
            last_folder_name = sorted_folder_names[0]
        else:
            raise JudalException(f'{folder_path}에 데이터가 존재하지 않습니다')
        last_scraped_folder = f'{folder_path}/{last_folder_name}'
        return last_scraped_folder

    async def filtered_query(self, query_condition: QueryCondition) -> pd.DataFrame:
        ''' 조건에 맞는 주식을 찾아서 반환한다. '''
        # 가장 최신 폴더
        base_folder = await self.get_last_scraped_folder()

        # 시작하려는 테마
        # themes = ['상승중인 테마', '기대수익률 높은 테마']
        themes = query_condition.테마목록

        theme_list = []
        for theme in themes:
            csv_files = f'{base_folder}/{theme.replace(' ','_').replace('/','_')}.csv'
            df = pd.read_csv(csv_files)
            theme_list.extend(df.head(10)['테마명'])
        #print(theme_list)        
        
        csv_files=[]
        for theme in theme_list:
            csv_file = f'{base_folder}/{theme.replace(' ', '_').replace('/','_')}.csv'
            if os.path.exists(csv_file):
                csv_files.append(csv_file)
            else:
                raise JudalException(f"File {csv_file} does not exist.")

        my_df = await self.get_my_filted_stocks(csv_files, query_condition)
        return my_df

    async def get_themes(self) -> List[JudalTheme]:
        ''' 테마 목록을 가져온다. '''
        base_folder = await self.get_last_scraped_folder()
        csv_file = f'{base_folder}/theme_list.csv'
        df = pd.read_csv(csv_file)

        # DataFrame에서 pydantic 모델 리스트로 변환
        judal_theme_list: List[JudalTheme] = [JudalTheme(name=row['name'], href=row['href']) for _, row in df.iterrows()]
        return judal_theme_list

    async def get_csv_file(self, name:str) -> List[JudalCsvData]:
        ''' 테마명에 해당하는 csv 파일을 가져온다. '''
        base_folder = await self.get_last_scraped_folder()
        csv_file = f'{base_folder}/{name.replace(" ", "_")}.csv'
        df = pd.read_csv(csv_file, dtype={'종목코드': str})
        # NaN 값을 None으로 변환
        df[['PBR', 'PER', 'EPS']] = df[['PBR', 'PER', 'EPS']].replace({np.nan: None})         
        judal_csv_data_list: List[JudalCsvData] = [
            JudalCsvData(
                **{**row.to_dict(), "종목코드": str(row['종목코드'])}  # 종목코드를 문자열로 변환
            ) for _, row in df.iterrows()
        ]
        
        return judal_csv_data_list
    
    async def get_detail_themes(self) -> List[JudalTheme]:
        ''' 상세 테마 목록을 가져온다. '''
        base_folder = await self.get_last_scraped_folder()
        csv_file = f'{base_folder}/href_list.csv'
        df = pd.read_csv(csv_file)

        # DataFrame에서 pydantic 모델 리스트로 변환
        judal_theme_list: List[JudalTheme] = [JudalTheme(name=row['name'], href=row['href']) for _, row in df.iterrows()]
        return judal_theme_list
    
    async def search(self, query_condition: QueryCondition) -> List[JudalStock]:
        
        df = await self.filtered_query(query_condition)
        # NaN 값을 None으로 변환
        df[['PBR', 'PER', 'EPS']] = df[['PBR', 'PER', 'EPS']].replace({np.nan: None})        
        
        df_columns = df.columns.tolist()
        logger.debug(df_columns)
        # pydantic 모델 리스트로 변환
        # 
        columns = [ '종목명', '종목코드', '현재가', '시가총액', '시장종류', '관련테마',
                '전일비', 
                '3일합산', 
                '52주 소외지수', 
                '3년 소외지수', 
                '3년 주가지수', 
                '기대수익률', 
                'PBR', 
                'PER', 
                'EPS', 
                '당일 거래량지수', 
                '최근7일 거래량지수', 
                '등락가', 
                '52주최고', 
                '52주최저', 
                '52주변동률최저', 
                '52주변동률최고', 
                '3년최고', 
                '3년최저', 
                '3년변동률최저', 
                '3년변동률최고'  ]
        for _, row in df.iterrows():
            logger.debug(row)
        stock_info_list = [JudalStock(**row) for _, row in df[columns].iterrows()]
        # for stock in stock_info_list:
        #     print(stock)    
        return stock_info_list
    

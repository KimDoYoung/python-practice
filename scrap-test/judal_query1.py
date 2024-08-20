import pandas as pd
import glob
import os

# CSV 파일들이 있는 폴더 경로
folder_path = 'c:/tmp/data/judal/'

def get_my_filted_stocks(csv_files : list[str], query_condition: dict) -> pd.DataFrame:
    '''csv_files 목록에서 내용을 모두 가져와서 붙인다.'''
    dataframes = [pd.read_csv(file, dtype={'종목코드': str}) for file in csv_files]
    df = pd.concat(dataframes, ignore_index=True)

    # 필터 조건
    market = query_condition['시장종류']
    if market == 'all' or market == None:
        condition1 = True
    else:
        condition1 = df['시장종류'] == query_condition['시장종류']
        
    condition2 = df['시가총액'] >= query_condition['시가총액']
    cost1 = query_condition['현재가'][0]
    cost2 = query_condition['현재가'][1]
    condition3 = (df['현재가'] >= cost1) & (df['현재가'] <= cost2)

    # 조건을 모두 만족하는 데이터 필터링
    # filtered_df = df[condition1 & condition2 & condition3]
    filtered_df = df[condition1 & condition2 & condition3]

    # 결과 출력
    #print(filtered_df)
    return filtered_df

def get_last_scraped_folder() -> str:
    '''judal 폴더하위의  가장 최근 폴더를 찾아서 반환한다.'''
    folder_path = 'c:/tmp/data/judal'
    list_folder_names = os.listdir(folder_path)
    sorted_folder_names = sorted(list_folder_names, reverse=True)

    if len(sorted_folder_names) > 0:
        last_folder_name = sorted_folder_names[0]

    last_scraped_folder = f'{folder_path}/{last_folder_name}'
    return last_scraped_folder

def filtered_query(query_condition: dict) -> pd.DataFrame:
    # 데이터 불러오기
    # Specify the folder path
    base_folder = get_last_scraped_folder()
    # 시작하려는 테마
    # themes = ['상승중인 테마', '기대수익률 높은 테마']
    themes = query_condition['target_themes']

    theme_list = []
    for theme in themes:
        csv_files = f'{base_folder}/{theme.replace(' ','_').replace('/','_')}.csv'
        df = pd.read_csv(csv_files)
        theme_list.extend(df.head(10)['테마명'])
    print(theme_list)        
    
    csv_files=[]
    for theme in theme_list:
        csv_file = f'{base_folder}/{theme.replace(' ', '_').replace('/','_')}.csv'
        if os.path.exists(csv_file):
            csv_files.append(csv_file)
        else:
            print(f"File {csv_file} does not exist.")

    my_df = get_my_filted_stocks(csv_files, query_condition)
    return my_df

def main():
    query_condition = {
        "target_themes" :['상승중인 테마', '기대수익률 높은 테마'],
        '시장종류': None,
        '시가총액': 5000,
        '현재가': [15000, 35000]
    }
    df = filtered_query(query_condition)
    print(df.columns)
    print(df[['종목명', '종목코드', '현재가', '시가총액', '시장종류','관련테마']])

if __name__ == "__main__":
    main()

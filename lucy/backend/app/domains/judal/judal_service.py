

from backend.app.core.logger import get_logger

logger = get_logger(__name__)


def get_my_filted_stocks(csv_files : list[str]) -> pd.DataFrame:
    # 모든 CSV 파일의 경로를 가져오기
    #csv_files = glob.glob(folder_path + '*.csv')

    # 모든 CSV 파일을 하나의 DataFrame으로 읽어오기
    dataframes = [pd.read_csv(file, dtype={'종목코드': str}) for file in csv_files]
    df = pd.concat(dataframes, ignore_index=True)

    # 필터 조건
    #condition1 = df['시장종류'] == 'KOSPI'
    condition2 = df['시가총액'] >= 5000
    condition3 = (df['현재가'] >= 15000) & (df['현재가'] <= 35000)

    # 조건을 모두 만족하는 데이터 필터링
    # filtered_df = df[condition1 & condition2 & condition3]
    filtered_df = df[ condition2 & condition3]

    # 결과 출력
    #print(filtered_df)
    return filtered_df

def get_last_scraped_folder() -> str:
    folder_path = 'data/'
    list_folder_names = os.listdir(folder_path)
    sorted_folder_names = sorted(list_folder_names, reverse=True)

    if len(sorted_folder_names) > 0:
        last_folder_name = sorted_folder_names[0]

    last_scraped_folder = f'{folder_path}{last_folder_name}/'
    return last_scraped_folder

def filtered_query():
    # 데이터 불러오기
    # Specify the folder path
    base_folder = get_last_scraped_folder()
    # 시작하려는 테마
    themes = ['상승중인 테마', '기대수익률 높은 테마']

    theme_list = []
    for theme in themes:
        csv_files = f'{base_folder}/{theme.replace(' ','_').replace('/','_')}.csv'
        df = pd.read_csv(csv_files)
        theme_list.extend(df.head(10)['테마명'])
    print(theme_list)        
    
    csv_files=[]
    for theme in theme_list:
        csv_file = f'{base_folder}{theme.replace(' ', '_').replace('/','_')}.csv'
        if os.path.exists(csv_file):
            csv_files.append(csv_file)
        else:
            print(f"File {csv_file} does not exist.")

    my_df = get_my_filted_stocks(csv_files)
    print(my_df.columns)
    print(my_df[['종목명', '종목코드', '현재가', '시가총액', '시장종류','관련테마']])

class JudalService:
    
    async def search(self, keyvalue: dict):
        pass
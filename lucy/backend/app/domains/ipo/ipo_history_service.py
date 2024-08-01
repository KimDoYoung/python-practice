
from beanie import PydanticObjectId
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from backend.app.core.logger import get_logger
from backend.app.domains.ipo.ipo_history_model import IpoHistory

logger = get_logger(__name__)

class IpoHistoryService:
    
    async def create(self, keyvalue: dict):
        history = IpoHistory(**keyvalue)
        await history.save()
        return history
    
    async def get_all(self):
        list =  await IpoHistory.all().to_list()
        return list
    
    async def get_1(self, ipo_id: str):
        object_id = PydanticObjectId(ipo_id)
        ipo = await IpoHistory.find_one(IpoHistory.id == object_id)
        return ipo

    async def delete_1(self, ipo_id: str):
        object_id = PydanticObjectId(ipo_id)
        ipo = await IpoHistory.find_one(IpoHistory.id == object_id)
        if ipo:
            deleted_ipo = await ipo.delete()
            return deleted_ipo
        else:
            return None
    
    async def update_1(self, ipo_id:str,  ipo_history: IpoHistory):
        history = await self.get_1(ipo_id)
        if history:
            ipo_history.id = history.id
            await ipo_history.save()
            return ipo_history
        else:
            return None
    
    
    async def make_formula(self) -> str:
        ''' 회귀 모델을 학습하여 곱하기변수를 만드는 수식을 반환 '''
        list = await self.get_all()
        # Pandas DataFrame으로 변환
        df = pd.DataFrame([history.model_dump() for history in list])

        # 필요한 컬럼만 선택
        df = df[['Revenue', 'InstitutionalSubscriptionRatio', 'LockupAgreement', 'MultipleVariable']]

        # 특성과 타깃 변수 분리
        X = df[['Revenue', 'InstitutionalSubscriptionRatio', 'LockupAgreement']]
        y = df['MultipleVariable']

        # 데이터 분할 (훈련 데이터와 테스트 데이터)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 회귀 모델 학습
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 모델 평가
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logger.debug(f'Mean Squared Error: {mse}')

        # 회귀 계수 출력
        coefficients = model.coef_
        intercept = model.intercept_
        logger.debug(f'Coefficients: {coefficients}')
        logger.debug(f'Intercept: {intercept}')

        # formula = f'({coefficients[0]} * Revenue) + ({coefficients[1]} * InstitutionalSubscriptionRatio) + ({coefficients[2]} * LockupAgreement) + {intercept}'
        formula = f'({coefficients[0]} * 매출액) + ({coefficients[1]} * 기관경쟁률) + ({coefficients[2]} * 의무보유확약) + {intercept}'
        return formula
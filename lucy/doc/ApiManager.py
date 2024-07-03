from dependency import get_user_service

from abc import ABC, abstractmethod

class StockApi(ABC):
    def __init__(self, user_id, acctno):
        self.user_id = user_id
        self.acctno = acctno

    @abstractmethod  # 추상 메서드로 선언
    def get_data(self):
        pass  # 하위 클래스에서 반드시 구현해야 함

class KisApi(StockApi):
    def get_data(self):
        # KisApi specific implementation
        return f"KisApi data for user {self.user_id} and account {self.acctno}"

class LsApi(StockApi):
    def get_data(self):
        # LsApi specific implementation
        return f"LsApi data for user {self.user_id} and account {self.acctno}"

# 예시 사용 방법
kis_api = KisApi(user_id="user1", acctno="12345")
ls_api = LsApi(user_id="user2", acctno="67890")

print(kis_api.get_data())  # KisApi data for user user1 and account 12345
print(ls_api.get_data())   # LsApi data for user user2 and account 67890


class StockApi:
    def __init__(self, user_id, acctno):
        self.user_id = user_id
        self.acctno = acctno

    def get_data(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class KisApi(StockApi):
    def get_data(self):
        # KisApi specific implementation
        return f"KisApi data for user {self.user_id} and account {self.acctno}"


class LsApi(StockApi):
    def get_data(self):
        # LsApi specific implementation
        return f"LsApi data for user {self.user_id} and account {self.acctno}"


class ApiManager:
    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiManager, cls).__new__(cls)
        return cls._instance

    def new_api(self, user_id, acctno, api_type):

        #cache에 있으면 cache에서 반환
        key = (user_id, acctno, api_type)
        if key in self._cache:
            return self._cache[key]

        user_service = get_user_service()
        user = user_service.get_1(user_id)
        abbr = None
        for account in user.accounts:
            if account.acctno == acctno:
                abbr = account.abbr
                break
        
        

        if api_type == 'KisApi':
            api = KisApi(user_id, acctno)
        elif api_type == 'LsApi':
            api = LsApi(user_id, acctno)
        else:
            raise ValueError(f"Unsupported api_type: {api_type}")

        self._cache[key] = api
        return api


# Usage example
if __name__ == "__main__":
    manager = ApiManager()
    kis_api = manager.new_api('user1', 'account1', 'KisApi')
    print(kis_api.get_data())

    ls_api = manager.new_api('user2', 'account2', 'LsApi')
    print(ls_api.get_data())

    # Retrieving the cached KisApi
    cached_kis_api = manager.new_api('user1', 'account1', 'KisApi')
    print(cached_kis_api.get_data())

    # Check if the cached instance is the same as the first instance
    print(kis_api is cached_kis_api)  # Should print True

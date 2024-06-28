import asyncio

class KISTask:
    async def run(self, user_id: str):
        while True:
            # KIS 회사의 WebSocket 통신 로직
            await asyncio.sleep(1)
            print(f"KIS WebSocket task for user {user_id}")

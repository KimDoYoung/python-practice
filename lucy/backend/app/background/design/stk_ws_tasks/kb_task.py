import asyncio

class KBTask:
    async def run(self, user_id: str):
        while True:
            # KB 회사의 WebSocket 통신 로직
            await asyncio.sleep(1)
            print(f"KB WebSocket task for user {user_id}")

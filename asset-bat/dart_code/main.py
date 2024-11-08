# fetch_dart_code/main.py

import asyncio
from common.database import Database

db = Database()

async def main():
    # 데이터 조회 예시
    query = "SELECT * FROM your_table WHERE column = $1"
    data = await db.fetch(query, "value")
    print("조회 결과:", data)

    # 데이터 삽입 예시
    insert_query = "INSERT INTO your_table (column1, column2) VALUES ($1, $2)"
    await db.execute(insert_query, "value1", "value2")
    print("데이터 삽입 완료")

    # 여러 데이터 일괄 삽입 예시
    batch_values = [
        ("value3", "value4"),
        ("value5", "value6"),
        ("value7", "value8")
    ]
    await db.execute_many(insert_query, batch_values)
    print("일괄 삽입 완료")

if __name__ == "__main__":
    asyncio.run(main())


async def handle_websocket(kis_ws_url, req, input_queue):
    async with websockets.connect(kis_ws_url, ping_interval=None) as websocket:
        senddata = req.model_dump_json()
        logger.info(f"보낸데이터 : [{senddata}]")
        await websocket.send(senddata)

        aes_key = None
        aes_iv = None

        while True:
            received_text = await websocket.recv()
            logger.info("웹소켓(KIS로부터 받은 데이터) : [" + received_text + "]")
            if is_real_data(received_text):  # 실시간 데이터인 경우
                header, real_model = kis_ws_real_data_parsing(received_text, aes_key, aes_iv)
                logger.info(f"header: {header}")
                logger.info(f"real_model: {real_model}")
                await asyncio.sleep(1)
            else:  # 실시간 데이터가 아닌 경우
                try:
                    resp_json = json.loads(received_text)
                    if resp_json['header']['tr_id'] == 'PINGPONG':  # PINGPONG 데이터인 경우
                        await websocket.pong(received_text)  # 웹소켓 클라이언트에서 pong을 보냄
                        logger.debug(f"PINGPONG 데이터 전송: [{received_text}]")
                    else:
                        kis_ws_model = KisWsResponse.from_json_str(received_text)
                        aes_iv = kis_ws_model.body.output.iv if kis_ws_model.body.output.iv is not None else aes_iv
                        aes_key = kis_ws_model.body.output.key if kis_ws_model.body.output.key is not None else aes_key
                        logger.info(f"PINGPONG 아닌 것: [{received_text}]")
                        logger.debug(f"kis_ws_model: {json.dumps(kis_ws_model.model_dump(), ensure_ascii=False)}")
                except ValueError as e:
                    logger.error(f"Error parsing response: {e}")

async def user_input(input_queue):
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        choice = input(timestamp + ": Enter 'exit' to exit or '1' for 주식호가 등록 or '2' for 주식체결 등록: ")
        await input_queue.put(choice)
        if choice == 'exit':
            break

async def run():
    await init_db()
    user_service = get_user_service()
    user = await user_service.get_1("kdy987")
    
    KIS_APP_KEY = user.get_value_by_key("KIS_APP_KEY")
    KIS_APP_SECRET = user.get_value_by_key("KIS_APP_SECRET")
    KIS_HTS_USER_ID = user.get_value_by_key("KIS_HTS_USER_ID")
    kis_ws_url = 'ws://ops.koreainvestment.com:21000'
    custtype = 'P'

    ws_approval_key = await get_ws_approval_key(KIS_APP_KEY, KIS_APP_SECRET)

    print(f"ws access key :[{ws_approval_key}]")

    input_queue = asyncio.Queue()

    while True:
        user_input_task = asyncio.create_task(user_input(input_queue))
        websocket_task = asyncio.create_task(handle_websocket(kis_ws_url, KisWsRequest(
            header=Header(
                approval_key=ws_approval_key,
                personalseckey=KIS_APP_SECRET,
                custtype=custtype,
                tr_type='1'  # 기본값 설정
            ),
            body=Body(
                input=Input(
                    tr_id='H0STASP0',  # 기본값 설정
                    tr_key='005930'
                )
            )
        ), input_queue))

        done, pending = await asyncio.wait(
            [user_input_task, websocket_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        choice = await input_queue.get()
        if choice == 'exit':
            break

        stk_code = '005930'
        if choice == '1':  # 주식호가 등록
            tr_id = 'H0STASP0'
            tr_type = '1'
        elif choice == '2':  # 주식체결 등록
            tr_id = 'H0STCNT0'
            tr_type = '1'
        else:
            print('잘못된 입력입니다.')
            continue

        req = KisWsRequest(
            header=Header(
                approval_key=ws_approval_key,
                personalseckey=KIS_APP_SECRET,
                custtype=custtype,
                tr_type=tr_type
            ),
            body=Body(
                input=Input(
                    tr_id=tr_id,
                    tr_key=stk_code
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(run())

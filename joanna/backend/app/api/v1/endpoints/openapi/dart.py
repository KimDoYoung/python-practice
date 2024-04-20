from io import BytesIO
from zipfile import ZipFile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from backend.app.core.logger import get_logger
from backend.app.domains.openapi.appkey_model import AppKey, AppKeyBase
from backend.app.domains.openapi.appkey_service import AppKeyService
from backend.app.domains.openapi.dart_model import DartCorpCode
from backend.app.core.dependencies import get_appkey_service, get_dart_service, get_db
from backend.app.core.template_engine import render_template
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from xml.etree.ElementTree import parse


logger = get_logger(__name__)

router = APIRouter()

template_base = "openapi/dart"

@router.get("/openapi/dart/corp_code", response_class=HTMLResponse)
async def dart_corp_code_form(searchText: str = None, 
                                session: AsyncSession = Depends(get_db), 
                                dart_service = Depends(get_dart_service)):
    '''
    DART 기업개황정보
    '''
    logger.debug("DART 기업개황정보 폼 display")
    if searchText:
        logger.debug(f"검색어: {searchText}")
        list = dart_service.get_all(session, searchText)

    context = {searchText: searchText, "corp_list": list}
    return render_template(f"{template_base}/corp_code.html", context)

@router.post("/openapi/dart/corp_code")
async def dart_corp_code_fill_db(session = Depends(get_db), 
            appkey_service = Depends(get_appkey_service),
            dart_service = Depends(get_dart_service)):

    base = AppKeyBase(user_id="kdy987", key_name="DART-OPENKEY")
    found_app_key = await appkey_service.get(base, session)
    crtfc_key = found_app_key.key_value
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={crtfc_key}"
    
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to download the corpCode file")
            # 파일을 메모리에 다운로드
            data = BytesIO(await response.read())
    
# ZIP 파일 열기
    with ZipFile(data, 'r') as zip_file:
        with zip_file.open('CORPCODE.xml') as xml_file:
            tree = parse(xml_file)
            root = tree.getroot()
            
    app_key_service = AppKeyService()

    # XML 데이터를 AppKey 모델로 변환하고 데이터베이스에 저장
    for corp in root.findall('./list'):
        corp_code = corp.find('corp_code').text
        corp_name = corp.find('corp_name').text
        stock_code = corp.find('stock_code').text.strip() or None
        modify_date = corp.find('modify_date').text
        
        dart = DartCorpCode(corp_code=corp_code, corp_name=corp_name, stock_code=stock_code, modify_date=modify_date)
        try:
            await dart_service.insert_corp_code(dart, session)
        except HTTPException as e:
            if e.status_code == 409:  # 이미 존재하는 키 업데이트
                await dart_service.update(dart, session)

    return {"status": "success", "message": "Data processed successfully"}

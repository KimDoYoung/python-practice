from io import BytesIO
import json
from zipfile import ZipFile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
import requests
from backend.app.core.logger import get_logger
from backend.app.domains.user.appkey_model import AppKey, AppKeyBase
from backend.app.domains.user.appkey_service import AppKeyService
from backend.app.domains.openapi.dart_model import DartCorpCode
from backend.app.core.dependencies import get_appkey_service, get_dart_service, get_db
from backend.app.core.template_engine import render_template
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from xml.etree.ElementTree import parse

from backend.app.domains.query_attr_model import QueryAttr


logger = get_logger(__name__)

router = APIRouter()

template_base = "openapi/dart"
@router.get("/openapi/dart/form", response_class=HTMLResponse, include_in_schema=False)
async def openapi_dart_form(template: str = None):
    ''' DART 관련 메뉴 또는 요청 폼을 표시합니다.'''
    if template is None:
        template = "menu"
    else:
        template = f"templates/{template}"   

    template_full_path = f"{template_base}/{template}.html" 
    logger.debug("template_full_path: %s", template_full_path)
    return render_template(template_full_path, {})

@router.get("/openapi/dart/jaemu")
async def dart_jaemu(
            corp_code: str,
            bsns_year: str,
            reprt_code: str,
            session: AsyncSession = Depends(get_db),
            appkey_service = Depends(get_appkey_service),
            dart_service = Depends(get_dart_service)
            ):
    '''
    DART 재무 정보 조회
    '''
    base = AppKeyBase(user_id="kdy987", key_name="DART-OPENKEY")
    found_app_key = await appkey_service.get(base, session)
    crtfc_key = found_app_key.key_value
    #raise HTTPException(status_code=500, detail="Server Error")
    params = {
        "crtfc_key": crtfc_key,
        "corp_code": corp_code,
        "bsns_year": bsns_year,
        "reprt_code": reprt_code
    }
    url = f"https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
    logger.debug("DART 재무 정보 조회: %s", url)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # 성공적으로 데이터를 받았을 때
        context = response.json()
    else:
        # 요청 실패 처리
        logger.error(f"Failed to retrieve data: {response.status_code}")
        context = {"message": "error"}
    logger.debug(json.dumps(context, indent=4, sort_keys=True))
    return context

@router.get("/openapi/dart/company")
async def dart_company(
            corp_code: str,
            session: AsyncSession = Depends(get_db),
            appkey_service = Depends(get_appkey_service),
            dart_service = Depends(get_dart_service)
            ):
    '''
    DART 회사 정보 조회
    '''
    base = AppKeyBase(user_id="kdy987", key_name="DART-OPENKEY")
    found_app_key = await appkey_service.get(base, session)
    crtfc_key = found_app_key.key_value
    #raise HTTPException(status_code=500, detail="Server Error")
    url = f"https://opendart.fss.or.kr/api/company.json?crtfc_key={crtfc_key}&corp_code={corp_code}"
    logger.debug("DART 회사 정보 조회: %s", url)
    response = requests.get(url)
    if response.status_code == 200:
        # 성공적으로 데이터를 받았을 때
        context = response.json()
    else:
        # 요청 실패 처리
        logger.error(f"Failed to retrieve data: {response.status_code}")
        context = {"message": "error"}
    
    return context
    

@router.post("/openapi/dart/corp_code")
async def dart_corp_code_form(queryAttr: QueryAttr, 
                                session: AsyncSession = Depends(get_db), 
                                dart_service = Depends(get_dart_service)):
    '''
    DART 기업 코드 조회
    '''
    logger.debug("DART 기업 코드 조회 시작: searchText=%s, limit=%d, skip=%d", queryAttr.searchText, queryAttr.limit, queryAttr.skip)
    try:
        corp_list = await dart_service.get_all(session, queryAttr.searchText, queryAttr.skip, queryAttr.limit + 1)
        context = {
            "searchText": queryAttr.searchText,
            "corp_list": corp_list[:queryAttr.limit],  # 한 페이지에 보여줄 항목만 전달
            "limit": queryAttr.limit,
            "skip": queryAttr.skip,
            "next": len(corp_list) > queryAttr.limit  # 다음 페이지 존재 여부
        }
    except Exception as e: 
        logger.error("DART 기업 코드 조회 중 에러 발생: %s", str(e))
        raise HTTPException(status_code=500, detail="Server Error")
    
    return context

@router.post("/openapi/dart/batch/corp_code")
async def dart_corp_code_fill_db(session = Depends(get_db), 
            appkey_service = Depends(get_appkey_service),
            dart_service = Depends(get_dart_service)):
    """
    DART 기업코드 데이터베이스에 저장
    """
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

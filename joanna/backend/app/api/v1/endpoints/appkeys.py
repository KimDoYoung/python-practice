import json
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession  # Import the missing AsyncSession class

from backend.app.core.template_engine import render_template
from backend.app.core.dependencies import get_appkey_service, get_db
from backend.app.domains.user.appkey_model import AppKey, AppKeyBase
from backend.app.core.logger import get_logger
from backend.app.core.exceptions.joanna_exceptions import JoannaException


router = APIRouter()

logger  = get_logger(__name__)

@router.get("/appkeys/form", response_class=HTMLResponse, include_in_schema=False)
async def appkeys_form(request: Request,mode: str = None, user_id: str = None, key_name: str = None) -> HTMLResponse:
    '''화면을 출력 '''
    data = {}
    if mode is None:
        mode = "list"
    elif mode == "update":
        mode = "update"
        data = {"user_id": user_id, "key_name": key_name}
    return render_template(f"appkeys/{mode}.html", data)

@router.delete("/appkeys/{user_id}/{key_name}")
async def appkeys_get_all(user_id: str, key_name: str, 
        session: AsyncSession = Depends(get_db),
        appkey_service = Depends(get_appkey_service)):
    ''' appkeys 레코드  삭제'''
    appkeybase = AppKeyBase(user_id=user_id, key_name=key_name)
    try:
        await appkey_service.delete(appkeybase, session)
    except JoannaException as http_exc:
        logger.error(str(http_exc.detail))
        raise HTTPException(status_code=http_exc.status_code, detail=str(http_exc.detail))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"result": "success"}

@router.get("/appkeys/{user_id}/{key_name}")
async def appkeys_get_1(user_id:str,key_name:str,
                    session: AsyncSession = Depends(get_db),
                    appkey_service = Depends(get_appkey_service)):
    ''' appkeys 레코드 1개 조회'''
    appkeybase = AppKeyBase(user_id=user_id, key_name=key_name)
    try:
        appkey = await appkey_service.get(appkeybase, session)
        appkey_dict = appkey.to_dict()
        logger.debug("appkey_dict: %s", appkey.to_string())
        return JSONResponse(content={"result": "success", "appkey": appkey_dict})
    except JoannaException as http_exc:
        logger.error(str(http_exc.detail))
        raise HTTPException(status_code=http_exc.status_code, detail=str(http_exc.detail))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/appkeys")
async def appkeys_get_all(session: AsyncSession = Depends(get_db),
        appkey_service = Depends(get_appkey_service),):
    ''' 모든 appkeys를 조회한다.'''

    appkey_list = await appkey_service.get_all(session)
    #json_data = {"result": "success", "list": appkey_list}
    #return { "list":list }
    #return JSONResponse(content={"result": "success", "list": appkey_list})
    return {"list" : appkey_list}

@router.post("/appkeys")
async def appkeys_insert( appkey : AppKey,  session: AsyncSession = Depends(get_db),
        appkey_service = Depends(get_appkey_service),):
    ''' 키 저장'''
    try:
        inserted_appkey = await appkey_service.insert(appkey, session)
        json = inserted_appkey.to_json()
        logger.debug("inserted_appkey: %s", json)
        return JSONResponse(content={"result": "success", "appkey": json})
    except JoannaException as http_exc:
        logger.error(str(http_exc.detail))
        raise HTTPException(status_code=http_exc.status_code, detail=str(http_exc.detail))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    

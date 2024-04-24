import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession  # Import the missing AsyncSession class

from backend.app.core.template_engine import render_template
from backend.app.core.dependencies import get_appkey_service, get_db
from backend.app.domains.user.appkey_model import AppKey


router = APIRouter()

@router.get("/appkeys/form", response_class=HTMLResponse, include_in_schema=False)
async def appkeys_form(request: Request,mode: str = None):
    ''' 키 관리 메인'''
    if mode is None:
        mode = "list"
    return render_template(f"appkeys/{mode}.html", {})

@router.get("/appkeys")
async def appkeys(session: AsyncSession = Depends(get_db),
        appkey_service = Depends(get_appkey_service),):
    ''' 키 관리 메인'''
    list = await appkey_service.get_all(session)
    
    return { "list":list }

@router.post("/appkeys")
async def appkeys( appkey : AppKey,  session: AsyncSession = Depends(get_db),
        appkey_service = Depends(get_appkey_service),):
    ''' 키 관리 메인'''
    appkey = await appkey_service.insert(appkey, session);
    
    return { "result" : "success", "appkey": json.dumps(appkey) }
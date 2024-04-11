# MVC style

## 특징

1. request를 받으면 htmlresponse를 한다.
2. service, model, routes(api=controller) 로 나누어서 사용한다.
3. async db조작을 한다

## folder structure

* 기본 구조
* create_folder_mvc.sh 실행

```text
.
|-- README.md
|-- api
|   `-- v1
|       `-- home_routes.py
|-- core
|   |-- config.py
|   |-- database.py
|   |-- exceptions.py
|   |-- logger.py
|   |-- template_engine.py
|   `-- util.py
|-- models
|-- services
|-- static
|   |-- css
|   |-- image
|   `-- js
`-- templates
```

## core folder 파일들

### config.py

* 환경변수는 {projectName}**_MODE**로 한다

```python
# config.py
from dotenv import load_dotenv
import os

# 현재 환경에 맞는 .env 파일을 로드하는 함수
# def load_environment(env_mode):
#     dotenv_path = f'.env.{env_mode}'
#     load_dotenv(dotenv_path=dotenv_path)

# 환경 변수를 통해 현재 모드를 결정
env_mode = os.getenv('SOFIA_MODE', 'local')
print("=====================================  env_mode  =====================================")
print(f"env_mode: {env_mode}")
print("=====================================  env_mode  =====================================")
# load_environment(env_mode)
PROJECT_NAME="SOFIA"


if env_mode == "local":
    LOG_FILE = f"c:\\tmp\\logs\\{PROJECT_NAME.lower()}\\{PROJECT_NAME.lower()}.log"
else:  
    LOG_FILE=f"/logs/{PROJECT_NAME.lower()}/{PROJECT_NAME.lower()}.log"

# 로그파일폴더가 존재하지 않으면 생성
log_dir = os.path.dirname(LOG_FILE)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
```

### database.sh

* SQLAlchemy 사용을 전제로 한다
* 데이터베이스 연결을 만든다.
  * AsyncSessionLocal 변수 생성
  * DB_URL이 Async를 지원하도록 만드는 것에 주의

  ```python
  AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
  ```

* 필요시 데이터베이스를 생성한다.

    ```python
    engine = create_async_engine(DB_URL, echo=True, future=True)
    ```

### dependencies.py

* router에서 사용할 db와 service의 dependency들을 만든다.
  
```python
from sqlalchemy.ext.asyncio import AsyncSession
from typing import  AsyncGenerator

from core.database import AsyncSessionLocal
from services.image_file_service import ImageFileService
from services.image_folder_service import ImageFolderService
from core.logger import get_logger

logger = get_logger(__name__)

#
# 데이터베이스 dependency
#
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("----> Creating DB session.")
    db: AsyncSession = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        logger.debug("----> DB session closed.")

#
# Service dependencies
#
def get_folder_service() -> ImageFolderService:
    return ImageFolderService()

def get_file_service() -> ImageFileService:
    return ImageFileService()

logger.debug("----> Dependencies created.")
# db_dependency = Annotated[AsyncSession, Depends(get_db)]
# folder_service_dependency = Annotated[ImageFolderService, Depends(get_folder_service)]
# file_service_dependency = Annotated[ImageFileService, Depends(get_file_service)]
```

### exceptions.py

* 비지니스 로직 Exception 정의
  
```python
class SofiaError(Exception):
    """Sofia 애플리케이션에서 발생하는 기본 예외"""
    pass

class RestfulError(SofiaError):
    """Restful API에서 발생하는 예외"""
    def __init__(self, detail: str = None):
        self.detail = detail or "Restful API에서 오류가 발생했습니다."
        super().__init__(self.detail)

class FolderNotFoundError(RestfulError):
    """폴더가 존재하지 않을 때 발생하는 예외"""
    def __init__(self, detail: str = "폴더가 존재하지 않습니다."):
        super().__init__(detail)
```

### logger.py

* profile에 따라서 log level변경
* profile에 따라서 log의 위치변경 즉 local은  console에도 write
* real에서는  error 레벨만 그리고 파일에만  기록
* logger = get_logger(**name**)로 사용
  
  ```python
    import logging
    from logging.handlers import RotatingFileHandler
    import os

    from core.config import LOG_FILE


    def get_logger(name):

        # LOG_FILE의 디렉토리 경로를 얻음
        log_dir = os.path.dirname(LOG_FILE)

        # 해당 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logger = logging.getLogger(name)
        SOFIA_MODE = 'local'
        if SOFIA_MODE == "local":
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)

        if not logger.handlers:
            # 매일 자정에 로그 파일을 회전, 최대 7개의 파일 보관
            # 파일의 최대 크기는 예시로 10MB로 설정하였습니다. 필요에 따라 조절하십시오.
            file_handler = RotatingFileHandler(LOG_FILE, "a", 10*1024*1024, 7)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            if SOFIA_MODE == "local":
                # 콘솔에도 로그 메시지 출력
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

        return logger
  ```

### template_engine.py
  
* jinja2를 베이스로 한다.
* 기본 {% %}, {{ }} => (% %), (( )) 로 변환해서 사용
* router에서 render_template 함수로 사용
  
```python
    import os
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    from core.logger import get_logger

    logger = get_logger(__name__)

    # 프로젝트 루트 디렉토리를 기반으로 템플릿 디렉토리 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(BASE_DIR, 'templates')
    logger.debug("------------------------------------------------")
    logger.debug(f"template_dir: {template_dir}")
    logger.debug("------------------------------------------------")
    # Jinja2 환경 설정
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))'
    )

    def render_template(template_name, context):
        template = env.get_template(template_name)
        return template.render(context)
```

### util.py

* 자주 사용하는 함수들 모음

## models folder

* 데이터베이스의 테이블에 해당하는 파일들을 만든다.
* 테이블 갯수 만큼 만든다
* class로 만든다.
* sqlmodel로 만들어서 SQLAlchemy와 pydantic을 동시에 지원하게 한다.
* **table=True** 가 중요함. 실제로 데이터베이스 물리적 파일에 적용되는 것은 이것이 선언된 class여야함

  ```python
    from datetime import datetime
    from typing import List, Optional
    from sqlmodel import SQLModel, Field

    from models.image_file_model import ImageFile, ImageFileBase

    class ImageFolderBase(SQLModel):
        folder_name: str
        folder_path: str
        last_load_time: Optional[datetime] = None
        note:  Optional[str] = None

    class ImageFolder(ImageFolderBase, table=True):
        __tablename__ = 'image_folders'
        id: Optional[int] = Field(default=None, primary_key=True)
        last_load_time: datetime = Field(sa_column_kwargs={"default": datetime.now, "nullable": False})

    class ImageFolderCreate(ImageFolderBase):
        pass

    class ImageFolderUpdate(ImageFolderBase):
        folder_name: Optional[str] = None
        last_load_time: Optional[datetime] = None
        note: Optional[str] = None

    class ImageFolderWithFiles(ImageFolderBase):
        files : Optional[List[ImageFile]] = None
  
  ```

## service 폴더

* 기본적으로 테이블 갯수만큼 class로 만든다.
* 각 class는 CRUD를 갖는다.

```python
from fastapi import HTTPException
from sqlalchemy.future import select 
from models.image_file_model import ImageFile
from models.image_folder_model import ImageFolderWithFiles, ImageFolder, ImageFolderCreate

from sqlalchemy.ext.asyncio import AsyncSession

class ImageFolderService:

    async def create(self, folder: ImageFolderCreate, db: AsyncSession) -> ImageFolder:
        new_folder = ImageFolder(**folder.model_dump())
        db.add(new_folder)
        await db.commit()
        await db.refresh(new_folder)
        return new_folder
    
    async def get(self, folder_id: int, session: AsyncSession) -> ImageFolderWithFiles:
        statement = select(ImageFolder).where(ImageFolder.id == folder_id)
        result = await session.execute(statement)
        folder = result.scalars().first()
        if not folder:
            raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")
        folder_and_files = ImageFolderWithFiles(**folder.__dict__)
        statement = select(ImageFile).where(ImageFile.folder_id == folder_id).order_by(ImageFile.seq.asc())
        files = await session.execute(statement)
        folder_and_files.files = files.scalars().all()
        return folder_and_files

    async def get_all(self, session: AsyncSession) -> list[ImageFolder]:
        statement = select(ImageFolder).order_by(ImageFolder.id.desc()) # 최신순으로 정렬
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def delete(self, folder_id: int, session: AsyncSession) -> ImageFolder:
        async with session.begin():  # 트랜잭션 시작
            result = await session.execute(select(ImageFolder).where(ImageFolder.id == folder_id))
            folder_to_delete = result.scalars().first()

            if not folder_to_delete:
                raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")

            # 데이터 삭제
            await session.delete(folder_to_delete)

            # 변경 사항을 데이터베이스에 커밋
            await session.commit()

            # 삭제된 폴더 객체 반환
            return folder_to_delete
    
    async def get_folder_path(self, folder_id : int, session: AsyncSession) -> str:
        '''
        folder_id에 해당하는 폴더의 경로를 반환
        '''
        statement = select(ImageFolder.folder_path).where(ImageFolder.id == folder_id)
        result = await session.execute(statement)
        if not result:
            raise HTTPException(status_code=404, detail=f"Folder with id {folder_id} not found")
        return result.scalars().first()
```

### Transaction

* db는 AsyncSession임
* ImageFolder 즉 table=true로 선언된 객체
* add는 await가 안씀
* flush는 commit이 아니지만 반영하라는 뜻
* refresh는 반영된 레코드를 가져오라는 뜻 즉 자동으로 생긴 id를 가져온다
* async with db.begin(): 으로 감싸면 모든 것이 끝나고 commit함 그래서 commit생략
  
```python

    async with db.begin():
        new_folder = ImageFolder(**folder.model_dump())
        db.add(new_folder)
        await db.flush()
        await db.refresh(new_folder)
        new_folder_id = new_folder.id
        for idx, file_name in enumerate(files):
            image_file = ImageFile(org_name=file_name, seq=idx+10, folder_id=new_folder_id)
            db.add(image_file)
```

### select, delete, update

* statement를 만들고, excecute한다 라는 개념으로 되어 있음

  ```python
        statement = select(ImageFolder).order_by(ImageFolder.id.desc()) # 최신순으로 정렬
        result = await session.execute(statement)
        return result.scalars().all()
  ```

### router 폴더

* db와 service를 Depends로 가져온다.
* **=**을 써서 default 값을 설정한다. 즉 인자 뒤에 써야한다
* response 타입을 정해줄 수 있다.
* 이때 주의 cookie값을 설정하면 cookie값이 설정되지 않는다.

```python
    @router.get("/folders/{folder_id}", response_class=HTMLResponse)
    async def get_folder(request: Request, folder_id: int,thumb: bool = False, db = Depends(get_db), service= Depends(get_folder_service) ):
        folder = await service.get(folder_id, db)
        folder_json = folder.model_dump()
        logger.debug(f"folder_json: {folder_json}")
        context = {"request": request,  "folder": folder_json}
        return render_template("view.html", context)
```

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"Hello": "World"}


def configure(dev_mode: bool):
    pass
    # configure_templates(dev_mode)
    # configure_routes()
    # configure_db(dev_mode)

def configure_db(dev_mode: bool):
    pass
    # file = (Path(__file__).parent / 'db' / 'pypi.sqlite').absolute()
    # db_session.global_init(file.as_posix())


def configure_templates(dev_mode: bool):
    pass
    # fastapi_chameleon.global_init('templates', auto_reload=dev_mode)


def configure_routes():
    pass
    # app.mount('/static', StaticFiles(directory='static'), name='static')
    # app.include_router(home.router)
    # app.include_router(account.router)
    # app.include_router(packages.router)

if __name__ == '__main__':
    main()
else:
    configure(dev_mode=False)

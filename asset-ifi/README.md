# asset-api 와 asset-bat 

## 설명

- asset-api와 asset-bat 2개의 프로젝트가 있음.
- asset-api
  - api서비스 제공
  - scheduling cron으로 동작
  - 외부 사이트 interface
- asset-bat
  - asset-api의 scheduling에의해서 호출되는 프로그램들

## 업데이트 절차

- asset-api와 asset-bat는 각각의 docker image로 만들어짐
- asset-api와 asset-bat는 각각의 docker container로 실행됨

- asset-api만 빌드 및 실행할 경우

```shell
docker-compose build asset_api
docker-compose up -d asset_api
```

- asset-bat만 빌디 및 실행할 경우

```shell
docker-compose build asset_bat
docker-compose up -d asset_bat
```
# kofic_schema.py
"""
모듈 설명: 
    - 영화진흥위원회 open API 응답 스키마를 정의합니다.
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-12-21
버전: 1.0
"""
from pydantic import BaseModel
from typing import List, Optional

#--------------------------------------------------------
# 에러 메세지
#--------------------------------------------------------
class FaultInfo(BaseModel):
    message: str  # 오류 메시지
    errorCode: str  # 오류 코드

class KoficErrorResponse(BaseModel):
    faultInfo: FaultInfo    
#--------------------------------------------------------
# search schema 영화목록
#--------------------------------------------------------
class Director(BaseModel):
    peopleNm: Optional[str]  # 감독명


class Company(BaseModel):
    companyCd: Optional[str]  # 제작사 코드
    companyNm: Optional[str]  # 제작사명


class Movie(BaseModel):
    movieCd: str  # 영화 코드
    movieNm: str  # 영화명(국문)
    movieNmEn: Optional[str]  # 영화명(영문)
    prdtYear: Optional[str]  # 제작연도
    openDt: Optional[str]  # 개봉일
    typeNm: Optional[str]  # 영화유형
    prdtStatNm: Optional[str]  # 제작상태
    nationAlt: Optional[str]  # 제작국가(전체)
    genreAlt: Optional[str]  # 영화장르(전체)
    repNationNm: Optional[str]  # 대표 제작국가명
    repGenreNm: Optional[str]  # 대표 장르명
    directors: List[Director]  # 영화감독 리스트
    companys: List[Company]  # 제작사 리스트


class MovieListResult(BaseModel):
    totCnt: int  # 총 영화 수
    source: str  # 출처
    movieList: List[Movie]  # 영화 리스트


class KoficSearchResponse(BaseModel):
    movieListResult: MovieListResult

#--------------------------------------------------------
# detail schema 영화 상세정보
#--------------------------------------------------------

class Nation(BaseModel):
    nationNm: Optional[str]  # 제작국가명

class Genre(BaseModel):
    genreNm: Optional[str]  # 장르명

class Director(BaseModel):
    peopleNm: Optional[str]  # 감독명
    peopleNmEn: Optional[str]  # 감독명(영문)

class Actor(BaseModel):
    peopleNm: Optional[str]  # 배우명
    peopleNmEn: Optional[str]  # 배우명(영문)
    cast: Optional[str]  # 배역명
    castEn: Optional[str]  # 배역명(영문)

class ShowType(BaseModel):
    showTypeGroupNm: Optional[str]  # 상영형태 구분
    showTypeNm: Optional[str]  # 상영형태명

class Audit(BaseModel):
    auditNo: Optional[str]  # 심의번호
    watchGradeNm: Optional[str]  # 관람등급 명칭

class Company(BaseModel):
    companyCd: Optional[str]  # 참여 영화사 코드
    companyNm: Optional[str]  # 참여 영화사명
    companyNmEn: Optional[str]  # 참여 영화사명(영문)
    companyPartNm: Optional[str]  # 참여 영화사 분야명

class Staff(BaseModel):
    peopleNm: Optional[str]  # 스텝명
    peopleNmEn: Optional[str]  # 스텝명(영문)
    staffRoleNm: Optional[str]  # 스텝역할명

class MovieInfo(BaseModel):
    movieCd: str  # 영화 코드
    movieNm: str  # 영화명(국문)
    movieNmEn: Optional[str]  # 영화명(영문)
    movieNmOg: Optional[str]  # 영화명(원문)
    showTm: Optional[str]  # 상영시간
    prdtYear: Optional[str]  # 제작연도
    openDt: Optional[str]  # 개봉일
    prdtStatNm: Optional[str]  # 제작상태명
    typeNm: Optional[str]  # 영화유형명
    nations: List[Nation]  # 제작국가 리스트
    genres: List[Genre]  # 장르 리스트
    directors: List[Director]  # 감독 리스트
    actors: List[Actor]  # 배우 리스트
    showTypes: List[ShowType]  # 상영형태 리스트
    audits: List[Audit]  # 심의정보 리스트
    companys: List[Company]  # 참여 영화사 리스트
    staffs: List[Staff]  # 스텝 리스트

class MovieInfoResult(BaseModel):
    movieInfo: MovieInfo  # 영화 정보
    source: str  # 출처
    class Config:
        extra = 'allow'  # 추가 필드 허용    

class KoficDetailResponse(BaseModel):
    movieInfoResult: MovieInfoResult
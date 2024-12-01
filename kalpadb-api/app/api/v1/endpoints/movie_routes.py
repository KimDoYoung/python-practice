from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.movie.movie_schema import MovieListResponse, MovieSearchRequest
from app.domain.movie.movie_service import MovieService


router = APIRouter()

@router.get("/movies", response_model=MovieListResponse)
async def get_movies(
    search_text: str = None,
    nara: str = None,
    category: str = None,
    gamdok: str = None,
    make_year: str = None,
    start_index: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """영화 목록 조회"""
    request = MovieSearchRequest(
        search_text=search_text,
        nara=nara,
        category=category,
        gamdok=gamdok,
        make_year=make_year,
        start_index=start_index,
        limit=limit
    )
    service = MovieService(db)
    return await service.get_movies(request)

@router.get("/movies", response_model=MovieListResponse)
async def get_movie_review(
    search_text: str = None,
    nara: str = None,
    year: str = None,
    lvl: str = None,
    start_ymd: str = None,
    end_ymd: str = None,
    start_index: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)
):
    """영화감상 목록 조회"""
    request = MovieSearchRequest(
        search_text=search_text,
        nara=nara,
        year=year,
        lvl=lvl,
        start_ymd=start_ymd,
        end_ymd=end_ymd,
        start_index=start_index,
        limit=limit
    )
    service = MovieService(db)
    return await service.get_movie_reviews(request)
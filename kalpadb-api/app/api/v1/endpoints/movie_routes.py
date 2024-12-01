from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.movie.movie_schema import MovieListResponse, MovieSearchRequest
from app.domain.movie.movie_service import MovieService


router = APIRouter()

@router.get("/movies", response_model=MovieListResponse)
async def get_movies(request: MovieSearchRequest, db: AsyncSession = Depends(get_session)):
    """영화 목록 조회"""
    service = MovieService(db)
    return await service.get_movies(request)

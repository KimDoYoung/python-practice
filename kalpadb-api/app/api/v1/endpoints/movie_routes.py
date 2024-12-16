from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.movie.movie_schema import MovieListResponse, MovieRequest, MovieResponse, MovieSearchRequest
from app.domain.movie.movie_service import MovieService
from app.domain.movie_review.moviereview_schema import MovieReviewListResponse, MovieReviewResponse, MovieReviewSearchRequest, MovieReviewUpsertRequest
from app.domain.movie_review.moviereview_service import MovieReviewService


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

@router.get("/movies/{id}", summary="특정 ID로 영화DVD 정보 조회", response_model=MovieResponse)
async def update_movie(id:int,  db: AsyncSession = Depends(get_session)):
    """특정 ID로 영화 정보 조회"""
    service = MovieService(db)
    return await service.get_movie(id)


@router.post("/movies/{id}", summary="영화DVD정보를 수정",response_model=MovieResponse)
async def update_movie(id:int, req: MovieRequest,  db: AsyncSession = Depends(get_session)):
    """영화 생성 또는 수정"""
    service = MovieService(db)
    return await service.update_movie(id, req)

@router.get("/movie_reviews", response_model=MovieReviewListResponse)
async def get_movie_review(
    search_text: str = None,
    nara: str = None,
    year: str = None,
    lvl: str = None,
    start_ymd: str = None,
    end_ymd: str = None,
    start_index: int = 0,
    limit: int = 10,
    include_content: bool = False,
    db: AsyncSession = Depends(get_session)
):
    """영화감상 목록 조회"""
    request = MovieReviewSearchRequest(
        search_text=search_text,
        nara=nara,
        year=year,
        lvl=lvl,
        start_ymd=start_ymd,
        end_ymd=end_ymd,
        start_index=start_index,
        limit=limit,
        include_content=include_content
    )
    service = MovieReviewService(db)
    return await service.get_movie_reviews(request)

@router.post("/movie_review", response_model=MovieReviewResponse)
async def upsert_movie_review(
    request: MovieReviewUpsertRequest,
    db: AsyncSession = Depends(get_session)
):
    """영화감상 생성 또는 수정"""
    service = MovieReviewService(db)
    return await service.upsert_movie_review(request)

@router.get("/movie_review/{movie_id}", response_model=MovieReviewResponse)
async def get_movie_review_by_id(movie_id:int, db: AsyncSession = Depends(get_session)):
    """영화감상 상세(1개) 조회"""
    service = MovieReviewService(db)
    return await service.get_movie_review(movie_id)

@router.delete("/movie_review/{movie_id}", response_model=MovieReviewResponse)
async def delete_movie_review(movie_id:int, db: AsyncSession = Depends(get_session)):
    """영화감상 삭제 """
    service = MovieReviewService(db)
    return await service.delete_movie_review(movie_id)
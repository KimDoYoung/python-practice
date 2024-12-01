from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import and_, delete

from app.domain.movie.movie_model import Movie
from app.domain.movie.movie_schema import MovieListResponse, MovieRequest, MovieResponse, MovieSearchRequest

class MovieService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movie(self, movie_id: int) -> MovieResponse:
        """특정 ID로 영화 정보 조회"""
        result = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            raise NoResultFound(f"Movie with ID {movie_id} not found")
        return MovieResponse.model_validate(movie)

    async def get_movies(self, request: MovieSearchRequest) -> MovieListResponse:
        """검색 조건과 페이징을 기반으로 영화 목록 조회"""
        query = select(Movie).where(
            and_(
                (Movie.gubun == request.gubun if request.gubun else True),
                (Movie.title1title2.like(f"%{request.search_text}%") if request.search_text else True),
                (Movie.nara == request.nara if request.nara else True),
                (Movie.category == request.category if request.category else True),
                (Movie.gamdok == request.gamdok if request.gamdok else True),
                (Movie.make_year == request.make_year if request.make_year else True),
            )
        ).order_by(Movie.id).limit(request.limit + 1).offset(request.start_index)

        # 데이터 조회
        result = await self.db.execute(query)
        movies = result.scalars().all()

        # 다음 데이터 존재 여부 확인
        next_data_exists = len(movies) > request.limit

        # 실제 반환할 데이터 (limit에 맞춰 자르기)
        movies_to_return = movies[:request.limit]

        return MovieListResponse(
            list=[MovieResponse.model_validate(movie) for movie in movies_to_return],
            item_count=len(movies_to_return) + (1 if next_data_exists else 0),
            next_data_exists=next_data_exists,
            next_index=request.start_index + len(movies_to_return),
        )


    async def create_movie(self, movie_data: MovieRequest) -> MovieResponse:
        """영화 데이터 생성"""
        movie = Movie(**movie_data.dict())
        self.db.add(movie)
        await self.db.commit()
        await self.db.refresh(movie)
        return MovieResponse.from_orm(movie)

    async def update_movie(self, movie_id: int, movie_data: MovieRequest) -> MovieResponse:
        """영화 데이터 수정"""
        result = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            raise NoResultFound(f"Movie with ID {movie_id} not found")
        
        for key, value in movie_data.dict(exclude_unset=True).items():
            setattr(movie, key, value)
        self.db.add(movie)
        await self.db.commit()
        await self.db.refresh(movie)
        return MovieResponse.from_orm(movie)

    async def delete_movie(self, movie_id: int) -> None:
        """영화 데이터 삭제"""
        result = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            raise NoResultFound(f"Movie with ID {movie_id} not found")
        
        await self.db.execute(delete(Movie).where(Movie.id == movie_id))
        await self.db.commit()

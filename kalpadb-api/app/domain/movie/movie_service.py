from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.domain.movie.movie_model import Movie
from app.domain.movie.movie_schema import MovieRequest, MovieResponse

class MovieService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movie(self, movie_id: int) -> MovieResponse:
        """특정 ID로 영화 정보 조회"""
        result = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            raise NoResultFound(f"Movie with ID {movie_id} not found")
        return MovieResponse.from_orm(movie)

    async def get_movies(self) -> list[MovieResponse]:
        """모든 영화 정보 조회"""
        result = await self.db.execute(select(Movie)) 
        movies = result.scalars().all()
        return [MovieResponse.from_orm(movie) for movie in movies]

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

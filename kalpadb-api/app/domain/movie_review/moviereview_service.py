from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.models.movie_review_model import MovieReview
from app.schemas.movie_review_schema import MovieReviewRequest, MovieReviewResponse

class MovieReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movie_review(self, review_id: int) -> MovieReviewResponse:
        """특정 ID로 리뷰 조회"""
        result = await self.db.execute(select(MovieReview).where(MovieReview.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            raise NoResultFound(f"MovieReview with ID {review_id} not found")
        return MovieReviewResponse.from_orm(review)

    async def get_movie_reviews(self) -> list[MovieReviewResponse]:
        """모든 리뷰 조회"""
        result = await self.db.execute(select(MovieReview))
        reviews = result.scalars().all()
        return [MovieReviewResponse.from_orm(review) for review in reviews]

    async def create_movie_review(self, review_data: MovieReviewRequest) -> MovieReviewResponse:
        """리뷰 생성"""
        review = MovieReview(**review_data.dict())
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return MovieReviewResponse.from_orm(review)

    async def update_movie_review(self, review_id: int, review_data: MovieReviewRequest) -> MovieReviewResponse:
        """리뷰 수정"""
        result = await self.db.execute(select(MovieReview).where(MovieReview.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            raise NoResultFound(f"MovieReview with ID {review_id} not found")
        
        for key, value in review_data.dict(exclude_unset=True).items():
            setattr(review, key, value)
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return MovieReviewResponse.from_orm(review)

    async def delete_movie_review(self, review_id: int) -> None:
        """리뷰 삭제"""
        result = await self.db.execute(select(MovieReview).where(MovieReview.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            raise NoResultFound(f"MovieReview with ID {review_id} not found")
        
        await self.db.execute(delete(MovieReview).where(MovieReview.id == review_id))
        await self.db.commit()

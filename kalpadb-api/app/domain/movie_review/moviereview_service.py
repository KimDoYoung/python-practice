from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import and_, delete

from app.domain.movie_review import MovieReview
from app.domain.movie_review import MovieReviewRequest, MovieReviewResponse
from app.domain.movie_review.moviereview_schema import MovieReviewListResponse, MovieReviewSearchRequest

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

    async def get_movie_reviews(self, request: MovieReviewSearchRequest) -> MovieReviewListResponse:
        """
        검색 조건과 페이징을 기반으로 영화 리뷰 목록 조회
        """
        # limit + 1로 데이터 조회
        query = select(MovieReview).where(
            and_(
                (MovieReview.title.like(f"%{request.search_text}%") if request.search_text else True),
                (MovieReview.nara == request.nara if request.nara else True),
                (MovieReview.year == request.year if request.year else True),
                (MovieReview.lvl == request.lvl if request.lvl else True),
                (MovieReview.ymd.between(request.start_ymd, request.end_ymd) if request.start_ymd and request.end_ymd else True),
            )
        ).order_by(MovieReview.ymd.desc()).limit(request.limit + 1).offset(request.start_index)

        # 데이터 조회
        result = await self.db.execute(query)
        reviews = result.scalars().all()

        # 다음 데이터 존재 여부 확인
        next_data_exists = len(reviews) > request.limit

        # 실제 반환할 데이터 (limit에 맞춰 자르기)
        reviews_to_return = reviews[:request.limit]

        return MovieReviewListResponse(
            list=[MovieReviewResponse.from_orm(review) for review in reviews_to_return],
            item_count=len(reviews_to_return) + (1 if next_data_exists else 0),
            next_data_exists=next_data_exists,
            next_index=request.start_index + len(reviews_to_return),
        )

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

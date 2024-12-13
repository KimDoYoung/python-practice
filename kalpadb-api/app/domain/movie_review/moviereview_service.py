from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import and_, delete

from app.domain.movie_review.moviereview_model import MovieReview
from app.domain.movie_review.moviereview_schema import MovieReviewRequest, MovieReviewResponse
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
        return MovieReviewResponse.model_validate(review)

    async def get_movie_reviews(self, request: MovieReviewSearchRequest) -> MovieReviewListResponse:
        """
        검색 조건과 페이징을 기반으로 영화 리뷰 목록 조회
        """
        # 동적으로 필드를 선택
        selected_fields = [
            MovieReview.id,
            MovieReview.title,
            MovieReview.nara,
            MovieReview.year,
            MovieReview.lvl,
            MovieReview.ymd,
        ]

        # content 필드 포함 여부
        if request.include_content:
            selected_fields.append(MovieReview.content)

        # 쿼리 작성
        query = select(*selected_fields).where(
            and_(
                (MovieReview.title.like(f"%{request.search_text}%") if request.search_text else True),
                (MovieReview.nara == request.nara if request.nara else True),
                (MovieReview.year == request.year if request.year else True),
                (MovieReview.lvl == request.lvl if request.lvl else True),
                (MovieReview.ymd.between(request.start_ymd, request.end_ymd) if request.start_ymd and request.end_ymd else True),
            )
        ).order_by(MovieReview.ymd.desc()).limit(request.limit + 1).offset(request.start_index)

        # 데이터 실행 및 변환
        result = await self.db.execute(query)
        rows = result.all()

        # 컬럼 이름 추출
        column_names = [field.key for field in selected_fields]

        # 데이터 변환
        reviews = []
        for row in rows:
            review_data = dict(zip(column_names, row))
            reviews.append(MovieReviewResponse(**review_data))
            
        next_data_exists = 'Y' if len(rows) > request.limit else 'N'
        reviews = reviews[:request.limit]
        # 응답 반환
        return MovieReviewListResponse(
            list=reviews,
            item_count=len(reviews),
            next_data_exists=next_data_exists,
            start_index=request.start_index,
            next_index=request.start_index + len(reviews),
        )

    async def upsert_movie_review(self,  review_data: MovieReviewRequest) -> MovieReviewResponse:
        """ movie_review_id가 존재하면 update아니면 insert 리뷰 생성"""
        movie_review_id = review_data.id
        if movie_review_id:
            return await self.update_movie_review(movie_review_id, review_data)
        else:
            return await self.create_movie_review(review_data)        

    async def create_movie_review(self, review_data: MovieReviewRequest) -> MovieReviewResponse:
        """리뷰 생성"""
        review = MovieReview(**review_data.model_dump())
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return MovieReviewResponse.model_validate(review)

    async def update_movie_review(self, review_id: int, review_data: MovieReviewRequest) -> MovieReviewResponse:
        """리뷰 수정"""
        result = await self.db.execute(select(MovieReview).where(MovieReview.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            raise NoResultFound(f"MovieReview with ID {review_id} not found")
        
        for key, value in review_data.model_dump(exclude_unset=True).items():
            setattr(review, key, value)
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return MovieReviewResponse.model_validate(review)

    async def delete_movie_review(self, review_id: int) -> MovieReviewResponse:
        """리뷰 삭제"""
        result = await self.db.execute(select(MovieReview).where(MovieReview.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            raise NoResultFound(f"MovieReview with ID {review_id} not found")
        
        deleted_movie_review = MovieReviewResponse.model_validate(review)

        await self.db.execute(delete(MovieReview).where(MovieReview.id == review_id))
        await self.db.commit()

        return deleted_movie_review
    
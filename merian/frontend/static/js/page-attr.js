class PageAttr {
    constructor(totalItemCount, pageSize = 10, currentPageNumber = 1) {
        this.totalItemCount = totalItemCount;
        this.pageSize = pageSize;
        this.currentPageNumber = currentPageNumber;
        this.pageNumberSize = 10; // 한 번에 표시할 페이지 번호의 개수

        // 초기값 설정
        this.offset = 0;
        this.limit = this.pageSize;
        this.totalPageCount = 0;
        this.startPageNumber = 0;
        this.endPageNumber = 0;
        this.isExistPrevPageNumber = false;
        this.isExistNextPageNumber = false;

        // 계산 메소드 실행
        this.calculate();
    }

    calculate() {
        // 총 페이지 수 계산
        this.totalPageCount = Math.ceil(this.totalItemCount / this.pageSize);

        // 현재 페이지 번호 검증
        if (this.currentPageNumber < 1) {
            this.currentPageNumber = 1;
        } else if (this.currentPageNumber > this.totalPageCount) {
            this.currentPageNumber = this.totalPageCount;
        }

        // offset, limit 설정
        this.offset = (this.currentPageNumber - 1) * this.pageSize;
        this.limit = this.pageSize;

        // 시작 페이지 번호와 끝 페이지 번호 계산
        this.startPageNumber = Math.floor((this.currentPageNumber - 1) / this.pageNumberSize) * this.pageNumberSize + 1;
        this.endPageNumber = Math.min(this.startPageNumber + this.pageNumberSize - 1, this.totalPageCount);

        // 이전/다음 페이지 존재 여부
        this.isExistPrevPageNumber = this.currentPageNumber > 1;
        this.isExistNextPageNumber = this.currentPageNumber < this.totalPageCount;
    }
}

module.exports = PageAttr;


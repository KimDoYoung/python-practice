// import PageAttr from '../page-attr'; // 상대 경로는 실제 파일 위치에 따라 달라질 수 있습니다.
const PageAttr = require('../../frontend/static/js/page-attr');

describe('PageAttr', () => {
    let pageAttr;

    beforeEach(() => {
        pageAttr = new PageAttr(100, 10, 1);
    });

    test('should calculate the total number of pages correctly', () => {
        expect(pageAttr.totalPageCount).toBe(10);
    });

    test('should calculate the total number of pages correctly when totalItemCount is not divisible by pageSize', () => {
        pageAttr = new PageAttr(105, 10, 1);
        expect(pageAttr.totalPageCount).toBe(11);
    });

    test('should calculate the current page correctly', () => {
        expect(pageAttr.currentPageNumber).toBe(1);
    });

    test('should update the current page correctly', () => {
        pageAttr.currentPageNumber = 5;
        expect(pageAttr.currentPageNumber).toBe(5);
    });

    test('offset 테스트 ', () => {
        pageAttr = new PageAttr(105, 10, 2);
        expect(pageAttr.offset).toBe(10);
    });
});


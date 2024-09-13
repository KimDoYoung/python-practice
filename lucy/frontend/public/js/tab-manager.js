/*
 * TabManager 클래스
- TabManager 클래스는 탭을 관리하는 기능을 제공하는 클래스입니다.
- 주의) jquery, bootstrap.js, bootstrap.css가 필요합니다.

- 사용법
const tabManager = new TabManager('#tab-area');
const tab1 = tabManager.addTab('tab1', '삼성전자1');
const tab2 = tabManager.addTab('tab2', '삼성전자2');
const lorem = 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Natus adipisci dolorum molestias, repudiandae, perspiciatis cumque vitae inventore similique maxime magni pariatur tempore ad officia recusandae corrupti aliquam necessitatibus cum deleniti';
tabManager.addTabContent(tab1, `<h1>삼성전자1</h1><p>${lorem}</p>`);
tabManager.addTabContent(tab2, `<div id="chart1" class="bg-danger">111</div>`);
$content = tabManager.getTabContent(tab2);
$content.find('#chart1').click(function() {
    alert('chart1 clicked');
});
// TabManager 초기화
const tabManager = new TabManager("#tabs");
tabManager.addTab('tab1', '첫 번째 탭');
tabManager.addTab('tab2', '두 번째 탭');
tabManager.addTabContent('tab1', '<p>첫 번째 탭의 새로운 컨텐츠</p>');
tabManager.selectTab('tab1');
console.log(tabManager.getTitle('tab1')); // '첫 번째 탭'
console.log(tabManager.getTabContent('tab1').html()); 
 */

class TabManager {
    constructor(selector) {
        this.tabArea = $(selector);
        if (!this.tabArea.length) {
            console.error("Tab area not found: " + selector);
            return;
        }

        this.tabList = $('<ul class="nav nav-tabs" role="tablist"></ul>');
        this.tabContent = $('<div class="tab-content"></div>');
        this.tabArea.append(this.tabList).append(this.tabContent);
        this.seq = 0; // "새로운"으로 시작하는 탭 제목의 일련번호 추적

        // 한 번만 고유한 해시를 생성하여 모든 tabId에 사용
        this.hashSuffix = Math.random().toString(36).substr(2, 9); // 고유한 해시 생성
    }

    // uniqueTabId 생성기: tabId + hashSuffix
    getUniqueTabId(tabId) {
        return `${tabId}-${this.hashSuffix}`;  // 고유한 tabId를 해시와 결합
    }

    getTabCount() {
        return this.tabList.children().length;
    }
    getTabSeq() {
        return this.seq;
    }
    // 탭 추가 함수
    addTab(tabId, title, onClickCallback) {
        const uniqueTabId = this.getUniqueTabId(tabId); // hashSuffix + tabId 결합
        if (this.getTab(uniqueTabId).length === 0) { // 동일한 ID가 이미 존재하는지 확인
            if (!title){
                title = '새로운 ' + (++this.seq); // 제목이 없으면 새로운 + 일련번호로 설정
            }else{
                title = title.trim(); // 제목이 있으면 앞뒤 공백 제거
                this.seq++; // 일련번호 증가
            }

            const newTab = $(`<li class="nav-item">
                                <a class="nav-link" data-toggle="tab" href="#${uniqueTabId}">
                                    ${title} <span class="close" style="cursor:pointer;">&times;</span>
                                </a>
                            </li>`);
            const newTabContent = $(`<div class="tab-pane fade" id="${uniqueTabId}">${title} 내용</div>`);

            this.tabList.append(newTab);
            this.tabContent.append(newTabContent);

            // 탭 클릭 시 선택 및 콜백 연결
            newTab.find('a').on('click', () => {
                this.selectTab(tabId);
                if (onClickCallback && typeof onClickCallback === 'function') {
                    onClickCallback(tabId, title);
                }
            });

            // 닫기 버튼 클릭 시 탭 제거
            newTab.find('.close').on('click', () => this.removeTab(tabId));
        } else {
            console.warn(`Tab with ID '${tabId}' already exists.`);
        }
        return tabId;
    }

    // 탭 제거 함수
    removeTab(tabId) {
        const uniqueTabId = this.getUniqueTabId(tabId);
        this.getTab(tabId).parent().remove();  // 탭 목록에서 제거
        if (uniqueTabId) {
            this.tabContent.find(`#${uniqueTabId}`).remove();  // 컨텐츠에서 제거
        } else {
            console.warn(`No tab found with ID '${tabId}'.`);
        }
    }

    // ID로 탭 찾기
    getTab(tabId) {
        const uniqueTabId = this.getUniqueTabId(tabId);
        return this.tabList.find(`a[href="#${uniqueTabId}"]`);
    }

    // 탭 선택 함수
    selectTab(tabId) {
        const tab = this.getTab(tabId);
        if (tab.length > 0) {
            tab.tab('show');  // 탭이 존재하면 선택
        } else {
            console.warn(`Tab with ID '${tabId}' does not exist.`);
        }
    }

    // 모든 탭 닫기 함수
    closeAllTabs() {
        this.tabList.children().each((_, elem) => {
            const uniqueTabId = $(elem).find('a').attr('href').substring(1);
            this.removeTab(uniqueTabId);
        });
    }

    // 특정 ID의 탭 제목 반환
    getTitle(tabId) {
        const tab = this.getTab(tabId);
        return tab.length ? tab.contents().not(tab.children()).text().trim() : null;
    }

    // 탭의 컨텐츠에 HTML 삽입
    addTabContent(tabId, htmlContent) {
        const uniqueTabId = this.getUniqueTabId(tabId);
        const tabContent = this.tabContent.find(`#${uniqueTabId}`);
        if (tabContent.length > 0) {
            tabContent.html(htmlContent);
            return tabContent; // 컨텐츠를 담고 있는 container 반환
        } else {
            console.warn(`No tab content area found for ID '${tabId}'.`);
            return null; // 컨테이너가 없을 경우 null 반환
        }
    }

    // 특정 ID의 탭 컨텐츠 반환
    getTabContent(tabId) {
        const uniqueTabId = this.getUniqueTabId(tabId);
        const tabContent = this.tabContent.find(`#${uniqueTabId}`);
        return tabContent.length > 0 ? tabContent : null;
    }
}

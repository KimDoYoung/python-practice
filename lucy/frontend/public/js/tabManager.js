function TabManager(selector) {
    this.tabArea = $(selector);
    this.tabList = $('<ul class="nav nav-tabs" role="tablist"></ul>');
    this.tabContent = $('<div class="tab-content"></div>');
    this.tabArea.append(this.tabList).append(this.tabContent);
    this.seq = 0; // "새로운"으로 시작하는 탭 제목의 일련번호 추적

    this.addTab = function(id, title, onClickCallback) {
        if(this.getTab(id).length === 0) { // 동일한 ID가 이미 존재하는지 확인
            if(title === undefined) {
                this.seq++; // "새로운" 탭의 일련번호 증가
                title = '새로운 ' + this.seq; // 제목이 undefined일 경우 자동 생성
            }
            var newTab = $('<li class="nav-item"><a class="nav-link" data-toggle="tab" href="#' + id + '">' + title + ' <span class="close" style="cursor:pointer;">&times;</span></a></li>');
            var newTabContent = $('<div class="tab-pane fade" id="' + id + '">' + title + ' 내용</div>');

            this.tabList.append(newTab);
            this.tabContent.append(newTabContent);

			newTab.find('a[href="#' + id + '"]').click(() => {
			    this.selectTab(id);
			});			
            newTab.find('.close').click(() => this.removeTab(id));
            if (typeof onClickCallback === 'function') {
                onClickCallback(id, title);
            }
        } else {
            console.warn("Tab with ID '" + id + "' already exists.");
        }
    };

    this.removeTab = function(id) {
        $('#' + id).remove();
        this.tabList.find('a[href="#' + id + '"]').parent().remove();
    };

    this.getTab = function(id) {
        return this.tabList.find('a[href="#' + id + '"]');
    };

    this.selectTab = function(id, title, onClickCallback) {
        var tab = this.getTab(id);
        if(tab.length > 0) {
            tab.tab('show'); // 탭이 존재하면 선택
        } else {
            this.addTab(id, title, onClickCallback); // 탭이 존재하지 않으면 새로 추가
            this.getTab(id).tab('show'); // 추가된 탭을 선택
        }
    };

    this.closeAllTabs = function() {
        this.tabList.children().each((index, elem) => {
            var id = $(elem).find('a').attr('href').substring(1);
            this.removeTab(id);
        });
    };

    this.getTitle = function(id) {
        // id에 해당하는 탭의 제목을 반환합니다.
        var tab = this.tabList.find('a[href="#' + id + '"]');
        if (tab.length > 0) {
            return tab.contents().not(tab.children()).text().trim(); // 닫기 버튼의 텍스트를 제외하고 탭의 제목만 반환
        } else {
            return null; // 해당 ID를 가진 탭이 없는 경우
        }
    };
}
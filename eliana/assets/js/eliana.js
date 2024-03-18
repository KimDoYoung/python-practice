var defaultResult = {
    url : 'http://localhost:8989/assets/image/noimage.png',
    title : 'Not Avable'
};

//처음 페이지
function init_chart_html(){
    // aside 크기 토글 버튼
    $('#toggleSidebar').click(function() {
        $('#sidebar').toggleClass('w-64 w-16');
        $('.sidebar-link, #menuText').toggle(); // 메뉴명 표시 전환
    });
    // aside 메뉴클릭 
    $('.menu-form').on('click', function(e){
        e.stopPropagation();
        var chart_type = $(this).data('chart-type');
        var url = "/form/" + chart_type;
        JuliaUtil.ajax(url,{}, {
            success : function(response){
                var html = response.template;
                $('#chart-page').html(html);
                init_chart_form_html();
            }
        })
    });
    
}
//차트 테스트 오른쪽 화면 
function init_chart_form_html(){
    //탭 click
    $('#right-area .tab').click(function() {
        var tabId = $(this).attr('class').split(' ')[1]; // 클릭한 탭의 class에서 식별자 추출

        // 모든 탭 컨텐츠 숨기기
        $('.tab-content').addClass('hidden');

        // 클릭한 탭에 해당하는 컨텐츠만 보이기
        $('.content-' + tabId.split('-')[1]).removeClass('hidden');

        // 모든 탭의 활성화 상태 제거
        $('.tab').removeClass('bg-blue-500 text-white');

        // 현재 탭 활성화
        $(this).addClass('bg-blue-500 text-white');
    });
    //샘플이 콥보 선택시
    $('#sample-select').on('change', function(e){
        e.stopPropagation();
        $('#messageArea').hide();
        var id = $(this).val();
        if(id == false) return;
        var url = "/sample/"+id;
        JuliaUtil.ajax(url,{}, {
            method : 'GET',
            success : function(response){
                var json = response.jsonData;
                $('#json-data').val(json);
            },
            error : function(xhr){
                var error = xhr.responseJSON.message.error;
                $('#messageArea').show().html(error);
            }
        })
    });
    //챠트생성 버튼 click
    $('#btnCreateChart').on('click',function(){
        var chart_type = $(this).data('chart-type');
        var url = "/chart/"+chart_type;
        var jsonStr = $('#json-data').val();
        var jsonObject = undefined;
        //json객체가 맞는가?
        try {
            jsonObject = JSON.parse(jsonStr);    
        } catch (error) {
            showResult(defaultResult);
            $('#messageArea').show().html('Json데이터 검증 실패: '+ xhr.responseJSON.message);
            return;
        }
        //검증
        var errors = validationFunctions[chart_type](jsonObject);
        if( errors.length > 0){
            var listItems = errors.map(function(error) {
                return `<li>${error}</li>`; 
            }).join(''); 
        
            var html =  `<ul>${listItems}</ul>`; // 전체를 ul 태그로 감싼다.
            $('#messageArea').show().html(html);
            return;
        }

        JuliaUtil.ajax(url,jsonObject, {
            method : 'POST',
            success : function(response){
                //debugger;
                //$('#resultChart').show();
                $('#messageArea').hide()
                var data = {url : response.url, title: response.url};
                showResult(data);
            },
            error : function(xhr){
                showResult(defaultResult);
                var error = xhr.responseJSON.message.error;
                $('#messageArea').show().html(error);
            }
        })
    });

    $('#btnClear').on('click', function(){
        $('#messageArea').hide();
        $('#sample-select').val('');

        $('#json-data').val('');
        showResult(defaultResult);
    });

    function showResult(data){
        $('#resultChart').find("a").attr("href", data.url);
        $('#resultChart').find("a").text(data.url);
        $('#resultChart').find("img").attr("src", data.url);
    }

    // 기본적으로 첫 번째 탭 활성화
    $('.tab-charts').click(); 
    showResult(defaultResult); 

}

//샘플 리스트 화면
function init_sample_list_html(){
    $('#btnSampleInsert').on('click', function(e){
        e.stopPropagation();
        var url = "/sample/insert/form";
        JuliaUtil.ajax(url,{}, {
            success : function(response){
                var html = response.template;
                $('#page').html(html);
                init_sample_form_html();
            }
        })
        
    });
    $('.btn-delete').on('click', function(e){
        e.stopPropagation();
        if(confirm('삭제하시겠습니까?') == false) return;
        var id = $(this).data('id');
        var url = "/sample/delete/" + id
        JuliaUtil.ajax(url,{}, {
            method:'DELETE',
            success : function(response){
                var html = response.template;
                $('a[data-url="sample"]').trigger('click');
            },
            error : function(xhr){
                //debugger;
                console.log(xhr.responseJSON.message);
                alert(xhr.responseJSON.message);
            }
        })        
    });
    $('.btn-edit').on('click', function(e){
        e.stopPropagation();
        var id = $(this).data('id');
        var url = "/sample/edit/form/" + id
        JuliaUtil.ajax(url,{}, {
            method:'GET',
            success : function(response){
                var html = response.template;
                $('#page').html(html);
                init_sample_edit_html();
            },
            error : function(xhr){
                //debugger;
                console.log(xhr.responseJSON.message);
                alert(xhr.responseJSON.message);
            }
        })        
    });    
}
//샘플 입력(insert) 화면
function init_sample_form_html(){
    //error 표시영역 감추기
    $('#messageArea').hide();
    //저장 insert버튼 클릭
    $('#chartForm').submit(function(){
        console.log('form submit...');
        var url = "/sample/insert";
        var data = {
            chart_type : $('#chartType').val(),
            title : $('#title').val(),
            json_data : $('#jsonData').val(),
            note : $('#chartDescription').val()
        };
        console.log(data)
        JuliaUtil.ajax(url,data, {
            method:'POST',
            success : function(response){
                $('a[data-url="sample"]').trigger('click');
            }, 
            error : function(xhr){
                $('#messageArea').show().html(xhr.responseJSON.message);
            }
        })  
        return false;
    });
    //목록으로 돌아가기
    $('#btnCancel').on('click',function(){
        $('a[data-url="sample"]').trigger('click');
    });
}

//샘플 수정(edit=update) 화면
function init_sample_edit_html(){
    console.log("sample edit initialize...");
    $('#messageArea').hide();
    $('#sampleEditForm').on('submit', function(){
        console.log("sample eidt submit...");
        var id = $('#chartId').val();
        var url = "/sample/edit/" + id;
        var data = {
            chart_type : $('#chartType').val(),
            title : $('#title').val(),
            json_data : $('#jsonData').val(),
            note : $('#chartDescription').val(),
        };
 
        JuliaUtil.ajax(url,data, {
            method:'POST',
            success : function(response){
                $('a[data-url="sample"]').trigger('click');
            }, 
            error : function(xhr){
                $('#messageArea').show().html(xhr.responseJSON.message);
            }
        })     
        return false;
    });
    //취소 버튼 클릭
    $('#btnCancel').on('click', function(){
        $('a[data-url="sample"]').trigger('click');
    });

}
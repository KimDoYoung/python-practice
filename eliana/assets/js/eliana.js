
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
    // 기본적으로 첫 번째 탭 활성화
    $('.tab-charts').click();  

}

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
                console.log(xhr);
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
                console.log(xhr);
            }
        })        
    });    
}

function init_sample_form_html(){
    $('#chartForm').submit(function(){
        console.log('form submit...');
        var url = "/sample/insert";
        var data = {
            chart_type : $('#chartType').val(),
            title : $('#title').val(),
            json : $('#jsonData').val(),
            note : $('#chartDescription').val(),
        };
        JuliaUtil.ajax(url,data, {
            method:'POST',
            success : function(response){
                var html = response.template;
                $('#page').html(html);
                init_sample_edit_html();
            }, 
            error : function(xhr){
                debugger;
                console.log(xhr);
            }
        })  
        return false;
    });
}
function init_sample_edit_html(){
    console.log("sample edit initialize...");
    $('#sampleEditForm').on('submit', function(){
        console.log("sample eidt submit...");
        $('#messageArea').hide();
        var url = "/sample/edit";
        var data = {
            id : $('#chartId').val(),
            chart_type : $('#chartType').val(),
            title : $('#title').val(),
            json : $('#jsonData').val(),
            note : $('#chartDescription').val(),
        };
        // debugger;
        // console.log(data);
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
    })
}
//웹소켓을 연결한다.
//window.ws에 저장하여 전역에서 사용할 수 있도록 한다.
if (!window.ws) {
    window.ws = new WebSocket("ws://localhost:8000/ws");
}

window.ws.onmessage = function(event) {
    //WS으로 메세지를 받음
    console.log(event.data)    
    var $messages = $('#messages');
    if ($messages) {
        var $message = $('<li>');
        var content = document.createTextNode(event.data);
        $message.append(content);
        $messages.append($message);
    }
    var $alertContainer = $('#alert-container');
    var $alert = $('<div class="alert alert-warning alert-dismissible fade show" role="alert">')
        .text(event.data)
        .append('<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>');
    $alertContainer.append($alert);    
};

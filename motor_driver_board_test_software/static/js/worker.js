self.addEventListener('message', function(e) {
    var message = e.data;
    var console;
    // 检查消息类型并执行相应操作
    if (message.type === 'type1') {
        // 处理类型1的消息
        // 在这里执行 AJAX 请求
        if (message.data === 'Console 1') {
            console = message.data;
        } else if (message.data === 'Console 2') {
            console = message.data;
        }
        fetch('/qrcode/' + console, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            // 将结果发送回主线程
            self.postMessage({ type: 'type1', data: data });
        })
        .catch(error => {
            console.error('Error in AJAX request:', error);
        })
    } else if (message.type === 'type2') {
        // 处理类型2的消息
        // 在这里执行 AJAX 请求
        if (message.data === 'Console 1') {
            console = message.data;
        } else if (message.data === 'Console 2') {
            console = message.data;
        }
        fetch('/board_test/' + console, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            // 将结果发送回主线程
            self.postMessage({ type: 'type2', data: data });
        })
        .catch(error => {
            console.error('Error in AJAX request:', error);
        })
    }
});

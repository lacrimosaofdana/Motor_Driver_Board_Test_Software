$(document).ready(function () {
    $('#button1').click(function () {
        if (confirm('开始扫码吗?')) {
            // 点击确认按钮时，执行AJAX请求
            // 点击按钮时，显示"读取中"信息
            $('#message1').replaceWith('<div class="spinner-border flex-shrink-0 me-2" role="status" aria-hidden="true" id="message1"></div>');

            $.ajax({
                url: '/qrcode',
                type: 'POST',
                success: function (response) {
                    // 当服务器返回结果时，这个函数会被调用
                    var messageHtml = `
                                                    <div class="table-responsive">
                                                    <table class="table table-striped table-sm">
                                                    <thead>
                                                    <tr>
                                                        <th scope="col">条码信息</th>
                                                        <th scope="col">电流/A</th>
                                                        <th scope="col">电压/V</th>
                                                        <th scope="col">功率/W</th>
                                                        <th scope="col">转速/PCS</th>
                                                        <th scope="col">测试时间</th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    <tr>
                                                        <td>${response}</td>
                                                        <td>～</td>
                                                        <td>～</td>
                                                        <td>～</td>
                                                        <td>～</td>
                                                        <td>～</td>
                                                    </tr>
                                                    </tbody>
                                                    </table>
                                                    </div>
                                                `;
                    $('#message3').html(messageHtml);
                    $('#message1').replaceWith('<div class="spinner-grow text-success flex-shrink-0 me-2" role="status" id="message1"></div>');
                    $('#message2').replaceWith('<div class="spinner-border flex-shrink-0 me-2" role="status" aria-hidden="true" id="message2"></div>');

                    $.ajax({
                        url: '/board_test',
                        type: 'POST',
                        success: function (response) {
                            // 当服务器返回结果时，这个函数会被调用
                            var messageHtml = `
                                                    <div class="table-responsive">
                                                    <table class="table table-striped table-sm">
                                                    <thead>
                                                    <tr>
                                                        <th scope="col">条码信息</th>
                                                        <th scope="col">电流/A</th>
                                                        <th scope="col">电压/V</th>
                                                        <th scope="col">功率/W</th>
                                                        <th scope="col">转速/PCS</th>
                                                        <th scope="col">测试时间</th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    <tr>
                                                        <td>${response.id}</td>
                                                        <td>${response.ecurrent}</td>
                                                        <td>${response.voltage}</td>
                                                        <td>${response.epower}</td>
                                                        <td>${response.rev}</td>
                                                        <td>${response.test_time}</td>
                                                    </tr>
                                                    </tbody>
                                                    </table>
                                                    </div>
                                                `;
                            $('#message3').html(messageHtml);
                            $('#message2').replaceWith('<div class="spinner-grow text-success flex-shrink-0 me-2" role="status" id="message2"></div>');
                            if (response.validate == 1) {
                                $('#message4').html('<h1><span class="badge text-bg-success rounded-pill"><i class="bi bi-check-circle"></i> 通过</span></h1>');
                            } else {
                                $('#message4').html('<h1><span class="badge text-bg-danger rounded-pill"><i class="bi bi-x-circle"></i> 未通过</span></h1>');
                            }
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    });
});
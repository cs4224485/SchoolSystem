(function ($, doc) {
    $.init();
    $.ready(function () {
        //日期
        var result = $('#result')[0];
        var btns = $('.Birthday');

        btns.each(function (i, btn) {
            btn.addEventListener('tap', function () {
                var _self = this;
                var appointmentId = _self.parentNode.getAttribute('itemid');
                console.log(appointmentId);
                if (_self.picker) {
                    _self.picker.show(function (rs) {
                        result.innerText = rs.text;
                        _self.picker.dispose();
                        _self.picker = null;
                    });
                } else {
                    var optionsJson = this.getAttribute('data-options') || '{}';
                    var options = JSON.parse(optionsJson);
                    var id = this.getAttribute('id');
                    console.log(options);
                    _self.picker = new $.DtPicker(options);
                    _self.picker.show(function (rs) {

                        /*
                         * rs.value 拼合后的 value
                         * rs.text 拼合后的 text
                         * rs.y 年，可以通过 rs.y.vaue 和 rs.y.text 获取值和文本
                         * rs.m 月，用法同年
                         * rs.d 日，用法同年
                         * rs.h 时，用法同年
                         * rs.i 分（minutes 的第二个字母），用法同年
                         */
                        let Time = rs.y.text + "-" + rs.m.text + "-" + rs.d.text;
                        // result.innerText = Time;
                        /*
                         * 返回 false 可以阻止选择框的关闭
                         * return false;
                         */
                        /*
                         * 释放组件资源，释放后将将不能再操作组件
                         * 通常情况下，不需要示放组件，new DtPicker(options) 后，可以一直使用。
                         * 当前示例，因为内容较多，如不进行资原释放，在某些设备上会较慢。
                         * 所以每次用完便立即调用 dispose 进行释放，下次用时再创建新实例。
                         */
                        _self.picker.dispose();
                        _self.picker = null;

                        Submission(Time, appointmentId )
                    });

                }

            }, false);
        });
    });
})(mui, document);



//发送
function Submission(Time, appointmentId) {
    var _time = Time;
    mui.ajax({
        url: '',
        type: 'post',
        data: {date:_time, appointmentId:appointmentId},
        dataType: 'json',
        success: function (data) {

            if (data.state) {
                mui.alert(data.msg);
                setTimeout(function () {
                     window.location.href = ""
                },1500)
            } else {
                mui.alert(data.msg)
            }

        },
        error: function (xhr, type, errorThrown) {
            mui.alert("亲，请求出错了")

        }
    })
}













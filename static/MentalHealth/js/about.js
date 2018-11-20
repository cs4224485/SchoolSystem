var class_id = $("#class_id").attr('class_id');
(function ($, doc) {
    $.init();
    $.ready(function () {
        //学生老师
        mui.ajax({
            url: ajaxUrl + '/api/v1/mental_info/?class_id=' + class_id,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.state) {

                    var Student = []; //学生
                    var Teacher = []; //老师
                    data.data.student.forEach(function (val, index, arr) {
                        Student.push({
                            value: val.id,
                            text: val.full_name,
                        })
                    })
                    data.data.teacher.forEach(function (val, index, arr) {
                        Teacher.push({
                            value: val.id,
                            text: val.last_name + val.first_name,
                        })
                    })
                    //学生
                    var userPicker = new $.PopPicker();
                    userPicker.setData(Student);
                    var BloodTypeButton = doc.getElementById('Student');
                    BloodTypeButton.setAttribute("data-id", data.data.student[0].id); // 设置
                    BloodTypeButton.innerText = data.data.student[0].full_name;
                    BloodTypeButton.addEventListener('tap', function (event) {
                        userPicker.show(function (items) {
                            BloodTypeButton.innerText = items[0].text;
                            BloodTypeButton.setAttribute("data-id", items[0].value);
                        });
                    }, false);

                    //班主任
                    var userPickers = new $.PopPicker();
                    userPickers.setData(Teacher);
                    var BloodTypeButtons = doc.getElementById('Teacher');
                    BloodTypeButtons.innerText = data.data.teacher[0].last_name + data.data.teacher[0].first_name;
                    BloodTypeButtons.setAttribute("data-id", data.data.teacher[0].id); // 设置
                    BloodTypeButtons.addEventListener('tap', function (event) {
                        userPickers.show(function (items) {
                            BloodTypeButtons.innerText = items[0].text;
                            BloodTypeButtons.setAttribute("data-id", items[0].value);

                        });
                    }, false);

                } else {
                    mui.alert(data.msg)
                }

            },
            error: function (xhr, type, errorThrown) {
                mui.alert("亲，请求出错了")
            }
        })

        //时间
        var userPickerT = new $.PopPicker();
        userPickerT.setData([{
            value: '1',
            text: 'AM9:00-AM10:00'
        }, {
            value: '2',
            text: 'PM15:30-PM16:30'
        }]);
        var BloodTypeButtonT = doc.getElementById('time');
        BloodTypeButtonT.addEventListener('tap', function (event) {
            userPickerT.show(function (items) {
                BloodTypeButtonT.innerText = items[0].text;
                BloodTypeButtonT.setAttribute("data-id", items[0].value);

            });
        }, false);

        //日期
        var result = $('#result')[0];
        var btns = $('.Birthday');
        doc.getElementById('result').innerHTML = dataTime();
        btns.each(function (i, btn) {
            btn.addEventListener('tap', function () {
                var _self = this;
                console.log(_self)
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
                    console.log(options)
                    /*
                     * 首次显示时实例化组件
                     * 示例为了简洁，将 options 放在了按钮的 dom 上
                     * 也可以直接通过代码声明 optinos 用于实例化 DtPicker
                     */
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
                        result.innerText = rs.text;
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
                    });
                }

            }, false);
        });

        //预约
        Submission();
        //删除预约
        delAppointment()
    });
})(mui, document);

//当前日期
function dataTime() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    if (month < 10) {
        month = "0" + month;
    }
    if (day < 10) {
        day = "0" + day;
    }
    var nowDate = year + "-" + month + "-" + day;
    return nowDate
}

//预约
function Submission() {
    mui("#muiContent").on('tap', '.Submission', function () {
        let data = {
            student_id: $("#Student").attr("data-id"),
            teacher_id: $("#Teacher").attr("data-id"),
            date: $("#result").text(),
            time_id: $("#time").attr("data-id")
        };
        mui.ajax({
            url: '',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {

                if (data.state) {
                    mui.alert(data.msg);
                    setTimeout(function () {
                        window.location.href = ""
                    }, 1000)
                } else {
                    mui.alert(data.msg)
                }

            },
            error: function (xhr, type, errorThrown) {
                mui.alert("亲，请求出错了")

            }
        })
    })
}

// 删除预约
function delAppointment() {
    $('.delete').click(function () {
            var appointmentId = $(this).parents().attr('itemid');
            mui.ajax({
                url: '',
                type: 'delete',
                data: JSON.stringify({appointmentId: appointmentId}),
                dataType: 'json',
                success: function (data) {
                    if (data.state) {
                        mui.alert(data.msg);
                        setTimeout(function () {
                            window.location.href = ""
                        }, 1000)
                    } else {
                        mui.alert(data.msg)
                    }
                },
                error: function (xhr, type, errorThrown) {
                    mui.alert("亲，请求出错了")

                }
            })
        }
    )
}
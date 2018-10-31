var personalState = {}; //班级/关系情况等等
var urlId = $.getUrlParam('student_id');
var pickerSetData = [];
var schoolId = $("#school_id").attr("pk");
(function ($, doc) {
    $.init();
    $.ready(function () {
        /**
         * 获取对象属性的值
         * 主要用于过滤三级联动中，可能出现的最低级的数据不存在的情况，实际开发中需要注意这一点；
         * @param {Object} obj 对象
         * @param {String} param 属性名
         */
        var _getParam = function (obj, param) {
            return obj[param] || '';
        };


        //年级
        var picker = new mui.PopPicker({
            layer: 2
        });

        mui.ajax({
            url: ajaxUrl + '/api/v1/stuclass/?school_id='+schoolId,
            type: 'get',
            success: function (data) {
                if (data.state) {
                    let datas = data.data;
                    $.each(datas, function (i) {
                        console.log(datas[i]); //获取对应的value
                        pickerSetData.push(datas[i])
                    });
                    picker.setData(pickerSetData)
                } else {
                    mui.alert(data.msg)
                }
            },
            error: function (xhr, type, errorThrown) {
                mui.alert("亲，请求出错了")
            }
        });


        picker.pickers[0].setSelectedIndex(1);
        picker.pickers[1].setSelectedIndex(1);
        var BloodTypeButton = doc.getElementById('BloodType');
        BloodTypeButton.addEventListener('tap', function (event) {
            picker.show(function (items) {
                BloodTypeButton.value = items[0].text + items[1].text;
                personalState.classes = items[0].value ;
                personalState.classess = items[1].value
            });
        }, false);




        //亲子关系
        var visionPicker = new $.PopPicker();
        visionPicker.setData([{
            value: '1',
            text: '父亲'
        }, {
            value: '2',
            text: '母亲'
        }, {
            value: '3',
            text: '爷爷'
        }, {
            value: '4',
            text: '奶奶'
        }, {
            value: '5',
            text: '外公'
        }, {
            value: '5',
            text: '外婆'
        }, {
            value: '5',
            text: '其它亲属'
        }]);
        var visionButton = doc.getElementById('visionType');
        visionButton.addEventListener('tap', function (event) {
            visionPicker.show(function (items) {
                visionButton.value = items[0].text;
                personalState.relationship = items[0].value
            });
        }, false);


    });
})(mui, document);


//          日期选择
(function ($) {
    $.init();
    var result = $('#result')[0];
    var btns = $('.Birthday');
    btns.each(function (i, btn) {
        btn.addEventListener('tap', function () {
            var _self = this;
            console.log(_self)
            if (_self.picker) {
                _self.picker.show(function (rs) {
                    result.value = rs.text;
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
                    result.value = rs.text;
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
})(mui);


//登陆
mui("#input_information").on('tap', '.Submission', function () {

    let check = true;
    mui("#input_information input").each(function () {

        //若当前input为空，则alert提醒
        if (!this.value || this.value.trim() == "") {
            var label = this.previousElementSibling;
            mui.alert(label.innerText + "不允许为空");
            check = false;
            return false;
        }


        check = true;
    }); //校验通过，继续执行业务逻辑
    if (check) {
        //mui.alert('验证通过!')
        let input = mui('.mui-input-row input').input();
        let data = {
            name: input[0].element.value,
            birthday: input[1].element.value, //生日
            classes: parseInt(personalState.classes),
            classess: parseInt(personalState.classess),
            relationship: parseInt(personalState.relationship),

        }
        console.log(data)

        mui.ajax({
            url: '',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log(data)
                if (data.state) {
                    setTimeout(function () {
                        window.location.href = "?step=stu_info_page&student_id=" + data.student_id +"&school_id="+schoolId+"&relation="+personalState.relationship
                    }, 1500)
                } else {
                    mui.alert(data.msg)
                }

            },
            error: function (xhr, type, errorThrown) {
                mui.alert("亲，请求出错了")
                console.log(xhr);
                console.log(type);
                console.log(errorThrown);
            }
        })


    }

})
 
;
var common_ops = {
    init: function () {
    },
    confirm: function (msg, callback) {
        callback = (callback != undefined) ? callback : {'ok': null, 'cancel': null};
        layer.confirm(msg, {
            btn: ['确定', '取消'] //按钮
        }, function (index) {
            //确定事件
            if (typeof callback.ok == "function") {
                callback.ok();
            }
            layer.close(index);
        }, function (index) {
            //取消事件
            if (typeof callback.cancel == "function") {
                callback.cancel();
            }
            layer.close(index);
        });
    },
    tip: function (msg, target) {
        layer.tips(msg, target, {
            tips: [3, '#e5004f']
        });
        $('html, body').animate({
            scrollTop: target.offset().top - 10
        }, 100);
    },
    buildUrl: function (path, params) {
        var url = "" + path;
        var _paramUrl = "";
        if (params) {
            _paramUrl = Object.keys(params).map(function (k) {
                return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
            }).join("&");
            _paramUrl = "?" + _paramUrl;
        }
        return url + _paramUrl;
    },
    buildPicUrl: function (img_key) {
        var domain = $(".hidden_layout_wrap input[name=domain]").val();
        var prefix_url = $(".hidden_layout_wrap input[name=prefix_url]").val();
        return domain + prefix_url + img_key;
    },
    orderClass: function (targetset, target) {
        targetset.each(function () {
            // 根据班级名称排序
            var perClass = $(this).find(target);
            var classCount = perClass.length;
            var reg = /\d+/;

            for (let i = 0; i < classCount - 1; i++) {
                for (let j = 0; j < classCount - i - 1; j++) {
                    var nextClass = $(perClass[j + 1]).find('span').first().html();
                    if (reg.test(nextClass)) {
                        var nextClassNum = parseInt(reg.exec(nextClass)[0]);
                        var classNum = parseInt(reg.exec($(perClass[j]).find('span').first().html())[0]);
                        if (classNum > nextClassNum) {
                            $(perClass[j + 1]).after(perClass[j]);
                            perClass = $(this).find(target)
                        }
                    }
                }
            }
        })
    },
    getStudentClass: function (schoolId, grade) {
        // 根据学校和年级过滤班级
        if (parseInt(grade) === 0 || !grade) {
            grade = 7  // 7代表1年级
        }
        var classData = '';
        if (grade != 0) {
            $.ajax({
                url: "/stark/students/studentinfo/filter_class/",
                type: "get",
                async: false,
                data: {"school_id": schoolId, 'grade': grade},
                success: function (data) {
                    classData = data;
                }
            })
        }
        return classData
    },
    IsInArray: function (arr, val) {
            // 判断字段是否被选中
            var testStr = ',' + arr.join(",") + ",";
            return testStr.indexOf("," + val + ",") != -1;
        },
    bindChangePicture:function (id) {
            // 预览上传的图片
            $("#" + id).change(function () {
                var file_obj = $(this)[0].files[0];
                var reader = new FileReader();
                reader.readAsDataURL(file_obj);
                reader.onload = function () {
                    $("#" + id + "_img").attr("src", reader.result)
                };
            })
    }
};

$(document).ready(function () {
    common_ops.init();
});

// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1,                 //月份
        "d+": this.getDate(),                    //日
        "h+": this.getHours(),                   //小时
        "m+": this.getMinutes(),                 //分
        "s+": this.getSeconds(),                 //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds()             //毫秒
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};
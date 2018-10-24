var imgFiles = {};
var province = "", city = "", region = "";

//三级联动
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
        //普通示例
        //var userPicker = new $.PopPicker();
        var userPicker = new $.PopPicker({
            layer: 3
        });
        userPicker.setData(cityData3);
        var showUserPickerButton = doc.getElementById('householdRegister');
        if (showUserPickerButton) {
            var userResult = doc.getElementById('userResult');
            showUserPickerButton.addEventListener('tap', function (event) {
                userPicker.show(function (items) {
                    showUserPickerButton.value = items[0].text + items[1].text + items[2].text;
                    //返回 false 可以阻止选择框的关闭
                    //return false;

                    province = items[0].text;
                    city = items[1].text;
                    region = items[2].text;

                });

            }, false);
        }


    });
})(mui, document);


//          日期选择
(function ($) {
    $.init();
    var result = $('#birthday')[0];
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

//国旗回填
mui.ajax({
    url: ajaxUrl + '/api/v1/country/',
    type: 'get',
    dataType: 'json',
    success: function (data) {

        if (data.state) {
            let html;
            for (var i in data.data) {
                //默认为中国
                if (data.data[i].country_name == "中国") {
                    $(".guoji_img").attr("data-id", data.data[i].id)
                    $(".guoji_img").attr("src", ajaxUrl + data.data[i].img)
                    $(".guoji_name").val(data.data[i].country_name)
                    $("#isName").hide();
                }
                html = "<li data-id=" + data.data[i].id + "><p><img src=" + ajaxUrl + data.data[i].img + " ></p><p>" + data.data[i].country_name + "</p></li>";
                $("#pop_nationality").append(html)
            }
        }

    },
    error: function (xhr, type, errorThrown) {
        mui.alert("亲，请求出错了")
    }
})

//			国籍选择
mui(".nationality").on('tap', '.right_pop', function () {
    $(".pop_nationality").show()
})
mui("#pop_nationality").on('tap', 'li', function () {

    $(this).addClass("act").siblings().removeClass("act");
    $(".guoji_img").attr("src", $(this).find("img").attr("src"))
    $(".guoji_img").attr("data-id", $(this).attr("data-id"))
    $(".guoji_name").val($(this).find("p").text())
    $(".pop_nationality").hide()

    if ($(this).text() == "中国") {
        $("#isName").hide();
        $("#isuserResult,#isNation,#zw_x,#zw_m").show();
    } else {
        $("#isName").show();
        $("#isuserResult,#isNation,#zw_x,#zw_m").hide();
    }

})


//			名族选择
mui(".Nation").on('tap', '.right_pop', function () {
    $(".pop_Nation").show()
})
mui(".pop_Nation").on('tap', 'p', function () {
    $(this).addClass("act").siblings().removeClass("act");
    $(".Nation input").val($(this).text())
    $(".pop_Nation").hide()

})
mui(".pop_Nation").on('tap', '.mui-btn', function () {
    $(this).addClass("act").siblings().removeClass("act");
    $(".Nation input").val($(this).text())
    $(".pop_Nation").hide()

})

//			性别选择
mui(".positionSex").on('tap', 'img', function () {
    // $(this).addClass("act").siblings().removeClass("act");
    let index = $(this).index();
    if (index == 0) {
        $(this).attr("src", "/static/entrance/images/male.png");
        $(this).parent(".positionSex").find("img").eq(1).attr("src", "/static/entrance/images/female2.png");
    } else if (index == 1) {
        $(this).attr("src", "/static/entrance/images/female.png");
        $(this).parent(".positionSex").find("img").eq(0).attr("src", "/static/entrance/images/male2.png");
    }
    let val = $(this).attr("data-sex");
    $("#gender").val(val)

})


//			下一步
mui("#input_information").on('tap', '.Submission', function () {
    let check;
    mui("#input_information input").each(function () {
        let name = $("#input_information .guoji_name").val()
        if (name == "中国") {
            $("#isName input").val("name")
        } else {

            $("#zw_x input").val("name")
            $("#zw_m input").val("name")
        }

        //若当前input为空，则alert提醒
        if (!this.value || this.value.trim() == "") {
            var label = this.previousElementSibling;
            let msg = label.innerText || "照片："
            mui.alert(msg + "不允许为空");
            check = false;
            return false;
        }

        check = true;
    }); //校验通过，继续执行业务逻辑
    if (check) {
        let input = mui('.mui-input-row input').input();
        let oimgFiles = {
            lastModified: imgFiles.lastModified,
            lastModifiedDate: imgFiles.lastModifiedDate,
            name: imgFiles.name,
            size: imgFiles.size,
            type: imgFiles.type,
            webkitRelativePath: imgFiles.webkitRelativePath
        };

        var studentID = $('#student_pk').attr("pk");
        var schoolID = getQueryString("school_id");
        console.log(schoolID)
        data = new FormData()
        data.append('country', parseInt($(".guoji_img").attr("data-id")) || 1)
        data.append('name', $("#name").val() || "")
        data.append('last_name', $("#last_name").val() || "")
        data.append('first_name', $("#first_name").val() || "")
        data.append('gender', parseInt($("#gender").val()) || "")
        data.append('id_card', $("#id_card").val() || "")
        data.append('birthday', $("#birthday").val() || "")
        data.append('nation', $("#nation").val() || "")
        data.append('province', province || "")
        data.append('city', city || "")
        data.append('region', region || "")
        data.append('graduate_institutions', parseInt($("#graduate_institutions").attr("data-id")) || "")
        data.append('student_id', studentID || "")
        data.append('school', schoolID || '')

        let fileID = document.getElementById("position_file");
        if (fileID) {
            data.append('photo', $("#file0")[0].files[0])
        }
        $(".mui_loading").show();
        //执行ajax上传数据
        mui.ajax({
            url: '/api/v1/student/',
            type: 'post',
            data: data,
            dataType: 'json',
            contentType: false,
            processData: false,
            //xhrFields: {withCredentials: true},
            timeout: 10000,
            success: function (data) {
                if (data.state) {
                    $(".mui_loading").hide()
                    var setting_pk = $('#setting_pk').attr('pk')
                    mui.alert(data.msg)
                    setTimeout(function () {
                        window.location.href = "/student/student_info/" + setting_pk + "/?step=2&student_id=" + data.data[0].student_id
                    }, 1500)
                } else {
                    $(".mui_loading").hide()
                    mui.alert(data.msg)

                }

            },
            error: function (xhr, type, errorThrown) {
                $(".mui_loading").hide()
                mui.alert("亲，请求出错了")
                console.log(xhr);
                console.log(type);
                console.log(errorThrown);
            }
        })


    }

})


//上传图
$("#file0").change(function () {

    imgFiles = this.files[0];

    console.log(imgFiles)
    var objUrl = getObjectURL(this.files[0]);
    console.log("objUrl = " + objUrl);
    if (objUrl) {
        $("#img0").attr("src", objUrl);
        $("#img0").removeClass("hide");
    }
});


// 获取url中的参数
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); // 匹配目标参数
    var result = window.location.search.substr(1).match(reg); // 对querystring匹配目标参数
    if (result != null) {
        return decodeURIComponent(result[2]);
    } else {
        return null;
    }
}

//建立一個可存取到該file的url
function getObjectURL(file) {
    var url = null;
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    }
    else if (window.URL != undefined) {
        // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    }
    else if (window.webkitURL != undefined) {
        // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}

//        名族回填
var nationAttr = [{"name": "汉族", "en": "Han", "population": "1220844520"}, {
    "name": "蒙古族",
    "en": "Manchu",
    "population": "5981840"
}, {"name": "回族", "en": "Hui", "population": "10586087"}, {
    "name": "藏族",
    "en": "Tibetan",
    "population": "6282187"
}, {"name": "维吾尔族", "en": "Uyghur", "population": "10069346"}, {
    "name": "苗族",
    "en": "Miao",
    "population": "9426007"
}, {"name": "彝族", "en": "Yi", "population": "8714393"}, {
    "name": "壮族",
    "en": "Zhuang",
    "population": "16926381"
}, {"name": "布依族", "en": "Buyei", "population": "2870034"}, {
    "name": "朝鲜族",
    "en": "Korean",
    "population": "1830929"
}, {"name": "满族", "en": "Manchu", "population": "10387958"}, {
    "name": "侗族",
    "en": "Dong",
    "population": "2879974"
}, {"name": "瑶族", "en": "Yao", "population": "2796003"}, {
    "name": "白族",
    "en": "Bai",
    "population": "1933510"
}, {"name": "土家族", "en": "Tujia", "population": "8353912"}, {
    "name": "哈尼族",
    "en": "Hani",
    "population": "1660932"
}, {"name": "哈萨克族", "en": "Kazakh", "population": "1462588"}, {
    "name": "傣族",
    "en": "Dai",
    "population": "1261311"
}, {"name": "黎族", "en": "Li", "population": "1463064"}, {
    "name": "傈僳族",
    "en": "Lisu",
    "population": "702839"
}, {"name": "佤族", "en": "Va", "population": "429709"}, {
    "name": "畲族",
    "en": "She",
    "population": "708651"
}, {"name": "高山族", "en": "Gaoshan", "population": "452579"}, {
    "name": "拉祜族",
    "en": "Lahu",
    "population": "485966"
}, {"name": "水族", "en": "Shui", "population": "411847"}, {
    "name": "东乡族",
    "en": "Dongxiang",
    "population": "621500"
}, {"name": "纳西族", "en": "Nakhi", "population": "326295"}, {
    "name": "景颇族",
    "en": "Jingpo",
    "population": "147828"
}, {"name": "柯尔克孜族", "en": "Kyrgyz", "population": "186708"}, {
    "name": "土族",
    "en": "Monguor",
    "population": "289565"
}, {"name": "达斡尔族", "en": "Daur", "population": "131992"}, {
    "name": "仫佬族",
    "en": "Mulao",
    "population": "216257"
}, {"name": "羌族", "en": "Qiang", "population": "309576"}, {
    "name": "布朗族",
    "en": "Blang",
    "population": "119639"
}, {"name": "撒拉族", "en": "Salar", "population": "130607"}, {
    "name": "毛南族",
    "en": "Maonan",
    "population": "101192"
}, {"name": "仡佬族", "en": "Gelao", "population": "550746"}, {
    "name": "锡伯族",
    "en": "Xibe",
    "population": "190481"
}, {"name": "阿昌族", "en": "Achang", "population": "39555"}, {
    "name": "普米族",
    "en": "Pumi",
    "population": "42861"
}, {"name": "塔吉克族", "en": "Tajik", "population": "51069"}, {
    "name": "怒族",
    "en": "Nu",
    "population": "37523"
}, {"name": "乌孜别克族", "en": "Uzbek", "population": "10569"}, {
    "name": "俄罗斯族",
    "en": "Russian",
    "population": "15393"
}, {"name": "鄂温克族", "en": "Evenk", "population": "30875"}, {
    "name": "德昂族",
    "en": "Deang",
    "population": "20556"
}, {"name": "保安族", "en": "Bonan", "population": "20074"}, {
    "name": "裕固族",
    "en": "Yughur",
    "population": "14378"
}, {"name": "京族", "en": "Kinh", "population": "28199"}, {
    "name": "塔塔尔族",
    "en": "Tatar",
    "population": "3556"
}, {"name": "独龙族", "en": "Derung", "population": "6930"}, {
    "name": "鄂伦春族",
    "en": "Oroqen",
    "population": "8659"
}, {"name": "赫哲族", "en": "Nanai", "population": "5354"}, {
    "name": "门巴族",
    "en": "Monpa",
    "population": "10561"
}, {"name": "珞巴族", "en": "Lhoba", "population": "3682"}, {"name": "基诺族", "en": "Jino", "population": "23143"}];
var nationHtml = '';
for (var i in nationAttr) {
    nationHtml += '<p>' + nationAttr[i].name + '</p>';
}
$("#NationData").html(nationHtml)


//	<input onkeyup="value=value.replace(/[\W]/g,'') "onbeforepaste="clipboardData.setData('text',clipboardData.getData('text').replace(/[^\d]/g,''))">
//	控制输入框只能输入文字或数字，也可以不允许输入特殊字符 这里不允许输入如下字符: (像 !@#$%^&* 等)<br> 


function isIDCard(idCard) {
    var reg = /^[1-9]{1}[0-9]{14}$|^[1-9]{1}[0-9]{16}([0-9]|[xX])$/;
    if (!reg.test(idCard)) {
        mui.alert("身份证号码不正确");

    }
}


function ShowInputNum(obj) {
    var length = $(obj).val().length;

    //var pattern = "/^([\u4e00-\u9fa5A-Za-z0-9,.?!，。？！])*$/";
    var s = $(obj).val();
    if (!/^([\u4e00-\u9fa5A-Za-z0-9,.?!;，。？！、；])*$/.test(s)) {
        alert("存在特殊字符");
        return false;
    }
}

function school(that) {
    that.value = that.value.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\w]/g, '')
    let filter = that.value;
    //console.log(filter)
    if (filter != "") {
        mui.ajax({
            url: ajaxUrl + '/api/v1/institutions/?filter=' + filter,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                console.log(data)
                $("#school").show();
                if (data.state) {
                    let html = "";
                    for (var i in data.data) {
                        html += "<li data-id=" + data.data[i].id + ">" + data.data[i].name + "</li>";
                    }
                    $("#school").html(html)
                } else {
                    // mui.alert("暂无匹配学校")
                    $("#school").html("")

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
}

// 园校选择
mui("#school").on('tap', 'li', function () {
    $("#MschooiInput input").val($(this).text())
    $("#MschooiInput input").attr("data-id", $(this).attr("data-id"))
    $("#schooiInput").val($(this).text())
    $(".pop_school").hide();
})
mui("#MschooiInput").on('tap', 'input', function () {
    $(".pop_school").show();
})
mui(".pop_school").on('tap', 'label', function () {
    $(".pop_school").hide();
})


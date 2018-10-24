var personalState = {}; //血型视力情况等等
var urlId = $.getUrlParam('student_id');


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
        //血型
        var userPicker = new $.PopPicker();
        userPicker.setData([{
            value: '1',
            text: 'A'
        }, {
            value: '2',
            text: 'B'
        }, {
            value: '3',
            text: 'O'
        }, {
            value: '4',
            text: 'AB'
        }, {
            value: '5',
            text: '暂不清楚'
        }]);
        var BloodTypeButton = doc.getElementById('BloodType');
        if (BloodTypeButton) {
            BloodTypeButton.addEventListener('tap', function (event) {
                userPicker.show(function (items) {
                    BloodTypeButton.value = items[0].text;
                    console.log(items[0].value)
                    personalState.blood_type = items[0].value
                });
            }, false);
        }


        //视力情况
        var visionPicker = new $.PopPicker();
        visionPicker.setData([{
            value: '1',
            text: '正常'
        }, {
            value: '2',
            text: '远视'
        }, {
            value: '3',
            text: '近视'
        }, {
            value: '4',
            text: '散光'
        }, {
            value: '5',
            text: '其它'
        }]);
        var visionButton = doc.getElementById('visionType');
        if (visionButton) {
            visionButton.addEventListener('tap', function (event) {
                visionPicker.show(function (items) {
                    visionButton.value = items[0].text;
                    personalState.vision = items[0].value
                });
            }, false);
        }

        //残疾情况
        var disabilityPicker = new $.PopPicker();
        disabilityPicker.setData([{
            value: '1',
            text: '无'
        }, {
            value: '2',
            text: '视力'
        }, {
            value: '3',
            text: '听力语言'
        }, {
            value: '4',
            text: '智力'
        }, {
            value: '5',
            text: '肢体'
        }, {
            value: '6',
            text: '精神'
        }]);
        var disabilityButton = doc.getElementById('disabilityType');
        if (disabilityButton) {
            disabilityButton.addEventListener('tap', function (event) {
                disabilityPicker.show(function (items) {
                    disabilityButton.value = items[0].text;
                    personalState.disability = items[0].value
                    //返回 false 可以阻止选择框的关闭
                    //return false;
                });
            }, false);
        }


    });
})(mui, document);

//体质指数（BMI）=体重（kg）÷身高^2（m）
$("#weight").blur(function () {
    bodymassFun()
});
$("#statureHeight").blur(function () {
    bodymassFun()
});

function bodymassFun() {
    let h = Number($("#statureHeight").val()) / 100;
    let k = Number($("#weight").val());
    if (h && k) {
        //体质指数（BMI）=体重（kg）÷身高^2（m）
        let bmi = k / (h * h);
        $(".bodyMass .title span").text(bmi.toFixed(2))
        $(".bodyMass").show()

    }
}

//过敏回填
mui.ajax({
    url: ajaxUrl + '/api/v1/allergy/',
    type: 'get',
    dataType: 'json',
    success: function (data) {

        if (data.state) {
            var allergyHtml = '';
            for (var i in data.data) {
                allergyHtml += '<p data-id=' + data.data[i].id + '>' + data.data[i].title + '</p>';
            }
            $("#allergyData").html(allergyHtml)
        }

    },
    error: function (xhr, type, errorThrown) {
        mui.alert("亲，请求出错了")
        console.log(xhr, type, errorThrown)

    }
})

mui(".allergy").on('tap', '.right_pop', function () {
    $(".pop_allergy").show()
})
mui(".pop_allergy").on('tap', 'p', function () {
    $(this).addClass("act").siblings().removeClass("act");
    $(".allergy input").val($(this).text())
    $(".allergy input").attr("data-id", $(this).attr("data-id"))
    $(".pop_Nation").hide()

})

//       遗传回填
mui.ajax({
    url: ajaxUrl + '/api/v1/Inherited/',
    type: 'get',
    dataType: 'json',
    success: function (data) {

        if (data.state) {
            var inheritanceHtml = '';
            for (var i in data.data) {
                inheritanceHtml += '<p data-id=' + data.data[i].id + '>' + data.data[i].title + '</p>';
            }
            $("#inheritanceData").html(inheritanceHtml)
        }

    },
    error: function (xhr, type, errorThrown) {
        mui.alert("亲，请求出错了")
        console.log(xhr, type, errorThrown)

    }
})


mui(".inheritance").on('tap', '.right_pop', function () {
    $(".pop_inheritance").show()
})
mui(".pop_inheritance").on('tap', 'p', function () {
    $(this).addClass("act").siblings().removeClass("act");
    $(".inheritance input").val($(this).text())
    $(".inheritance input").attr("data-id", $(this).attr("data-id"))
    $(".pop_Nation").hide()
})


//			下一步
mui("#input_information").on('tap', '.Submission', function () {
    //window.location.href = "index2.html";
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
            height: parseInt($("input[name='height']").val()) || "",
            weight: parseFloat($("input[name='weight']").val()) || "",
            blood_type: personalState.blood_type || "",
            vision_status: personalState.vision || "",
            vision_left: parseFloat($("input[name='vision_left']").val()) || "",
            vision_right: parseFloat($("input[name='vision_right']").val()) || "",
            allergy: parseInt($("#allergy").attr("data-id")) || "",
            InheritedDisease: parseInt($("#InheritedDisease").attr("data-id")) || "",
            disability: parseInt(personalState.disability) || "",
            student: urlId,
        }
        console.log(data)

        mui.ajax({
            url: ajaxUrl + '/api/v1/health/',
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log(data)
                if (data.state) {
                    var setting_pk = $('#setting_pk').attr('pk')
                    mui.alert(data.msg)
                    setTimeout(function () {
                        window.location.href = "/student/student_info/" + setting_pk + "/?step=3&student_id=" + data.data[0].student_id
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

function num(obj,n) {
    obj.value = obj.value.replace(/[^\d.]/g, ""); //清除"数字"和"."以外的字符
    obj.value = obj.value.replace(/^\./g, ""); //验证第一个字符是数字
    obj.value = obj.value.replace(/\.{2,}/g, "."); //只保留第一个, 清除多余的
    obj.value = obj.value.replace(".", "$#$").replace(/\./g, "").replace("$#$", ".");
    obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/, '$1$2.$3'); //只能输入两个小数
    if(n=="name"){
        if (obj.value > 5.3 || obj.value < 3.5) {
        mui.alert("视力范围：3.5---5.3")
        obj.value = ""
         }
    }

}

$(window).click(function () {
    $(".pop_Choice").hide()
    return false
});

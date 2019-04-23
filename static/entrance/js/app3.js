var urlId = $.getUrlParam('student_id');
var relation = $.getUrlParam('relation');
var province = "", city = "", region = "", FamilyText = [];
var FamilyObj = {};
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
        //居住环境
        var userPicker = new $.PopPicker();
        userPicker.setData([{
            value: '1',
            text: '一室户'
        }, {
            value: '2',
            text: '两室户'
        }, {
            value: '3',
            text: '三室户'
        }, {
            value: '4',
            text: '三室以上'
        }]);
        var LivingConditionButton = doc.getElementById('living_condition');
        if (LivingConditionButton) {
            LivingConditionButton.addEventListener('tap', function (event) {
                userPicker.show(function (items) {
                    LivingConditionButton.value = items[0].text;
                    FamilyObj.living_condition = items[0].value;
                    //返回 false 可以阻止选择框的关闭
                    //return false;
                });
            }, false);
        }


        //居所属性
        var visionPicker = new $.PopPicker();
        visionPicker.setData([{
            value: '1',
            text: '自有'
        }, {
            value: '2',
            text: '租赁'
        }, {
            value: '3',
            text: '亲友住宅'
        }]);
        var LivingTypeButton = doc.getElementById('living_type');
        if (LivingTypeButton) {
            LivingTypeButton.addEventListener('tap', function (event) {
                visionPicker.show(function (items) {
                    LivingTypeButton.value = items[0].text;
                    FamilyObj.living_type = items[0].value;
                    //返回 false 可以阻止选择框的关闭
                    //return false;
                });
            }, false);
        }

        //交流语言
        var disabilityPicker = new $.PopPicker();
        disabilityPicker.setData([{
            value: '1',
            text: '中文普通话'
        }, {
            value: '2',
            text: '中文方言'
        },
         {
            value: '3',
            text: '英语'
        }, {
            value: '4',
            text: '其它外语'
        }]);
        var disabilityButton = doc.getElementById('language');
        if (disabilityButton) {
            disabilityButton.addEventListener('tap', function (event) {
                disabilityPicker.show(function (items) {
                    disabilityButton.value = items[0].text;
                    FamilyObj.language = items[0].value;
                    //返回 false 可以阻止选择框的关闭
                    //return false;
                });
            }, false);
        }

        //
        var userPickers = new $.PopPicker({
            layer: 3
        });
        userPickers.setData(cityData3);
        var showUserPickerButton = doc.getElementById('householdRegister');
        var userResult = doc.getElementById('userResult');
        if (userResult) {
            showUserPickerButton.addEventListener('tap', function (event) {
                userPickers.show(function (items) {
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

//家庭关系
mui(".FamilyBox").on('tap', '.flex', function () {

    if ($(this).attr("data-choose") == "true") {
        console.log("选中")
        $(this).removeClass("addFamilybj");
        $(this).attr("data-choose", false)
    } else {
        $(this).addClass("addFamilybj");
        $(this).attr("data-choose", true)
    }

    let FamilyText = $(this).attr("data-id");
    if (FamilyText == 6) {
        $(this).siblings().removeClass("addFamilybj");
        $(this).siblings().attr("data-choose", false)
    } else {
        $(".FamilyBox .isno").removeClass("addFamilybj");
        $(".FamilyBox .isno").attr("data-choose", false)
    }
});

//			下一步
mui("#input_information").on('tap', '.Submission', function () {
    //window.location.href = "index2.html";
    let check;
    mui("#input_information input").each(function () {
        var required = $(this).hasClass('required');
        if(!required){
            return
        }
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
        mui.alert('验证通过!');
        //获取家庭关系
        let FamilyText = [];
        mui("#input_information .FamilyBox .flex").each(function (e) {
            if ($(this).attr("data-choose") == "true") {
                FamilyText.push($(this).attr("data-id"))
                console.log(FamilyText)
            }
        });

        let input = mui('.mui-input-row input').input();
        let data = {
            province: province,		// 家庭省
            city: city,			// 家庭市
            region: region,		 //家庭县区
            address: $("#address").val() || "", //详细地址
            living_condition: FamilyObj.living_condition || '', //居住条件
            living_type: FamilyObj.living_type || '',  //居住类型
            language: FamilyObj.language || '',    //家庭语言
            family_status: FamilyText || '',//家庭关系
            student: urlId,
        }

        console.log(data)
        mui.ajax({
            url: ajaxUrl + '/api/v1/family/',
            traditional: true,
            type: 'post',
            data: data,
            dataType: 'json',
            success: function (data) {

                if (data.state) {
                    var setting_pk = $('#setting_pk').attr('pk');
                    setTimeout(function () {
                        window.location.href = "/student/student_info/" + setting_pk + "/?step=parents_page&student_id=" + data.data[0].student_id + "&relation=" + relation
                    }, 1500)
                } else {
                    mui.alert(data.msg)
                }

            },
            error: function (xhr, type, errorThrown) {
                mui.alert("亲，请求出错了");
                console.log(xhr);
                console.log(type);
                console.log(errorThrown);
            }
        })


    }

})


var showUserPickerButton = document.getElementById('householdRegister');
var family_district =  JSON.parse($("#family_district").text());

if(family_district){

	province = family_district.province;
	city= family_district.city;
	region= family_district.region;
	showUserPickerButton.value = province+city+region;
	console.log(province,city,region)
}

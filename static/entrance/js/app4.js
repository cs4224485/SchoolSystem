var urlId = $.getUrlParam('student_id');
var relation = $.getUrlParam('relation');
var Birthday = $('.mui-input-group .Birthday');


formFunctionTap();

function formFunctionTap() {
    //          日期选择
    (function ($) {
        $.init();
        var btns = $('.mui-input-group .Birthday');
        btns.each(function (i, btn) {
            btn.addEventListener('tap', function () {
                var _self = this;
                console.log(_self);
                if (_self.picker) {
                    _self.picker.show(function (rs) {

                        _self.value = rs.text;
                        _self.picker.dispose();
                        _self.picker = null;
                    });
                } else {
                    var optionsJson = this.getAttribute('data-options') || '{}';
                    var options = JSON.parse(optionsJson);
                    var id = this.getAttribute('id');

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

                        _self.value = rs.text;

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
//          学历选择	
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
            //居所属性
            var visionPicker = new $.PopPicker();
            visionPicker.setData([{
                value: '1',
                text: '博士'
            }, {
                value: '2',
                text: '硕士'
            }, {
                value: '3',
                text: '本科'
            }, {
                value: '4',
                text: '专科'
            }, {
                value: '5',
                text: '高中'
            }, {
                value: '6',
                text: '高中以下'
            }]);


            var visionButton = $('.visionType');
            visionButton.each(function (i, btn) {
                btn.addEventListener('tap', function (e) {
                    var _self = this;
                    visionPicker.show(function (items) {
                        _self.value = items[0].text;
                        _self.name = items[0].value

                        //返回 false 可以阻止选择框的关闭
                        //return false;
                    });
                }, false)
            })

        });
    })(mui, document);


}


//			下一步
mui("#input_information").on('tap', '.Submission', function () {
    let check = true;
    mui("#input_information input").each(function () {
        var required = $(this).hasClass('required');
        if (!required) {
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
        let input = mui('.mui-input-row input').input();
        let obj = {}

        mui("#input_information a.mui-navigate-right span").each(function (e) {
            let obj_name = $("#input_information a").eq(e).attr("data-name");
            let input_val = $("#input_information li").eq(e).find("input");
            let is_main_contact = $("#input_information").find(".MUIradio").eq(e).attr("data-id");
            var education, relation, is_contact; //最高学历

            console.log(is_main_contact)
            //return false
            switch (obj_name) {
                case "父亲":
                    education = $(".visionType").eq(e).attr("name");
                    relation = 1
                    break;
                case "母亲":
                    education = $(".visionType").eq(e).attr("name")
                    relation = 2
                    break;
                case "爷爷":
                    education = $(".visionType").eq(e).attr("name");
                    relation = 3
                    break;
                case "奶奶":
                    education = $(".visionType").eq(e).attr("name")
                    relation = 4
                    break;
                case "外公":
                    education = $(".visionType").eq(e).attr("name");
                    relation = 5
                    break;
                case "外婆":
                    education = $(".visionType").eq(e).attr("name")
                    relation = 6
                    break;
                default:

            }

            if (is_main_contact == "0") {
                is_contact = true

            } else {
                is_contact = false
            }
            console.log(obj_name)
            obj[obj_name] = {
                "last_name": $("input[name='last_name']").eq(e).val() || '', //姓
                "first_name": $("input[name='first_name']").eq(e).val() || '', //名
                "birthday": $("input[name='birthday']").eq(e).val() || '', //生日
                "telephone": $("input[name='telephone']").eq(e).val() || "", //联系电话
                "education": parseInt(education) || 7,  		//最高学历
                "company": $("input[name='company']").eq(e).val() || "", 	//工作单位
                "job": $("input[name='job']").eq(e).val() || "", 			//当前职务
                "wechat": $("input[name='wechat']").eq(e).val() || "", 		   // 微信号
                "is_main_contact": is_contact,   //是否是主要联系人
                "relation": parseInt(relation), //与学生的关系
                "student": parseInt(urlId),   //学生id
            }


        })

        console.log(obj)
//						console.log(JSON.stringify(obj))
//						var ss = JSON.stringify(obj)

        mui.ajax({
            url: ajaxUrl + '/api/v1/parents/',
            type: 'post',
            data: {'parents': JSON.stringify(obj)},
            dataType: 'json',
            success: function (data) {
                console.log(data);
                if (data.state) {
                    var setting_pk = $('#setting_pk').attr('pk');
                    setTimeout(
                        function () {
                            window.location.href = "/student/student_info/" + setting_pk + "/?step=question_page&student_id=" + urlId
                        },
                        1500)
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


//			
//选择增加监护人 personnel
var addPersonnel = document.getElementById('addPersonnel');
var Close = document.getElementById('Close');
addPersonnel.addEventListener('tap', function (event) {
    $(".pop_Choice").show()
})
Close.addEventListener('tap', function (event) {
    $(".pop_Choice").hide()
})
var add_radio_num = 1;
document.querySelector('.mui-table-view.mui-table-view-radio').addEventListener('selected', function (e) {
    let check;
    let name = e.detail.el.innerText; //当前弹窗选中的name
    let bodyName = $("#addPersonnel .mui-navigate-right");

    let nameBox = $("#input_information").find(".mui-navigate-right");
    if (nameBox.length <= 0) {
        check = true;
    } else {
        $(".find_li").each(function (e) {
            let index_name = $(".mui-table-view").find(".find_li .mui-navigate-right").eq(e).attr("data-name"); //当前页面的name
            if ($.trim(index_name) == $.trim(name)) {
                mui.alert("请误重复添加")
                check = false;
                return false;
            }
            check = true;
        });
    }
    add_radio_num++
    let radio_name = "add_radio" + add_radio_num;
    if (check) {
        $(".pop_Choice").hide()
        fieldList = JSON.parse($('#fields').attr('field'))

        var html = `<li class="mui-table-view-cell mui-collapse find_li" ">
                                <button class="btnClose">×</button>
					            <a class="mui-navigate-right" href="#" data-name=${name}><span>${name}</span></a>
                                <div class="mui-collapse-content">`;

        for (var i = 0; i < fieldList.length; i++) {
            var innerHtml = ""
            if (fieldList[i] == '家长姓名') {
                innerHtml = `<div class="mui-collapse-content">
                            <div class="mui-input-row flex_center box_sizing">
                                <label>中文姓：</label>
                                <input type="text" class="mui-input-clear" placeholder="请填写您的中文姓" name="first_name">
                            </div>
                            <div class="mui-input-row flex_center box_sizing">
                                <label>中文名：</label>
                                <input type="text" class="mui-input-clear" placeholder="请填写您的中文名" name="last_name">
                            </div>`
            } else if (fieldList[i] == '家长生日') {
                innerHtml = `<div class="mui-input-row flex_center box_sizing">
                                <label>生日：</label>
                                <input type="text" class="mui-input-clear Birthday"
                                       data-options='{"type":"date","beginYear":"1940","endYear":""}'
                                       placeholder="请选择日期" name="birthday">
                                <div class="right_pop flex_center">
                                    <span class="mui-icon mui-icon-arrowright"></span>
                                </div>
                            </div>`
            } else if (fieldList[i] == '学历') {
                innerHtml = `<div class="mui-input-row flex_center box_sizing">
                                <label>最高学历：</label>
                                <input type="text" class="mui-input-clear visionType" placeholder="请选择最高学历" name='0'
                                       readonly="readonly">
                                <div class="right_pop flex_center">
                                    <span class="mui-icon mui-icon-arrowright"></span>
                                </div>
                            </div>`
            } else if (fieldList[i] == '工作单位') {
                innerHtml = `<div class="mui-input-row flex_center box_sizing">
                                <label>工作单位：</label>
                                <input type="text" class="mui-input-clear" placeholder="请填写您的工作单位" name="company">
                            </div>`
            } else if (fieldList[i] == '职务') {
                innerHtml = `<div class="mui-input-row flex_center box_sizing">
                                <label>当前职务：</label>
                                <input type="text" class="mui-input-clear" placeholder="请填写您的当前职务" name="job">
                            </div>`
            } else if (fieldList[i] == '家长微信') {
                innerHtml = ` <div class="mui-input-row flex_center box_sizing">
                                <label>微信号：</label>
                                <input type="text" class="mui-input-clear" placeholder="选填写" name="wechat">
                            </div>`
            }


            html += innerHtml
        }
        var endHtml = `<div class="mui-input-row flex box_sizing">
                            <label class="flex_center" style=" height: 30px;">设为主要联络人：</label>
                            <div class="mui-input-clear flex_center">
                               <div class="flex_center">
                                <div class="flex_center" style=" height: 30px;">
                                       <div class="MUIradio flex_center" data-id=""><span></span></div>
                                <label>是</label>
                              </div>
                        </div>
                            </div>
                        </div>
						</div>
					</div>
	          	</div>	          					
			</li>`
        html += endHtml
        $("#input_information ul").append(html)
        formFunctionTap()
    }
});


//更换主要联系人
$("#input_information").on("click", ".MUIradio", function (e) {
    let that = $(this);
    if (!$(this).is('.addMUIradio')) {
        let btnArray = ['否', '是'];
        mui.confirm('确定更换主要联系人？', '', btnArray, function (e) {
            if (e.index == 1) {
                $("#input_information").find(".MUIradio").removeClass("addMUIradio");
                $("#input_information").find(".MUIradio").attr("data-id", "");
                that.addClass("addMUIradio")
                that.attr("data-id", "0")
            }
        })
    }

})
//删除主要联系人
$("#input_information").on("click", ".btnClose", function (e) {
    let that = $(this);
    let btnArray = ['否', '是'];
    mui.confirm('确定要删除主要联系人？', '', btnArray, function (e) {
        if (e.index == 1) {
            that.parents(".find_li").remove();
        }
    })

})

if (relation != "" && relation != null) {

    switch (relation) {
        case "1":
            addHtmls("父亲")
            break;
        case "2":
            addHtmls("母亲")
            break;
        case "3":
            addHtmls("爷爷")
            break;
        case "4":
            addHtmls("奶奶")
            break;
        case "5":
            addHtmls("外公")
            break;
        case "6":
            addHtmls("外婆")
            break;
            break;
        case "7":
            addHtmls("其他亲属")
            break;
        default:

    }
}

function addHtmls(name) {
    $("#input_information").find(".mui-navigate-right").eq(0).find("span").text(name)
    $("#input_information").find(".mui-navigate-right").eq(0).attr("data-name", name)

}
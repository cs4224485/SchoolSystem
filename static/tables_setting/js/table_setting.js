
$(function () {
    moveUpDownDelete();
    choiceField();
    operation();
    filterSchool();
    choicedSchool();
    deleteSelectedSchool()
});

function choiceField() {
    $('.sub-info').on('click', '.field', function () {
        var field = $(this).html();
        var fieldId = $(this).attr('id');
        var field_type = $(this).prop('type');
        console.log(field_type);
        if (IsInArray(selectField, field)) {
            alert('该字段已被选择中无法重复选择');
        }else if (field_type === "customization"){
            if (field === "矩阵量表"){
                var stringTag=`
                    <div class="div_question scale-table choice-wrap item">
                        <div>
                            <h3>标题</h3>
                        </div>
                        <div class="div_table_par">
                            <div class="div_table_radio_question">
                                <table style="width: 100%;" border="0px" cellpadding="5" cellspacing="0">
                                    <thead>
                                    <tr>
                                        <td class="des"></td>
                                        <td align="center" class="des">1</td>
                                        <td align="center" class="des">2</td>
                                        <td align="center" class="des">3</td>
                                        <td align="center" class="des">4</td>
                                        <td align="center" class="des">5</td>
                                    </tr>
                                    <tr>
                                        <th style="color: #efa030; font-size: 14px;" align="left">分值</th>
                                        <td align="center" style="color: #efa030; font-size: 14px">1</td>
                                        <td align="center" style="color: #efa030; font-size: 14px">2</td>
                                        <td align="center" style="color: #efa030; font-size: 14px">3</td>
                                        <td align="center" style="color: #efa030; font-size: 14px">4</td>
                                        <td align="center" style="color: #efa030; font-size: 14px">5</td>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr>
                                        <th align="left" style="border-bottom: 1px solid #efefef">外观</th>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>

                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                        <td style="border-bottom: 1px solid #efefef" align="center">
                                            <a href="###" class="jqRadio" style="position:static;"></a>
                                            <input style="display: none" type="radio">
                                        </td>
                                    </tr>
                   
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="div_title_attr_question">
                            <div class="div_title_attr_question_triangle"></div>
                            <div>
                                <input type="text" class="form-control scale-title" value="请输入标题">
                            </div>
                            <div class="tb_container">
                                <div style="padding-top: 10px;"></div>
                                <div class="spanLeft" style="position: relative;z-index:1; width: 415px ">
                                    <div class="matrixtitle" style="width: 415px">
                                        <div class="matrixhead" style="padding-left: 4px">
                                            <span style="float:left;">
                                                <b>行标题</b>
                                            </span>
                                        </div>
                                        <textarea wrap="off" rows="7" class="inputtext" tabindex="1"
                                                  style="width: 390px; height: 172px; overflow: auto; padding: 2px; margin-top: 7px; border: 1px solid rgb(205, 205, 205); resize: none;"></textarea>
                                    </div>
                                </div>
                                <div class="spanLeft" style="text-align:center; width: 570px">
                                    <table class="tableoption" cellspacing="0" cellpadding="2" width="98%">
                                        <tbody>
                                        <tr>
                                            <td style="width: 170px" align="center">
                                                        <span>
                                                            <a href="javascript:;"
                                                               style="color: rgb(34, 34, 34); margin-left: 7px; text-decoration: none">
                                                                编辑文字
                                                            </a>
                                                        </span>
                                            </td>
                                            <td align="center" style="padding: 3px 5px 3px 15px;">
                                                <span>移动</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="width: 170px;" align="center">
                                                <input type="text" value="1" class="choicetext choicetxt" tabindex="1"
                                                       style="width: 125px; border: 1px solid rgb(205, 205, 205);">
                                            </td>
                                            <td align="center" style="padding-left: 15px;">
                                            <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                  style="cursor: pointer;"></span>
                                                <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                      style="cursor: pointer;"></span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="width: 170px;" align="center">
                                                <input type="text" value="2" class="choicetext choicetxt" tabindex="1"
                                                       style="width: 125px; border: 1px solid rgb(205, 205, 205);">
                                            </td>
                                            <td align="center" style="padding-left: 15px;">
                                            <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                  style="cursor: pointer;"></span>
                                                <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                      style="cursor: pointer;"></span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="width: 170px;" align="center">
                                                <input type="text" value="3" class="choicetext choicetxt" tabindex="1"
                                                       style="width: 125px; border: 1px solid rgb(205, 205, 205);">
                                            </td>
                                            <td align="center" style="padding-left: 15px;">
                                            <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                  style="cursor: pointer;"></span>
                                                <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                      style="cursor: pointer;"></span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="width: 170px;" align="center">
                                                <input type="text" value="4" class="choicetext choicetxt" tabindex="1"
                                                       style="width: 125px; border: 1px solid rgb(205, 205, 205);">
                                            </td>
                                            <td align="center" style="padding-left: 15px;">
                                            <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                  style="cursor: pointer;"></span>
                                                <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                      style="cursor: pointer;"></span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="width: 170px;" align="center">
                                                <input type="text" value="5" class="choicetext choicetxt" tabindex="1"
                                                       style="width: 125px; border: 1px solid rgb(205, 205, 205);">
                                            </td>
                                            <td align="center" style="padding-left: 15px;">
                                            <span title="将当前选项上移一个位置" class="choiceimg design-icon design-cup"
                                                  style="cursor: pointer;"></span>
                                                <span title="将当前选项下移一个位置" class="choiceimg design-icon design-cdown"
                                                      style="cursor: pointer;"></span>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div style="margin: 14px 50px 20px">
                                <div style="color: red; font-size: 14px; display: inline-block; margin: 0px 0px 6px 10px"></div>
                                <input type="button" value="完成编辑" class="submitbutton" style="width: 100%">
                            </div>
                        </div>
                        <div class="edit-bar">
                            <a class="move-up">上移</a>
                            <a class="move-down">下移</a>
                            <a class="remove">删除</a>
                        </div>

                    </div>
                `
            }
        }else {
            var stringTag = `
                     <div class="choice-wrap item">
                          <p class="is_choice"><span name='${field}' id='${fieldId}'>${ field }</span></p>
                            <div class="edit-bar">
                                <a class="move-up">上移</a>
                                <a class="move-down">下移</a>
                                <a class="remove">删除</a>
                            </div>
                     </div>`;
           // $('.' + field_type).append(stringTag);
            selectField.push(field);
            if (field == '身份证') {
                $('#1,#4').removeClass('field').addClass('disabled')
            }
        }
        $('.' + field_type).append(stringTag);
    });
}

function IsInArray(arr, val) {
    // 判断字段是否被选中
    var testStr = ',' + arr.join(",") + ",";
    return testStr.indexOf("," + val + ",") != -1;
}

function moveUpDownDelete() {
    $('.body').on('click', '.move-down', function () {
        if ($(this).parents('.item').nextAll().length > 0) {
            $(this).parents('.item').next().after($(this).parents('.item').prop('outerHTML'));
            $(this).parents('.item').remove();
        }
    }).on('click', '.move-up', function () {
        //判断是否有上一个节点
        if ($(this).parents('.item').prevAll().length > 0) {
            $(this).parents('.item').prev().before($(this).parents('.item').prop('outerHTML'));
            $(this).parents('.item').remove();
        }

    }).on('click', '.remove', function () {
        // 点击删除
        var field = $(this).parent().prev().children();
        field = field.html();
        $(this).parents('.item').remove();
        var fieldIndex = selectField.indexOf(field);
        delete selectField[fieldIndex];
        if (field == '身份证') {
            $('#1,#4').addClass('field').removeClass('disabled')
        }
    })
}

function createDate() {
    // 构建发送的数据
    var data = {
        'title': $('#title').val(),
        'statTime': $('#start_date').val(),
        'endTime': $('#end_date').val(),
    };

    var range = [];
    var choiceId = [];
    var fieldName = [];
    var school = [];
    var scaleTable=[];

    $(".scale-table").each(function () {
         var scaleObj = {

         };

         var scaleTitle = $(this).find('h3').text();
         var scaleDes = [];
         $($(this).find('.des')).each(function () {
             if($(this).text()){
                 scaleDes.push($(this).text())
             }
         });

         var lineTitle = [];
         $($(this).find('.div_table_radio_question').find('th')).each(function (index) {
             if (index != 0){
                 lineTitle.push($(this).text())
             }
         });
         scaleObj.scaleTitle = scaleTitle;
         scaleObj.scaleDes = scaleDes;
         scaleObj.lineTitle = lineTitle;
         scaleTable.push(scaleObj);

    });

    $('.content-area span').each(function (index) {
        var id = parseInt($(this).attr('id'));
        if (id) {
            choiceId.push($(this).attr('id'));
            fieldName.push($(this).html());
        }
    });

    $('.range input').each(function () {
        if ($(this).prop("checked")) {
            var val = $(this).val();
            range.push(val)
        }
    });

    $('.choiced-school a').each(function () {
        var val = $(this).attr('value');
        school.push(val)
    });


    data.scaleTable = scaleTable;
    data.school = school;
    data.range = range;
    data.choiceFieldId = choiceId;
    data.fieldName = fieldName;
    return data
}

function operation() {
    // 保存和预览操作
    $('.actions').on('click', '#save,#preview', function () {
        var data = createDate();
        console.log(data, 'data');
        var action = $(this).html();
        if (action == '保存') {
            if (check(data)) {
                sendData(data)
            }

        } else if (action == '预览') {
            var url = '/school/preview/?data=' + JSON.stringify(data);
            window.open(url)
        }

    })
}

function check(data) {
    var flag = false;
    if (!data.title) {
        alert('请填写标题');
        return flag
    } else if (!data.statTime) {
        alert('请选择开始日期');
        return flag
    } else if (!data.endTime) {
        alert('请选择结束日期');
        return flag
    } else if (data.school.length == 0) {
        alert('请选择学校');
        return flag
    } else if (data.range.length == 0) {
        alert('请选择填表范围');
        return flag
    } else {
        flag = true;
        return flag
    }
}

function sendData(data) {
    // 发送数据到后台
    console.log(data, 'senddata');
    $.ajax({
        url: '',
        type: 'post',
        data: {'data': JSON.stringify(data)},
        success: function (data) {
            alert('保存成功');
            console.log(data);
            var nid = data.setting_obj_id;
            location.href = '/school/release/' + nid + '/'
        }
    })


}

function filterSchool() {
    // 根据省市区过滤学校
    $('#layer,#region').change(function () {
        var province = $('#province').val();
        var city = $('#city').val();
        var region = $('#region').val();
        var layer = $('#layer').val();
        console.log(layer);
        if (province && city && region) {
            console.log(province, city, region);
            $.ajax({
                url: '/school/filter/',
                type: 'get',
                dataType: 'json',
                data: {
                    'province': province,
                    'city': city,
                    'region': region,
                    'layer': layer
                },
                success: function (data) {
                    console.log('ok', data);
                    $('.school-range label').remove();
                    $.each(data['school_list'], function (index, item) {
                        var campus = item.campus_district;
                        if (!campus) {
                            campus = ''
                        }
                        var htmlTag = `<label class="checkbox-inline">
                                                    <input class="choiced", type="checkbox"  value="${item.pk}"><span>${item.school_name} ${campus}</span>
                                              </label>`;
                        $('.school-range').append(htmlTag)

                    })
                }
            })
        }

    })

}

function choicedSchool() {
    // 已选中的学校
    $('.school-range').on('click', '.choiced', function () {
        var school_name = $(this).next('span').html();
        var nid = $(this).attr("value");
        var htmlTag = ` <a style="margin: 5px" value="${nid}" class="selectedSchool"><span value="${nid}">${school_name}</span></a>`;
        if ($(this).prop('checked')) {
            $('.choiced-school').append(htmlTag)
        } else {
            //console.log($("span[value="+nid+"]"));
            $(".choiced-school a[value=" + nid + "]").remove()
        }

    })
}



function  deleteSelectedSchool() {
    // 删除已选中的学习
    $('.choiced-school').on('click', '.selectedSchool', function () {
        console.log($(this).attr('value'));
        console.log( $(this).parent().prevAll().eq(1).find('input'));
        var selectedId = $(this).attr('value');
        $(this).parent().prevAll().eq(1).find('input').each(function () {
            if(selectedId == $(this).attr('value')){
                $(this).prop('checked', '')
            }
        });
        $(this).remove();

    })

}
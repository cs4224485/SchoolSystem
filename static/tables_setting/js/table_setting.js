
$(function () {
    moveUpDownDelete();
    choiceField();
    operation();
    filterSchool();
    choicedSchool();
});

function choiceField() {
    $('.sub-info').on('click', '.field', function () {
        var field = $(this).html();
        var fieldId = $(this).attr('id');
        var field_type = $(this).prop('type');
        if (IsInArray(selectField, field)) {
            alert('该字段已被选择中无法重复选择');
        } else {
            var stringTag = `
                     <div class="choice-wrap item">
                          <p class="is_choice"><span name='${field}' id='${fieldId}'>${ field }</span></p>
                            <div class="edit-bar">
                                <a class="move-up">上移</a>
                                <a class="move-down">下移</a>
                                <a class="remove">删除</a>
                            </div>
                     </div>`;
            $('.' + field_type).append(stringTag);
            selectField.push(field);

            if (field == '身份证') {
                $('#1,#4').removeClass('field').addClass('disabled')
            }
        }
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
        console.log($(this).next('span').html());
        var school_name = $(this).next('span').html();
        var nid = $(this).attr("value");
        var htmlTag = ` <a style="margin: 5px" value="${nid}"><span value="${nid}">${school_name}</span></a>`;
        if ($(this).prop('checked')) {
            $('.choiced-school').append(htmlTag)
        } else {
            //console.log($("span[value="+nid+"]"));
            $(".choiced-school a[value=" + nid + "]").remove()
        }


    })
}
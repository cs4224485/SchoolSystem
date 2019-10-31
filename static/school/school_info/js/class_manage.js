$(function () {
    fillTh();
    fillTd();
    addClass();
    editClass();
    sendClassData()
});

function caculateMaxClasses() {
    let maxClasses = 0;
    $('.tb-body').find('tr').each(function () {
        let trCount = $(this).find('td').length;
        if (maxClasses < trCount) {
            maxClasses = trCount
        }
    });
    return maxClasses
}

function fillTh() {
    // 填充th
    let maxClasses = caculateMaxClasses();
    let addTtCount = maxClasses;
    for (let i = 0; i < addTtCount; i++) {
        let thHtml = `<th></th>`;
        $('.tb-head').find('tr').append(thHtml)
    }
}

function fillTd() {
    // 填充Td
    let maxClasses = caculateMaxClasses();
    $('.tb-body').find('tr').each(function () {
        let tdCount = $(this).find('td').length - 4;
        if (tdCount < maxClasses) {
            let addTdCount = maxClasses - tdCount;
            for (let i = 0; i < addTdCount; i++) {
                let thHtml = `<td><div class="td-box" style="display: none"></div></td>`;
                $(this).append(thHtml)
            }
        }
    })
}


function orderByClass() {
    $('.tb-body').find('tr').each(function () {
        // 根据班级名称排序
        var perClass = $(this).find('.per-class');
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
                        perClass = $(this).find('.per-class')
                    }
                }
            }
        }
    })
}

function addClass() {
    // 添加一个班级
    $('.add').on('click', '.add-btn', function () {
        var content = $(this).parents('tr').find('.per-class').last().find('span').html();
        var matchClassNumber = /\d+/.exec(content);
        console.log(matchClassNumber, 'match');
        var className = '';
        if (matchClassNumber){
            className = parseInt(matchClassNumber[0]) + 1;
        }else {
            className =  parseInt($(this).parents('tr').find('.per-class').length) + 1;
            console.log(className, '1222')
        }

        var grade = $(this).parents('tr').find('td').eq(1).attr('grade-id');
        var data = {
            grade: grade,
            className: className + '班'
        };
        var that = this;
        $.ajax({
            url: '',
            method: 'patch',
            type: 'json',
            contentType: 'json',
            data: JSON.stringify(data),
            success: function (data) {
                if (data.state) {
                    alert(data.msg);
                    let classHtml = `
                              <td class="per-class">
                                    <div class="td-box">
                                        <div class="text class-item">
                                            <p style="font-size:14px;"><span style="color:#1E1E1E;" class-id="${data.data.class_id}">${className}班</span>
                                            </p>
                                            <p style="font-size:7px;"><span
                                                    style="color:#999999;">Non，0人</span>
                                            </p>
                                        </div>
                                    </div>
                               </td>
                       `;
                    $(that).parents('tr').find('.per-class').last().after(classHtml);
                    $(that).parents('tr').siblings().each(function () {
                        $(this).append("<td></td>")
                    });
                    let thHtml = `<th></th>`;
                    $('.tb-head').find('tr').append(thHtml)
                } else {
                    alert(data.msg)
                }
            }
        });
    })
}

function editClass() {
    // 编辑班级名称以及更新班主任老师
    $('.tb-body').on('click', '.per-class', function () {
        var sourceClassName = $(this).find('.class-name').text();
        $('#class-name').val(sourceClassName);
        var classId = $(this).find('.class-name').attr('class-id');
        var selectedTutorId = $(this).find('.tutor-name').attr('tutor-id');
        selectedTutor(selectedTutorId);
        $('#class-Id').val(classId);
        $('#identifier').modal('show');
    });

}

function sendClassData() {
    $('#identifier').on('click', '#submit-data', function () {
        var classId = $('#class-Id').val();
        var className = $('#class-name').val();
        var teacherId = $('#tutor').val();
        $.ajax({
            url: '',
            method: 'post',
            contentType: 'json',
            type: 'json',
            data: JSON.stringify({className: className, teacherId: teacherId, classId: classId}),
            success: function (data) {
                if (data.state) {
                    $('#identifier').modal('hide');
                    alert(data.msg);
                    location.href = ""
                } else {
                    $('#identifier').modal('hide');
                    alert(data.msg);
                }
            }
        })
    })
}

function selectedTutor(selectedId) {
    // 获取已选中的班主任
    $('#tutor').find('option').each(function () {
        var thisId = $(this).attr('teacher-id');
        if (selectedId === thisId) {
            $(this).prop('selected', 'selected');
        } else {
            return ''
        }
    })
}
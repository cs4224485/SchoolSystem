$(function () {
    // 页面加载后从接口获取每个班级的学生
    var teacher_id = $('#teacher_id').attr('teacher_id');
    $.ajax({
        url: ajaxUrl + '/api/v1/per_class_stu/?teacher_id=' + teacher_id,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            var class_data = data.data;
            if (data.state) {
                for (let key in class_data[0]) {
                    $('#class_name').text(key).attr('index', 0);
                    createStudentHtml(class_data, 0, key)
                }
                bindLeft(class_data);
                bindRight(class_data);
            }else {
                mui.alert(data.msg)
            }
        }
    });
});

function bindLeft(class_data) {
    $('#class_left').click(function () {
        let index = $('#class_name').attr('index');
        if (index > 0) {
            index = parseInt(index) - 1;
            for (let key in class_data[index]) {
                $('#class_name').text(key).attr('index', index);
                $('#StudentList').find('li').remove();
                createStudentHtml(class_data, index, key)
            }
        }
    });
}

function bindRight(class_data) {
    $('#class_right').click(function () {
        let index = $('#class_name').attr('index');
        if (index < class_data.length) {
            index = parseInt(index) + 1;
            for (let key in class_data[index]) {
                $('#class_name').text(key).attr('index', index);
                $('#StudentList').find('li').remove();
                createStudentHtml(class_data, index, key)
            }
        }
    })
}

function createStudentHtml(class_data, index, key) {
    for (let i = 0; i < class_data[index][key].length; i++) {
        let htmlStr = `
                                       <li class="mui-table-view-cell">
                                            <span>${i + 1}</span>
                                            <span>${class_data[index][key][i].full_name}</span>
                                            <a href="/mental/record_list/${class_data[index][key][i].id}/" class="mui-icon mui-icon-arrowright right"></a>
                                       </li>
                                                      `;
        $('#StudentList').append(htmlStr)
    }
}

;
let classCount = $('.th-class').length / 5;
var schoolTimeTable = {
    init: function () {
        $('.week').each(function () {
            $(this).prop('colspan', classCount)
        });
        this.renderCourseTable(classCount);
        this.timeModule();
        this.bindAddRow(classCount);
        this.editCourse();
        this.switchTag();
        this.bindCourseSubmit();
        this.closeModel();
        this.deleteTimeRow();
        this.bindChangeCourse()
    },
    fillTd: function (classCount) {
        // 填充TD
        $('tbody').find('tr').each(function () {
            if ($(this).find('.other-event').text()) {
                return true
            }
            let courseInfoCount = $(this).find('.course-td').length;
            for (let i = courseInfoCount; i < classCount * 5; i++) {
                let border = '';
                if ((i + 1) % classCount === 0) {
                    border = 'right-border';
                }
                let rowTdHtml = `
                    <td class="${border}">
                        <div  class="text td-box course-td">
                            <p style="font-size:;"><span style="color:#999999;width: 30px;display: inline-block;">点我编辑</span></p>
                            <p style="font-size:;"><span style="color:#999999;"></span></p>
                        </div>
                    </td>
             `;
                $(this).append(rowTdHtml)
            }
        })
    },
    bindAddRow: function (classCount) {
        // 添加一行
        $('#add-row').click(function () {
            let trEle = document.createElement('tr');
            for (let i = 0; i < classCount * 5; i++) {
                let border = '';
                let timeTd = null;
                if (i === 0) {
                    timeTd = '<td class="left-border time-body"><input class="set-time form-control"  type="text" placeholder="点击设置时间">' +
                        ' <div style="margin-top: 5px"><button class="btn-danger btn btn-sm delete-time">删除</button></div> ' +
                        '</td>';
                    border = 'left-border';
                } else if ((i + 1) % classCount === 0) {
                    border = 'right-border';
                }
                let rowTdHtml = timeTd + `
                    <td class="${border}">
                        <div  class="text td-box course-td">
                            <p style="font-size:;"><span style="color:#999999;width: 30px;display: inline-block;">点我编辑</span></p>
                            <p style=""><span style="color:#999999;"></span></p>
                        </div>
                    </td>
                `;
                $(trEle).append(rowTdHtml)
            }
            $('tbody').append($(trEle));
            $(trEle).find('.set-time').focus()
        });

    },
    bindCourseSubmit: function () {
        // 提交模态对话框的数据更改
        $('#submit-data').click(function () {
            let classId = $("#class-info").attr('class-id');
            let week = $("#time-info").attr('week');
            let timeInfo = $("#time-info").attr('time-info');
            let type = parseInt($(this).attr('data-type'));
            let courseTableId = $('#course-table-id').val();
            let position = $('#position').val();
            let data = {
                'classId': classId,
                'week': week,
                'timeInfo': timeInfo,
                'type': type,
                'courseTableId': courseTableId,
            };

            if (!timeInfo) {
                alert('请先设置时间！');
                return
            }
            if (type === 0) {

                let teacherId = $('#select-teacher').val();
                let courseId = $('#op-course').val();
                let singleDoubleWeek = $('#single-double-week').find('input[type=radio]:checked').val();
                data.singleDoubleWeek = singleDoubleWeek ? singleDoubleWeek : '';
                data.teacherId = teacherId;
                data.courseId = courseId;
                data.position = position
            } else if (type === 1) {
                let event = $('#op-event').val();
                data.event = event
            }
            $.ajax({
                url: '',
                method: 'POST',
                type: 'json',
                data: data,
                success: function (res) {
                    if (res.state) {
                        $('tbody tr').each(function () {
                            let rowTime = $(this).find('.set-time').val();
                            if (timeInfo === rowTime) {
                                let courseTdDiv = $(this).find('td').eq(position).find('div');
                                $(courseTdDiv).attr('course-table-id', res.data.table_id);
                                if (res.data.info_type === 0) {
                                    // 处理课程相关
                                    if (res.data.course_week === 2 || res.data.course_week === 3) {
                                        // 处理单双周的单元格
                                        if (!courseTdDiv.hasClass('single-double-week-wrap')) {
                                            let courseHtml = `<div class="single-double-week-wrap ">
                                                                <div class="td-box single-week course-td">
                                                                    <span style="color:#1E1E1E;" class="course "></span> <span style="color:#999999;" class="teacher"></span>
                                                                </div>
                                                                <div class="td-box double-week course-td">
                                                                    <span style="color:#1E1E1E;" class="course"></span> <span style="color:#999999;" class="teacher"></span>
                                                                </div>
                                                             </div>`;
                                            $(this).find('td').eq(position).html(courseHtml);
                                        }
                                        courseTdDiv = $(this).find('td').eq(position).find('.single-double-week-wrap');
                                        $(courseTdDiv).find("div").eq(res.data.course_week - 2).attr("course-table-id", res.data.table_id);
                                        $(courseTdDiv).find("div").eq(res.data.course_week - 2).find('.course').attr('course-id', res.data.course_id).text(res.data.course_name);
                                        $(courseTdDiv).find("div").eq(res.data.course_week - 2).find('.teacher').attr('teacher-id', res.data.teacher_id).text(res.data.teacher_name);
                                    } else {
                                        if (courseTdDiv.hasClass('single-double-week-wrap')) {
                                            let courseHtml = `  <div class="text td-box course-td" course-table-id="${res.data.table_id}">
                                                                        <p style=""><span style="color:#1E1E1E;" course-id="${res.data.course_id}">${res.data.course_name}</span></p>
                                                                        <p style=""><span style="color:#999999;" teacher-id="${res.data.teacher_id}">${res.data.teacher_name}</span></p>
                                                                 </div>`;
                                            $(this).find('td').eq(position).html(courseHtml);
                                        } else {
                                            $(courseTdDiv).find('span').eq(0).text(res.data.course_name).attr('course-id', res.data.course_id).css('color', '#1E1E1E');
                                            $(courseTdDiv).find('span').eq(1).text(res.data.teacher_name).attr('course-id', res.data.teacher_id);
                                        }
                                    }
                                } else if (res.data.info_type === 1) {
                                    // 处理其他事件
                                    if (!courseTdDiv.hasClass('other-event')) {
                                        let eventHtml = ` <div class="text td-box other-event" course-table-id="${res.data.table_id}">
                                                          <p style=""><span style="color:#1E1E1E;" event-id="${res.data.event_id}">${res.data.event_name}</span></p>
                                                          </div>`;
                                        $(this).find('td').eq(1).html(eventHtml).attr("colspan", classCount * 5);
                                        $(this).find('td:gt(1)').remove();
                                    } else {
                                        $(courseTdDiv).find('span').text(res.data.event_name).attr('event-id', res.data.event_id)
                                    }
                                }
                                $('#course-edit').modal('hide');
                            }
                        })
                    } else {
                        alert(res.msg)
                    }
                }
            })
        })
    },
    editCourse: function () {
        // 获取班级以及时间信息
        let that = this;
        $('tbody').on('click', '.course-td,.other-event', function () {
            let courseTdIndex = $(this).parents('tr').find('td').index($(this).parents('td'));
            let classId = $('.class-th').find('th').eq(courseTdIndex).find('.class-name').attr('class-id');
            let week = $('.class-th').find('th').eq(courseTdIndex).attr('week');
            let timeInfo = $(this).parents('tr').find('.set-time').val();
            let position = $(this).parents('tr').children('td').index($(this).parents('td'));
            let courseTableId = $(this).attr('course-table-id') || $(this).children().attr('course-table-id');
            if (courseTableId) {
                // 如果课程表中存在将原来的数据渲染进模态对话框中
                if ($(this).hasClass('course-td')) {
                    let teacherId = $(this).find('span').eq(1).attr('teacher-id');
                    let courseId = $(this).find('span').eq(0).attr('course-id');
                    that.getCourseTeacher(courseId, classId);

                    $('#op-course').find('option').each(function () {
                        if (courseId === $(this).val()) {
                            $(this).prop('selected', 'selected');
                        }
                    });

                    setTimeout(function () {
                        $('#op-teacher').find('option').each(function () {
                            if (teacherId === $(this).val()) {
                                $(this).prop('selected', 'selected');
                            }
                        })
                    }, 100);

                    // 获取单双周信息
                    if ($(this).hasClass('single-week')) {
                        $('#single-double-week').find('input').eq(1).prop('checked', 'checked')
                    } else if ($(this).hasClass('double-week')) {
                        $('#single-double-week').find('input').eq(2).prop('checked', 'checked')
                    }
                    $('.edit-course').removeClass('modal-hide').siblings('.modal-body').addClass('modal-hide');
                    $('.course-tag').addClass('active').siblings('a').removeClass('active');
                    $('#submit-data').attr('data-type', 0)
                } else if ($(this).hasClass('other-event')) {
                    let eventId = $(this).find('p').eq(0).children().attr('event-id');
                    $('#op-event').find('option').each(function () {
                        if (eventId === $(this).val()) {
                            $(this).prop('selected', 'selected');
                        }
                    });
                    $('.edit-orther').removeClass('modal-hide').siblings('.modal-body').addClass('modal-hide');
                    $('.other-tag').addClass('active').siblings('a').removeClass('active');
                    $('#submit-data').attr('data-type', 1)
                }
            }

            $('#position').val(position);
            $('#course-table-id').val(courseTableId);
            $('#class-info').attr('class-id', classId);
            $('#time-info').attr('week', week).attr('time-info', timeInfo);
            $('#course-edit').modal('show')
        })
    },
    switchTag: function () {
        // 切换编辑课程和编辑其他
        $('.edit-tag').click(function () {
            $(this).parent().find('.active').removeClass('active');
            $(this).addClass('active');
            let tagIndex = $(this).parent().find('.edit-tag').index($(this));
            $('.modal-body').eq(tagIndex).removeClass('modal-hide').siblings('.modal-body').addClass('modal-hide');
            $('#submit-data').attr('data-type', tagIndex)
        })
    },
    renderCourseTable: function (classCount) {
        // 将后台返回的课程表数据渲染到前端
        let courseTableObj = JSON.parse($('#table-dict').text());
        for (let item in courseTableObj) {
            let trEle = document.createElement('tr');
            let timeHtml = `
                        <td class="left-border time-body">
                            <input  class="set-time form-control" type="text" value="${item}" placeholder="${item}">
                            <div style="margin-top: 5px"><button class="btn-danger btn btn-sm delete-time">删除</button></div>
                        </td>
                `;
            $(trEle).html(timeHtml);
            $('tbody').append($(trEle));
            this.fillTd(classCount);
            for (let i = 0; i < courseTableObj[item].length; i++) {
                let courseTbItem = courseTableObj[item][i];
                let tdHtml = `
                             <div class="text td-box course-td" course-table-id="${courseTbItem.course_table_id}">
                                    <p style=""><span style="color:#1E1E1E;" course-id="${courseTbItem.course_id}">${courseTbItem.course}</span></p>
                                    <p style=""><span style="color:#999999;" teacher-id="${courseTbItem.teacher_id}">${courseTbItem.teacher}</span></p>
                             </div>
                          `;
                if (courseTbItem.is_event) {
                    tdHtml = `
                                 <div class="text td-box other-event" course-table-id="${courseTbItem.course_table_id}">
                                        <p style=""><span style="color:#1E1E1E;" event-id="${courseTbItem.event_id}">${courseTbItem.other_event}</span></p>
                                 </div>
                          `;
                    $(trEle).find('td').eq(1).html(tdHtml).attr("colspan", classCount * 5);
                    $(trEle).find('td:gt(1)').remove();
                    continue
                }

                if (courseTbItem.week_info) {
                    let elePosition = $(trEle).find('td').eq(courseTbItem.position);
                    if (!elePosition.children().hasClass('single-double-week-wrap')) {
                        tdHtml = `
                                <div class="single-double-week-wrap ">
                                    <div class="td-box  single-week course-td">
                                        <span style="color:#1E1E1E;" class="course "></span> <span style="color:#999999;" class="teacher"></span>
                                    </div>
                                    <div class="td-box  double-week course-td">
                                        <span style="color:#1E1E1E;" class="course"></span> <span style="color:#999999;" class="teacher"></span>
                                    </div>
                                </div>
                           `;
                        elePosition.html(tdHtml);
                    }

                    $(elePosition).find("div").eq(courseTbItem.week_info - 1).attr("course-table-id", courseTbItem.course_table_id);
                    $(elePosition).find("div").eq(courseTbItem.week_info - 1).find('.course').attr('course-id', courseTbItem.course_id).text(courseTbItem.course);
                    $(elePosition).find("div").eq(courseTbItem.week_info - 1).find('.teacher').attr('teacher-id', courseTbItem.teacher_id).text(courseTbItem.teacher);
                    continue
                }
                $(trEle).find('td').eq(courseTbItem.position).html(tdHtml);
            }
        }
    },
    getCourseTeacher: function (courseId, classId) {
        // 根据课程获取代课老师
        $("#select-teacher").children().remove();
        $.ajax({
            url: ajaxUrl + '/api/v1/teacher_to_course/?courseId=' + courseId + '&classId=' + classId,
            method: "get",
            type: "json",
            success: function (res) {
                if (res.code === 200) {
                    // 选择老师的op盒子
                    let selectOp = $('#select-teacher');
                    for (var i = 0; i < res.data.length; i++) {
                         let optionElement = `<option class="op-teacher" class="form-control" value="${res.data[i].id}">${res.data[i].last_name + res.data[i].first_name}</option>`;
                        selectOp.append(optionElement);
                    }
                } else {
                    alert(res.msg);
                }
            }
        })

    },
    bindChangeCourse: function () {
        let that = this;
        $('#op-course').change(function () {
            let courseId = $(this).val();
            if (parseInt(courseId) !== 0) {
                let classId = $('#class-info').attr('class-id');
                that.getCourseTeacher(courseId, classId)
            }
        })
    },
    closeModel: function () {
        $('#course-edit').on('hidden.bs.modal', function () {
            // 清空之前模态对话框的数据
            $('#op-course').find('option').eq(0).prop('selected', 'selected');
            $('#select-teacher').val('').children().remove();

        })
    },
    saveTime: function (timeValue, sourceTime) {
        // 添加或修改后把时间保存到数据库
        let timeData = {'time': timeValue, 'sourceTime': ''};
        if (sourceTime) {
            timeData.sourceTime = sourceTime
        }
        $.ajax({
                url: '',
                method: 'patch',
                type: 'json',
                contentType: 'json',
                data: JSON.stringify(timeData),
                success: function (res) {
                    if (res.code === -1) {
                        alert(res.msg)
                    }
                }
            }
        )
    },
    deleteTimeRow: function () {
        $('#tMain').on('click', '.delete-time', function () {
            let that = this;
            let timeValue = $(this).parents('.time-body').find('.set-time').val();
            let flag = confirm('请确认是否删除');
            if (flag) {
                $.ajax({
                    url: "",
                    method: "delete",
                    data: JSON.stringify({time: timeValue}),
                    contentType: 'json',
                    success: function (res) {
                        if (res.code === -1) {
                            alert(res.msg)
                        } else if (res.code === 200) {
                            $(that).parents('tr').remove()
                        }
                    }
                })
            }
        })

    },
    timeModule: function () {
        var TimeSelection = function () {
            this.class = ""; //包裹的class
            this.isclass = ""; //当前的class
        };
        //初始化
        TimeSelection.prototype.init = function (config) {

            !config && (config = {});
            $.extend(this, config);
            this.CountDown();
            return this
        };

        //加载
        TimeSelection.prototype.CountDown = function () {
            var that = this;
            $("body").find("." + that.isclass).remove();
            var ph = "";
            for (var i = 10; i <= 59; i++) {
                // console.log(i)
                ph += "<p>" + i + "</p>"
            }

            var phs = "";
            for (var i = 0; i <= 9; i++) {
                // console.log(i)
                phs += "<p>0" + i + "</p>"
            }
            var pho = "";
            for (var i = 10; i <= 24; i++) {
                //  console.log(i)
                pho += "<p>" + i + "</p>"
            }
            var htmls = `
                     <div class=${that.isclass}>
                        <div class="title">选择时间</div>
                          <div class="box-l scrollbar">
                            <h1>时</h1>
                            <div>

                            ${phs} ${pho}
                            </div>
                          </div>
                          <div class="box-r scrollbar">
                            <h1>分</h1>
                            <div>

                            ${phs}
                            ${ph}
                            </div>
                          </div>
                        </div>
                    `;
            var b = $(that.class).find("." + that.isclass)[0];
            if (!b) {
                $(that.class).append(htmls)
            }
            that.ConfirmSF();

        };
        //时分确认
        TimeSelection.prototype.ConfirmSF = function () {
            var that = this;
            $("." + that.isclass).find("p").click(function () {
                let sourceTime = $(that.class).find('.set-time').val();
                $(this).addClass("act").siblings().removeClass("act");
                let s = $("." + that.isclass).find(".box-l .act").text();
                let f = $("." + that.isclass).find(".box-r .act").text();
                let text = s + ':' + f;
                if (s == "" || s == null) {
                    alert("请先选择：时");
                    return false;
                }
                if (s != "" && s != null && f != "" && f != null) {
                    $(that.class).find("input").val(text);
                    $("." + that.isclass).remove();
                    let timeValue = $(that.class).find('.set-time').val();
                    schoolTimeTable.saveTime(timeValue, sourceTime)
                }
            });


        };

        $("#tMain").on('click', '.time-body .set-time', function () {
            let that = $(this);
            // 判断当前行是否是表中得最后一行，把scroll拉到最底部
            let trElement = that.parents('tr');
            let trIndex = $('tbody').find('tr').index(trElement);
            let totalTr = $('tbody').find('tr').length;
            if (totalTr === trIndex + 1 || totalTr - 1 === trIndex + 1) {
                var scrollHeight = $('#wrap').prop("scrollHeight");
                $('#wrap').animate({scrollTop: scrollHeight}, 100);
            }
            var Times = new TimeSelection();
            Times.init({
                class: that.parents(".left-border"),
                isclass: "time_box"
            });

        })
    }

};

$(document).ready(function () {
    schoolTimeTable.init();
});
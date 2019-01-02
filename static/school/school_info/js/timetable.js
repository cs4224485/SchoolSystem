var schoolTimeTable = {
        init: function () {
            let classCount = $('.th-class').length / 5;
            $('.week').each(function () {
                $(this).prop('colspan', classCount)
            });
            this.renderCourseTable(classCount);
            this.bindAddRow(classCount);
            this.editCourse();
            this.switchTag();
            this.bindDateEvent();
            this.bindSubmit();
            this.bindChangeGrade();
            this.bindChangeTeacher();
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
                            <p style="font-size:5px;"><span style="color:#999999;width: 30px;display: inline-block;">点我编辑</span></p>
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
                        timeTd = '<td class="left-border"><input class="dateinput dateicon mr25"  type="text" placeholder="点击设置时间" readonly></td>';
                        border = 'left-border';
                    } else if ((i + 1) % classCount === 0) {
                        border = 'right-border';
                    }
                    let rowTdHtml = timeTd + `
                    <td class="${border}">
                        <div  class="text td-box course-td">
                            <p style="font-size:5px;"><span style="color:#999999;width: 30px;display: inline-block;">点我编辑</span></p>
                        </div>
                    </td>
                `;
                    $(trEle).append(rowTdHtml)
                }
                $('tbody').append($(trEle));
                $(trEle).find('.dateinput').click()
            });

        },
        addJeDate: function (elem) {
            jeDate(elem, {
                format: "hh:mm"
            });
        },
        bindDateEvent: function () {
            var that = this;
            $('tbody').on('click', '.dateinput', function () {
                that.addJeDate(this)
            })
        },
        bindSubmit: function () {
            // 添加数据到后台
            $('#submit-data').click(function () {
                let classId = $("#class-info").attr('class-id');
                let week = $("#time-info").attr('week');
                let timeInfo = $("#time-info").attr('time-info');
                let type = parseInt($(this).attr('data-type'));
                let courseTableId = $('#course-table-id').val();

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
                    let position = $('#position').val();
                    let teacherId = $('#op-teacher').val();
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
                            alert(res.msg);
                            window.location = ''
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
                let timeInfo = $(this).parents('tr').find('.dateinput').val();
                let position = $(this).parents('tr').children('td').index($(this).parents('td'));
                let courseTableId = $(this).attr('course-table-id') || $(this).children().attr('course-table-id');
                if (courseTableId) {
                    // 如果课程表中存在将原来的数据渲染进模态对话框中
                    if ($(this).hasClass('course-td')) {
                        let teacherId = $(this).find('span').eq(1).attr('teacher-id');
                        let courseId = $(this).find('span').eq(0).attr('course-id');
                        that.teacherCourseInfo(teacherId);

                        $('#op-teacher').find('option').each(function () {
                            if (teacherId === $(this).val()) {
                                $(this).prop('selected', 'selected');
                            }
                        });

                        setTimeout(function () {
                            $('#op-course').find('option').each(function () {
                            if (courseId === $(this).val()) {
                                $(this).prop('selected', 'selected');
                            }
                        })}, 100);

                        // 获取单双周信息
                        if ($(this).hasClass('single-week')){
                            $('#single-double-week').find('input').eq(0).prop('checked', 'checked')
                        }else if ($(this).hasClass('double-week')){
                            $('#single-double-week').find('input').eq(1).prop('checked', 'checked')
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
        bindChangeGrade: function () {
            // 切换年级
            $('#choice-grade').change(function () {
                let gradeId = $(this).val();
                window.location = '' + '?gradeId=' + gradeId
            })
        },
        renderCourseTable: function (classCount) {
            // 将后台返回的课程表数据渲染到前端

            let courseTableObj = JSON.parse($('#table-dict').text());
            for (let item in courseTableObj) {
                let trEle = document.createElement('tr');
                let timeHtml = `
                        <td class="left-border">
                            <input class="dateinput dateicon mr25 " id="texthms" type="text" value="${item}" placeholder="${item}" readonly>
                        </td>
                `;
                $(trEle).html(timeHtml);
                $('tbody').append($(trEle));
                this.fillTd(classCount);
                for (let i = 0; i < courseTableObj[item].length; i++) {
                    let courseTbItem = courseTableObj[item][i];
                    let tdHtml = `
                             <div class="text td-box course-td" course-table-id="${courseTbItem.course_table_id}">
                                    <p style="font-size:7px;"><span style="color:#1E1E1E;" course-id="${courseTbItem.course_id}">${courseTbItem.course}</span></p>
                                    <p style="font-size:5px;"><span style="color:#999999;" teacher-id="${courseTbItem.teacher_id}">${courseTbItem.teacher}</span></p>
                             </div>
                          `;
                    if (courseTbItem.is_event) {

                        tdHtml = `
                                 <div class="text td-box other-event" course-table-id="${courseTbItem.course_table_id}">
                                        <p style="font-size:7px;"><span style="color:#1E1E1E;" event-id="${courseTbItem.event_id}">${courseTbItem.other_event}</span></p>
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
                                        <span style="color:#1E1E1E; font-size: 4px" class="course"></span> <span style="color:#999999;" class="teacher"></span>
                                    </div>
                                </div>
                           `;
                            elePosition.html(tdHtml);
                        }

                        $(elePosition).find("div").eq(courseTbItem.week_info).attr("course-table-id", courseTbItem.course_table_id);
                        $(elePosition).find("div").eq(courseTbItem.week_info).find('.course').attr('course-id', courseTbItem.course_id).text(courseTbItem.course);
                        $(elePosition).find("div").eq(courseTbItem.week_info ).find('.teacher').attr('teacher-id', courseTbItem.teacher_id).text(courseTbItem.teacher);
                        continue
                    }
                    $(trEle).find('td').eq(courseTbItem.position).html(tdHtml);
                }
            }
        },
        teacherCourseInfo: function (teacherId) {
            // 根据选择的老师过滤该老师所代课程
            $("#op-course").children().remove();
            $.ajax({
                url:ajaxUrl + '/api/v1/teacher_to_course/?teacherId=' + teacherId,
                method: "get",
                type:"json",
                success:function (res) {
                    if(res.code === 200){
                        $("#op-course").children().remove();
                        for (let i=0; i < res.data.length; i++){
                           let optionHtml = `<option value="${res.data[i].course_id}">${res.data[i].course_des}</option>`;
                           $('#op-course').append(optionHtml)
                        }
                    }else {
                        alert(res.msg)
                    }

                }
            })

        },
        bindChangeTeacher:function () {
            let that = this;
            $('#op-teacher').change(function () {
                let teacherId = $(this).val();
                if (parseInt(teacherId) !== 0){
                    that.teacherCourseInfo(teacherId)
                }

            })
        }

    };

    $(document).ready(function () {
        schoolTimeTable.init();
        //点击显示 时分（hh:mm）格式
        jeDate(".dateinput", {
                format: "hh:mm"
        });
    });
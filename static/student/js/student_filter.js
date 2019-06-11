student_ops = {
    init: function () {
        this.renderSchool();
        let that = this;
        let schoolId = parseInt(common_ops.getUrlParam('school'));
        let gradeId = parseInt(common_ops.getUrlParam('grade'));
        layui.use('form', function () {
            let layuiForm = layui.form;
            that.renderGrade(layuiForm, schoolId);
            that.renderClass(layuiForm, schoolId, gradeId )
        });

    },
    renderSchool: function () {
        let schoolData = common_ops.getAllSchool();
        let selectedSchool = parseInt(common_ops.getUrlParam('school'));
        for (let i = 0; i < schoolData.length; i++) {
            let schoolName = schoolData[i].school_name;
            let schoolId = schoolData[i].id;
            let optionTag = `<option  value="${schoolId}">${schoolName}</option>`;
            if (schoolId === selectedSchool) {
                optionTag = `<option selected="selected" value="${schoolId}">${schoolName}</option>`;
            }
            $("#school").append(optionTag)
        }
    },
    renderGrade: function (form, schoolId) {
        let that = this;
        if (schoolId) {
            that.createGradeOption(schoolId);
            form.render('select', '')
        }

        form.on('select(school)', function (data) {
            let schoolId = data.value;
            that.createGradeOption(schoolId);
            form.render('select', '')
        })
    },
    renderClass: function (form, schoolId, gradeId) {
        let that = this;
        if (gradeId) {
            that.createClassOption(schoolId, gradeId);
            form.render('select', '')
        }
        form.on('select(grade)', function (data) {
            let gradeId = data.value;
            if (!schoolId){
                schoolId = $('#school').val();
            }
            that.createClassOption(schoolId, gradeId);
            form.render('select', '')
        })
    },
    createGradeOption: function (schoolId) {
        let grades = common_ops.getSchoolGrade(schoolId);
        let selectedGrade = parseInt(common_ops.getUrlParam('grade'));
        $('#grade').find("option[value!='']").remove();
        $('#_class').find("option[value!='']").remove();
        for (let i = 0; i < grades.length; i++) {
            let gradeName = grades[i].grade_name;
            let gradeId = grades[i].id;
            let optionTag = `<option  value="${gradeId}">${gradeName}</option>`;
            if (selectedGrade === gradeId) {
                optionTag = `<option selected="selected" value="${gradeId}">${gradeName}</option>`;
            }
            $("#grade").append(optionTag);
        }
    },
    createClassOption: function (schoolId, gradeId) {
        let _class = common_ops.getSchoolClass(schoolId, gradeId);
        let selectedClassId = parseInt(common_ops.getUrlParam('_class'));
        $('#_class').find("option[value!='']").remove();
        for (let i = 0; i < _class.length; i++) {
            let className = _class[i].name;
            let classId = _class[i].id;
            let optionTag = `<option  value="${classId}">${className}</option>`;
            if (selectedClassId === classId) {
                optionTag = `<option selected="selected" value="${classId}">${className}</option>`;
            }
            $("#_class").append(optionTag);
        }
    }
};
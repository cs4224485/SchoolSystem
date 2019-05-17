let formId = $('#form_id').val();
layui.use('form', function () {
    let form = layui.form;
    form.on('switch', function (data) {
        let inputValue = '';
        if (!data.elem.checked) {
            inputValue = 2
        } else {
            inputValue = 1
        }
        $('#switch').val(inputValue)
    });

    form.on('switch(field)', function (data) {
        let fieldId = data.value;
        if (data.elem.checked) {
            console.log(fieldId);
            $.ajax({
                url: "/stark/school/tablesettings/" + formId + "/bind_field",
                type: 'POST',
                data: {'action': 'add', 'id': fieldId},
                dataType: 'json'
            })
        } else {
            $.ajax({
                url: "/stark/school/tablesettings/" + formId + "/bind_field",
                type: 'POST',
                data: {'action': 'del', 'id': fieldId},
                dataType: 'json'
            })
        }
    })
});
let formSetting = {
    init: function () {
        this.submitData();
    },
    createData: function () {
        let title = $('#title').val();
        let on_off = $('#switch').val();
        let description = $('#description').val();
        let peroration = $('#peroration').val();
        return {'title': title, 'switch': on_off, 'description': description, 'peroration': peroration};
    },
    submitData: function () {
        $("#submit").click(function () {
            let data = formSetting.createData();
            $.ajax({
                url: '',
                type: 'post',
                data: data,
                dataType: 'json',
                success: function (data) {
                    if (data.state) {
                        location.href = ''
                    } else {
                        layer.alert(data.msg);
                    }
                },
                error: function () {
                    common_ops.alert('请求出错', function () {
                        window.location.href = ''
                    })
                }
            })
        })
    }

};


$(document).ready(function () {
    formSetting.init();
});
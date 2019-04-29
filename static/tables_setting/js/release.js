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
});
let formSetting = {
    init: function () {
        this.submitData();

    },
    createData: function () {
        let title = $('#title').val();
        let on_off = $('#switch').val();
        let description = $('#description').val();
        return {'title': title, 'switch': on_off, 'description': description};

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
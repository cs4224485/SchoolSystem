(function ($, doc) {
    $.init();
    $.ready(function () {
        //心理症状
        var userPicker = new $.PopPicker();
        userPicker.setData([{
            value: '1',
            text: '心理症状1'
        }, {
            value: '2',
            text: '心理症状2'
        }, {
            value: '3',
            text: '心理症状3'
        }, {
            value: '4',
            text: '心理症状4'
        }, {
            value: '5',
            text: '暂不清楚'
        }]);
        var BloodTypeButton = doc.getElementById('BloodType');
        if (BloodTypeButton) {
            BloodTypeButton.addEventListener('tap', function (event) {
                userPicker.show(function (items) {
                    BloodTypeButton.value = items[0].text;
                    console.log(items[0].value)

                });
            }, false);
        }


    });
})(mui, document);

//选中
mui("#AnswerBox").on('tap', '.mui-radio', function () {
    console.log("1")
    $(this).find(".Pradio").addClass("act").parent(".mui-radio").siblings().find(".Pradio").removeClass("act");
})
//			下一步
mui("#AnswerBox").on('tap', '.Submission', function () {

    let radioBox = $("#AnswerBox").find(".radioBox");
    let check;
    radioBox.each(function (e) {
        if (!$(this).find(".Pradio").is('.act')) {
            let tx = $(this).parents(".box").find(".title").text();
            mui.alert("请选择:" + tx);
            check = false;
            return false
        }
        check = true;
    });

    if (check) {
        let dataObj = {
            studentId: $('#student').attr('student_id'),
            scaleInfo: {}
        };
        let scaleTableID = $('#AnswerBox').attr('scale_pk');
        dataObj.scaleInfo[scaleTableID] = [];
        console.log($('#AnswerBox').find('radioBox'));
        $('#AnswerBox').find('.Pradio').each(function () {
            if ($(this).hasClass('act')) {
                let obj = {};
                let optionValue = $(this).attr('optionValue');
                let lintTitleId = $(this).attr('lineTitle');
                obj['title_id'] = lintTitleId;
                obj['value_id'] = optionValue;
                dataObj.scaleInfo[scaleTableID].push(obj)
            }
        });

        console.log(dataObj, 'data');

        $.ajax({
            url: '',
            type: 'post',
            data: {info: JSON.stringify(dataObj)},
            dataType: 'json',
            success: function (data) {
                if (data.state) {
                    mui.alert(data.msg);
                    var setting_pk = $('#setting_pk').attr('pk');
                    setTimeout(
                        function () {
                            window.location.href = "/student/student_info/" + setting_pk + "/?step=finish_page&student_id=" + studentId
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


});
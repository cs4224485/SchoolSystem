var studentId = $.getUrlParam('student_id');
//选中
mui("#input_information").on('tap', '.mui-radio', function () {
    $(this).find(".Pradio").addClass("act").parent(".mui-radio").siblings().find(".Pradio").removeClass("act");
});
//			下一步
mui("#input_information").on('tap', '.Submission', function () {

    let radioBox = $("#input_information").find(".radioBox");
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
            studentId: studentId,
            scaleInfo: []
        };
        $(".AnswerBox").each(function (index) {
            let scaleTableOjb = {};
            let scaleTableID = $(this).attr('scale_pk');
            scaleTableOjb[scaleTableID] = [];
            console.log($(this).find('radioBox'));
            $(this).find('.Pradio').each(function () {
                if ($(this).hasClass('act')) {
                    let obj = {};
                    let optionValue = $(this).attr('optionValue');
                    let lintTitleId = $(this).attr('lineTitle');
                    obj[lintTitleId] = optionValue;
                    scaleTableOjb[scaleTableID].push(obj)
                }
            });
            dataObj.scaleInfo.push(scaleTableOjb);

        });
        $.ajax({
            url: ajaxUrl + '/api/v1/customization/',
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
			

	
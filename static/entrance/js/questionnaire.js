var studentId = $.getUrlParam('student_id');
//选中
mui("#input_information").on('tap', '.mui-radio', function () {
    $(this).find(".Pradio").addClass("act").parent(".mui-radio").siblings().find(".Pradio").removeClass("act");
});

//选中单选
mui("#dan_input_information").on('tap','.mui-radio',function(){

	$(this).find(".Pradio").addClass("act").parent(".mui-radio").siblings().find(".Pradio").removeClass("act");
});

//选中 多选
mui("#Many_input_information").on('tap','.mui-radio',function(){
	var that = $(this);
	 if( that.find(".Pradio").hasClass("act")){
         that.find(".Pradio").removeClass("act");
    }else{
         that.find(".Pradio").addClass("act");
    }
});

//			下一步
mui(".mui-content").on('tap','.btnPrimary',function(){
	let radioBox = $(".mui-content").find(".radioBox");
	let check;
	 radioBox.each(function(e,h,){
	 	if($(this).attr("data-type")=="1"){
	 		if(!$(this).find(".Pradio").is('.act')){
		 		let tx = $(this).parents(".box").find(".title").text();
		 		mui.alert("请选择:"+tx);
		 		check = false;
		 		return false
		 	}
	 	}else if($(this).attr("data-type")=="2"){
		 	if(!$(this).find(".Pradio").is('.act')){
		 		let tx = $(this).parents(".ManyAnswerBox").find(".component-title").text();
		 		mui.alert("请选择:"+tx);
		 		check = false;
		 		return false
		 	}
	 	}else{
	 		if(!$(this).find(".Pradio").is('.act')){
		 		let tx = $(this).parents(".ManyAnswerBox").find(".component-title").text();
		 		mui.alert("请选择:"+tx);
		 		check = false;
		 		return false
		 	}
	 	}
	 	check = true;
	 });
     if (check) {
        let dataObj = {
            studentId: studentId,
            scaleInfo: [],
            choiceInfo:[]
        };
        $(".ScaleTable").each(function (index) {
            // 构建矩阵类别数据
            let scaleTableOjb = {};
            let scaleTableID = $(this).attr('scale_pk');
            scaleTableOjb[scaleTableID] = [];
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

        $(".SingleChoice,.MultiChoice").each(function () {
            // 构建选择题数据
            var choiceTableId = $(this).attr('choice-id');
            let options_id = [];
            $(this).find('.Pradio').each(function () {
                if ($(this).hasClass('act')){
                    let optionId = $(this).attr('op-id');
                    options_id.push(optionId)
            }
            });
            dataObj.choiceInfo.push({choice_id:choiceTableId, options:options_id})
        });

        console.log(dataObj);

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
			

	
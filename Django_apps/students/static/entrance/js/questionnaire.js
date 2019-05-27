	
	
//			下一步
mui("#input_information").on('tap','.Submission',function(){ 
	
	let val=$('input:radio[name="radio1"]:checked').val();
	let check;
	mui("#input_information input").each(function() {
				
		//若当前input为空，则alert提醒 
		if(val== null || val == "") {
		    var label = this.previousElementSibling;
		   // mui.alert(label.innerText + "不允许为空");
		    mui.alert("请认真写");
		    check = false;
		    return false;
		}
		
		check = true;	
	});
	if(check){
		  	mui.alert('验证通过!')
		  	
		  	
		}	

	

		
})
			

	
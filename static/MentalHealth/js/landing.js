
		//登陆
			mui("#input_information").on('tap','.Submission',function(){ 						
				let check= true;
				mui("#input_information input").each(function() {
					
						//若当前input为空，则alert提醒 
						if(!this.value || this.value.trim() == "") {
						    var label = this.previousElementSibling;
						    mui.alert(label.innerText + "不允许为空");
						    check = false;
						    return false;
						}	
						
						
						check = true;	
				}); //校验通过，继续执行业务逻辑 				
				if(check ){
					  	//mui.alert('验证通过!')
					  	let input = mui('.mui-input-row input').input(); 
					  	let data={
					  		name:        input[0].element.value,
					  		phoneNumber: input[1].element.value, //生日
					  		
					  	};
					  	 console.log(data);
					  	mui.ajax({	                          
	                          url : '/mental/login/',
	                          type : 'post',	                       
	                          data:data,
							  dataType:'json',
	                          success : function(data){	  
	                          	 console.log(data);
	                             if(data.state){
	                             	mui.alert(data.msg);
									setTimeout(function () {window.location.href = "/mental/index/"}, 1500)
	                             }else{
	                             	mui.alert(data.msg)
	                             }
	
	                          },
	                          error : function(xhr,type,errorThrown){
	                          	  mui.alert("亲，请求出错了");
	                              console.log(xhr);
	                              console.log(type);
	                              console.log(errorThrown);
	                          }
           				 })  	
	  	
					  	
					}	
					
			})



(function($, doc) {
				$.init();
				$.ready(function() {					
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
					BloodTypeButton.addEventListener('tap', function(event) {
						userPicker.show(function(items) {
							BloodTypeButton.value = items[0].text;
							console.log(items[0].value)
					
						});
					}, false);
					
					
					
				});
			})(mui, document);
			
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
					  		name:          parseInt(input[0].element.value),
					  		birthday   : input[1].element.value	, //生日	
					  		
					  	}				
					  	mui.ajax({	                          
	                          url : ajaxUrl+'/api/v1/health/',
	                          type : 'post',	                       
	                          data:data,
							  dataType:'json',
	                          success : function(data){	  
	                          	 console.log(data)
	                             if(data.state){
	                             	mui.alert(data.msg)	                           		
									setTimeout(function () {window.location.href = "index3.html?student_id="+urlId}, 1500)
	                             }else{
	                             	mui.alert(data.msg)
	                             }
	
	                          },
	                          error : function(xhr,type,errorThrown){
	                          	  mui.alert("亲，请求出错了")
	                              console.log(xhr);
	                              console.log(type);
	                              console.log(errorThrown);
	                          }
           				 })  	
	  	
					  	
					}	
					
			})


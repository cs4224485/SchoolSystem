	
				
		(function($, doc) {
				$.init();
				$.ready(function() {
					/**
					 * 获取对象属性的值
					 * 主要用于过滤三级联动中，可能出现的最低级的数据不存在的情况，实际开发中需要注意这一点；
					 * @param {Object} obj 对象
					 * @param {String} param 属性名
					 */
					var _getParam = function(obj, param) {
						return obj[param] || '';
					};
					//血型
					var userPicker = new $.PopPicker();
					userPicker.setData([{
						value: '0',
						text: 'A'
					}, {
						value: '1',
						text: 'B'
					}, {
						value: '2',
						text: 'O'
					}, {
						value: '4',
						text: 'AB'
					}, {
						value: '5',
						text: '暂不清楚'
					}]);
        			var BloodTypeButton = doc.getElementById('BloodType');
					BloodTypeButton.addEventListener('tap', function(event) {
						userPicker.show(function(items) {
							BloodTypeButton.value = items[0].text;
							//返回 false 可以阻止选择框的关闭
							//return false;
						});
					}, false);
					
					//视力情况
					var visionPicker = new $.PopPicker();
					visionPicker.setData([{
						value: '0',
						text: '正常'
					}, {
						value: '1',
						text: '近视'
					}, {
						value: '2',
						text: '远视'
					}, {
						value: '3',
						text: '散光'
					}, {
						value: '4',
						text: '其它'
					}]);
        			var visionButton = doc.getElementById('visionType');
					visionButton.addEventListener('tap', function(event) {						
						visionPicker.show(function(items) {
							visionButton.value = items[0].text;
							//返回 false 可以阻止选择框的关闭
							//return false;
						});
					}, false);
				//残疾情况
					var disabilityPicker = new $.PopPicker();
					disabilityPicker.setData([{
						value: '0',
						text: '无'
					}, {
						value: '1',
						text: '视力'
					}, {
						value: '2',
						text: '听力语言'
					}, {
						value: '3',
						text: '智力'
					}, {
						value: '4',
						text: '肢体'
					}, {
						value: '5',
						text: '精神'
					}]);
        			var disabilityButton = doc.getElementById('disabilityType');
					disabilityButton.addEventListener('tap', function(event) {						
						disabilityPicker.show(function(items) {
							disabilityButton.value = items[0].text;
							//返回 false 可以阻止选择框的关闭
							//return false;
						});
					}, false);					
					
					
				});
			})(mui, document);
			
		//体质指数（BMI）=体重（kg）÷身高^2（m）		
		$("#weight").blur(function(){
		  	bodymassFun()
		});
		$("#statureHeight").blur(function(){
		  	bodymassFun()
		});
		function bodymassFun (){
			let h =  Number($("#statureHeight").val());
		  	let k =  Number($("#weight").val());		  	
		  	 if(h&&k){
		  	 	//体质指数（BMI）=体重（kg）÷身高^2（m）
				let bmi = k/(h*h);				
				$(".bodyMass .title span").text(bmi.toFixed(2))
				$(".bodyMass").show()
				
		  	 }
		}
		
//       过敏回填
var allergyAttr= [{"name":"花粉"},{"name":"花粉1"},{"name":"花粉2"},{"name":"花粉3"},{"name":"花粉4"},{"name":"花粉5"},{"name":"花粉"},{"name":"花粉"},{"name":"花粉"},{"name":"花粉"}];
var allergyHtml='' ;
	 for(var i in allergyAttr){	
		 allergyHtml +='<p>' + allergyAttr[i].name + '</p>';                
	}
$("#allergyData").html(allergyHtml)		
			mui(".allergy").on('tap','.right_pop',function(){ 			
					 $(".pop_allergy").show()					  
			})
			mui(".pop_allergy").on('tap','p',function(){ 
					 $(this).addClass("act").siblings().removeClass("act");
					 $(".allergy input").val($(this).text())
					 $(".pop_Nation").hide()
					  
			})
//       遗传回填
var inheritanceAttr= [{"name":"大豆"},{"name":"花粉1"},{"name":"花粉2"},{"name":"花粉3"},{"name":"花粉4"},{"name":"花粉5"},{"name":"花粉"},{"name":"花粉"},{"name":"花粉"},{"name":"花粉"}];
var inheritanceHtml='' ;
	 for(var i in inheritanceAttr){	
		 inheritanceHtml +='<p>' + inheritanceAttr[i].name + '</p>';                
	}
$("#inheritanceData").html(inheritanceHtml)		
			mui(".inheritance").on('tap','.right_pop',function(){ 			
					 $(".pop_inheritance").show()					  
			})
			mui(".pop_inheritance").on('tap','p',function(){ 
					 $(this).addClass("act").siblings().removeClass("act");
					 $(".inheritance input").val($(this).text())
					 $(".pop_Nation").hide()					  
			})
		
		
		//			下一步
			mui("#input_information").on('tap','.Submission',function(){ 
				window.location.href = "index2.html";
				let check;
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
				if(check){
					  	mui.alert('验证通过!')
					  	let input = mui('.mui-input-row input').input(); 
					  	console.log(input)
					  	
					}	
					
			})
			
function num(obj){
obj.value = obj.value.replace(/[^\d.]/g,""); //清除"数字"和"."以外的字符
obj.value = obj.value.replace(/^\./g,""); //验证第一个字符是数字
obj.value = obj.value.replace(/\.{2,}/g,"."); //只保留第一个, 清除多余的
obj.value = obj.value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3'); //只能输入两个小数
}

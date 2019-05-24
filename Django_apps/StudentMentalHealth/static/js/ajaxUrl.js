var ajaxUrl = "http://47.99.121.206:8080";

/*获取到Url里面的参数*/
(function ($) {
  $.getUrlParam = function (name) {
   var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
   var r = window.location.search.substr(1).match(reg);
   if (r != null) return unescape(r[2]); return null;
  }
 })(jQuery);
let is = "1"
if(is=="1"){
	 $(".mui-bar").css("background","#2EB6BE")
}



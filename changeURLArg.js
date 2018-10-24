 function changeURLArg(url,arg,arg_val){
      var pattern=arg+'=([^&]*)';
      var replaceText=arg+'='+arg_val;
      if(url.match(pattern)){
          var tmp='/('+ arg+'=)([^&]*)/gi';
          tmp=url.replace(eval(tmp),replaceText);
          return tmp;
      }else{
          if(url.match('[\?]')){
             return url+'&'+replaceText;
         }else{
             return url+'?'+replaceText;
         }
     }
 }
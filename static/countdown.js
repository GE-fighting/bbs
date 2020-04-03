// 验证码倒计时插件

function countdown(obj){
		var that = $(obj);
		 var seconds = 60;
		 that.attr("disabled", true);
		 that.html(seconds+'秒');
	     let promise = new Promise((resolve, reject) => {
	      let setTimer = setInterval(
	        () => {
	          seconds -= 1;
	          // console.info('倒计时:' + seconds);
	          that.html(seconds+'秒');
	          if (seconds <= 0) {
	          	that.html('获取短信验证码');
	            resolve(setTimer)
	          }
	        }
	        , 1000)
	    })
	    promise.then((setTimer) => {
	       // console.info('清除');
	      clearInterval(setTimer);
	      that.attr("disabled", false);
	    })   
	}
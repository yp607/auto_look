var logMap = {}
var fs = require('fs');
var logger = fs.createWriteStream('./saveButton.log', {
    flags: 'a', // 'a' means appending (old data will be preserved)
	encoding: 'utf-8'
})


module.exports = {
    summary: 'a rule to modify request',
	*beforeSendRequest(requestDetail) {
    if (/lessonStudyData.updateRcoTreeList.dwr/i.test(requestDetail.url)) {
		logger.write(requestDetail.url + '|');
		var header_obj = requestDetail.requestOptions.headers

		//先判断是否有postdata，过滤无用请求
		var payload_obj = requestDetail.requestData
		var arr=payload_obj.toString().split("\n");
		if(arr.length > 0 )
		{
			for(var i in header_obj) {
				logger.write('"'+i+'":"'+header_obj[i]+'",');
			}
			logger.write('|');
			
			for (var j in arr)
			{
				if(j == arr.length - 1){
					break;
				}
				var brr = arr[j].split("=");
				logger.write('"'+brr[0]+'":"'+brr[1]+'",');
			}
			logger.write('\r\n');
		}
    }
	else if (/lessonStudyData.removeSession.dwr/i.test(requestDetail.url))
    {
		 const localResponse = {
			  statusCode: 200,
			  header: { 'Content-Type': 'application/json' },
			  body: '{"hello": "You are SB"}'
			};
			
		  return {
			response: localResponse
		  };
		
	}
  },
};
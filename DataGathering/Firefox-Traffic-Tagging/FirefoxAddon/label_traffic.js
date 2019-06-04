/*
 * Connect to the UDP traffic labeling application.
 */
var port = browser.runtime.connectNative("webudptagger");

/*
 * Tag traffic on the beginning of a web page load.
 */
browser.webNavigation.onBeforeNavigate.addListener(function(details){
	console.log("Page " + details.url + " is about TO BE LOADED...");
	console.log(details);
	//port.postMessage("TrafficBegin: " + details.url);
	var begin_obj = {};
	begin_obj['state'] = "begin";
	begin_obj['windowId'] = details.windowId;
	begin_obj['tabId'] = details.tabId;
	begin_obj['url'] = details.url;
	if (details.frameId == 0) {
		port.postMessage(JSON.stringify(begin_obj));
	}
});

/*
 * Tag traffic at the end of a web page load.
 */
browser.webNavigation.onCompleted.addListener(function(details){
	console.log("Page " + details.url + " has been FULLY LOADED!");
	console.log(details);
	//port.postMessage("TrafficEnd: " + details.url);
	var end_obj = {};
	end_obj['state'] = "end";
	end_obj['windowId'] = details.windowId;
	end_obj['tabId'] = details.tabId;
	end_obj['url'] = details.url;
	if (details.frameId == 0) {
		port.postMessage(JSON.stringify(end_obj));
	}
});


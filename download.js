// ==UserScript==
// @name         发送给下载器
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @require      https://code.jquery.com/jquery-2.1.4.min.js
// @author       You
// @match        https://xxxxxxxxxxxxxxxxxxxxxxx/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        GM_xmlhttpRequest
// @run-at       document-end
// ==/UserScript==

(function() {
    // Your code here...
    $(".copy-to-clipboard").click(function(){
        var url_string=$(this).attr("data-clipboard-text");
        console.log(url_string);
        var json = JSON.stringify({url:url_string});
        console.log(json);
        var on_error = function(){
               alert("发生了一些错误，添加下载任务失败")
        }
        var on_load = function(response){
            console.log(response.status);
            if(response.status==200){
               alert("成功添加任务")
            }
        }
        var request = {method:"POST",onerror:on_error,onload:on_load,headers:{"Content-Type":"application/json"},url:"http://synology-downloader.lemonhall.me:8000/create_task",data:json};
        GM_xmlhttpRequest(request);
     });
})();

//tampermonkey的脚本，给某站点定制的，这样一旦点击了复制到剪贴板之后，自动开始下载
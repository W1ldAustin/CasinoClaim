"use strict";!function(e){e.vAPI&&!0===e.vAPI.uBO||(e.vAPI={uBO:!0});var t=e.vAPI,n=e.chrome;t.setTimeout=t.setTimeout||e.setTimeout.bind(e);var o;t.download=function(e){if(e.url){var t=document.createElement("a");t.href=e.url,t.setAttribute("download",e.filename||""),t.setAttribute("type","text/plain"),t.dispatchEvent(new MouseEvent("click"))}},t.getURL=n.runtime.getURL,t.i18n=n.i18n.getMessage,o=t.i18n("@@ui_locale"),document.body.setAttribute("dir",-1!==["ar","he","fa","ps","ur"].indexOf(o)?"rtl":"ltr"),t.closePopup=function(){e.browser instanceof Object&&"function"==typeof e.browser.runtime.getBrowserInfo?window.close():window.open("","_self").close()};try{t.localStorage=window.localStorage}catch(e){}t.localStorage instanceof Object==!1&&(t.localStorage={length:0,clear:function(){},getItem:function(){return null},key:function(){throw new RangeError},removeItem:function(){},setItem:function(){}})}(this);
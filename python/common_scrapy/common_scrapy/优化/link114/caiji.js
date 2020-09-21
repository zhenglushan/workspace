var _0xef47 = ["undefined", "&r=", "random", "img", "createElement", "src", "/template/images/loading.gif", "setAttribute", "appendChild", "abort", "超时:", "createTextNode", "a", "href", "#", "重查", "onclick", "onreadystatechange", "readyState", "status", "search", "responseText", "(", ")", "-1", "1", "result", "-2", "过载,暂停2分钟", "-3", "已停用", "-4", "不支持域名后辍", "-7", "match", "", "wxaq", "付费,200元/月:", "icp", "gfw", "开通VIP赠送:", "开通", "/member.php", "title", "自助充值，开通后无限查询。", "target", "_blank", "GET", "open", "Content-Type", "text/html", "setRequestHeader", "charset", "utf-8", "send", "Msxml2.XMLHTTP", "Microsoft.XMLHTTP", "&id=1&sign=signstring&signtype=1", "jsonp", "callback", "VIP功能:", "升级", "3秒注册，自助充值升级", "ajax"];

function getContent(url, callback, domEl, async) {
    if (typeof (async) == _0xef47[0]) {
        async = true
    }
    ;
    url += _0xef47[1] + parsInt(Math[_0xef47[2]]() * 1000);
    clearChild(domEl);
    var loadingimg = document[_0xef47[4]](_0xef47[3]);
    loadingimg[_0xef47[7]](_0xef47[5], _0xef47[6]);
    domEl[_0xef47[8]](loadingimg);
    var xmlhttp = GetXmlHttpObject();
    var mytimeout = 60000;
    var timer;
    if (mytimeout) {
        timer = setTimeout(function () {
            xmlhttp[_0xef47[9]]();
            clearChild(domEl);
            var timeoutRetryText = document[_0xef47[11]](_0xef47[10]);
            domEl[_0xef47[8]](timeoutRetryText);
            var timeoutRetry = document[_0xef47[4]](_0xef47[12]);
            timeoutRetry[_0xef47[7]](_0xef47[13], _0xef47[14]);
            var timeoutRetryText2 = document[_0xef47[11]](_0xef47[15]);
            timeoutRetry[_0xef47[16]] = function () {
                clearChild(domEl);
                getContent(url, callback, domEl);
                return false
            };
            timeoutRetry[_0xef47[8]](timeoutRetryText2);
            domEl[_0xef47[8]](timeoutRetry);
            getNext()
        }, mytimeout)
    }
    ;
    xmlhttp[_0xef47[17]] = function () {
        if (xmlhttp[_0xef47[18]] == 4) {
            if (timer) {
                clearTimeout(timer)
            }
            ;
            getNext();
            if (xmlhttp[_0xef47[19]] == 200) {
                var result = new Object;
                if (xmlhttp[_0xef47[21]][_0xef47[20]](/^\{[\s\S]+\}$/) >= 0) {
                    result = eval(_0xef47[22] + xmlhttp[_0xef47[21]] + _0xef47[23])
                } else {
                    result[_0xef47[19]] = _0xef47[24]
                }
                ;
                if (result[_0xef47[19]] == _0xef47[25]) {
                    callback(url, result[_0xef47[26]], domEl)
                } else {
                    if (result[_0xef47[19]] == _0xef47[24]) {
                        otherReasonRetry(url, callback, domEl)
                    } else {
                        if (result[_0xef47[19]] == _0xef47[27]) {
                            clearChild(domEl);
                            var caijiRetryText = document[_0xef47[11]](_0xef47[28]);
                            domEl[_0xef47[8]](caijiRetryText)
                        } else {
                            if (result[_0xef47[19]] == _0xef47[29]) {
                                clearChild(domEl);
                                var caijiRetryText = document[_0xef47[11]](_0xef47[30]);
                                domEl[_0xef47[8]](caijiRetryText)
                            } else {
                                if (result[_0xef47[19]] == _0xef47[31]) {
                                    clearChild(domEl);
                                    var caijiRetryText = document[_0xef47[11]](_0xef47[32]);
                                    domEl[_0xef47[8]](caijiRetryText)
                                } else {
                                    if (result[_0xef47[19]] == _0xef47[33]) {
                                        var func = callback.toString()[_0xef47[34]](/^function\s*([^\s(]+)/)[1];
                                        var tips = _0xef47[35];
                                        if (func == _0xef47[36]) {
                                            tips = _0xef47[37]
                                        } else {
                                            if (func == _0xef47[38] || func == _0xef47[39]) {
                                                tips = _0xef47[40]
                                            }
                                        }
                                        ;
                                        clearChild(domEl);
                                        var caijiRetryText = document[_0xef47[11]](tips);
                                        var spanText = document[_0xef47[11]](_0xef47[41]);
                                        var spanA = document[_0xef47[4]](_0xef47[12]);
                                        spanA[_0xef47[7]](_0xef47[13], _0xef47[42]);
                                        spanA[_0xef47[7]](_0xef47[43], _0xef47[44]);
                                        spanA[_0xef47[7]](_0xef47[45], _0xef47[46]);
                                        spanA[_0xef47[8]](spanText);
                                        domEl[_0xef47[8]](caijiRetryText);
                                        domEl[_0xef47[8]](spanA)
                                    } else {
                                        otherReasonRetry(url, callback, domEl)
                                    }
                                }
                            }
                        }
                    }
                }
            } else {
                otherReasonRetry(url, callback, domEl)
            }
        }
    };
    xmlhttp[_0xef47[48]](_0xef47[47], url, async);
    xmlhttp[_0xef47[51]](_0xef47[49], _0xef47[50]);
    xmlhttp[_0xef47[51]](_0xef47[52], _0xef47[53]);
    xmlhttp[_0xef47[54]](null)
}

function GetXmlHttpObject() {
    var xmlHttp = null;
    try {
        xmlHttp = new XMLHttpRequest()
    } catch (e) {
        try {
            xmlHttp = new ActiveXObject(_0xef47[55])
        } catch (e) {
            xmlHttp = new ActiveXObject(_0xef47[56])
        }
    }
    ;
    return xmlHttp
}

function getContentCrossdomain(url, callback, domEl, async) {
    if (typeof (async) == _0xef47[0]) {
        async = true
    }
    ;
    clearChild(domEl);
    var loadingimg = document[_0xef47[4]](_0xef47[3]);
    loadingimg[_0xef47[7]](_0xef47[5], _0xef47[6]);
    domEl[_0xef47[8]](loadingimg);
    url += _0xef47[57];
    $[_0xef47[63]]({
        url: url,
        timeout: 60000,
        type: _0xef47[47],
        async: async,
        dataType: _0xef47[58],
        jsonp: _0xef47[59],
        success: function (result) {
            if (result[_0xef47[19]] == _0xef47[25]) {
                callback(url, result[_0xef47[26]], domEl)
            } else {
                if (result[_0xef47[19]] == _0xef47[24]) {
                    otherReasonRetryCrossdomain(url, callback, domEl)
                } else {
                    if (result[_0xef47[19]] == _0xef47[27]) {
                        clearChild(domEl);
                        var caijiRetryText = document[_0xef47[11]](_0xef47[28]);
                        domEl[_0xef47[8]](caijiRetryText)
                    } else {
                        if (result[_0xef47[19]] == _0xef47[29]) {
                            clearChild(domEl);
                            var caijiRetryText = document[_0xef47[11]](_0xef47[30]);
                            domEl[_0xef47[8]](caijiRetryText)
                        } else {
                            if (result[_0xef47[19]] == _0xef47[31]) {
                                clearChild(domEl);
                                var caijiRetryText = document[_0xef47[11]](_0xef47[32]);
                                domEl[_0xef47[8]](caijiRetryText)
                            } else {
                                if (result[_0xef47[19]] == _0xef47[33]) {
                                    clearChild(domEl);
                                    var caijiRetryText = document[_0xef47[11]](_0xef47[60]);
                                    var spanText = document[_0xef47[11]](_0xef47[61]);
                                    var spanA = document[_0xef47[4]](_0xef47[12]);
                                    spanA[_0xef47[7]](_0xef47[13], _0xef47[42]);
                                    spanA[_0xef47[7]](_0xef47[43], _0xef47[62]);
                                    spanA[_0xef47[7]](_0xef47[45], _0xef47[46]);
                                    spanA[_0xef47[8]](spanText);
                                    domEl[_0xef47[8]](caijiRetryText);
                                    domEl[_0xef47[8]](spanA)
                                } else {
                                    otherReasonRetryCrossdomain(url, callback, domEl)
                                }
                            }
                        }
                    }
                }
            }
        },
        complete: function (XMLHttpRequest, status) {
            getNext()
        }
    })
}
var _0xff16 = ["", "replace", "val", "#ip_websites", "shift", "#mysite", "length", "baidu_sl", "baidu_qz_ai", "baidu_qz_ai_pc", "baidu_qz_ai_wap", "baidu_qz_zz", "baidu_qz_zz_pc", "baidu_qz_zz_wap", "baidu_uv_zz", "baidu_uv_zz_pc", "baidu_uv_zz_wap", "baidu_kw_zz", "baidu_kw_zz_pc", "baidu_kw_zz_wap", "baidu_checksl_pc", "baidu_checksl_wap", "baidu_backlink", "baidu_backlink1", "baidu_backlink7", "baidu_sl1", "baidu_sl7", "baidu_aq", "baidu_kz", "baidu_news_sl", "baidu_news_checksl", "baidu_vstar", "baidu_koubei", "so360_sl", "so360_checksl", "so360_qz_ai", "so360_qz_ai_pc", "so360_qz_ai_wap", "so360_qz_zz", "so360_qz_zz_pc", "so360_qz_zz_wap", "so360_uv_zz", "so360_uv_zz_pc", "so360_uv_zz_wap", "so360_kw_zz", "so360_kw_zz_pc", "so360_kw_zz_wap", "so360_aq", "so360_kz", "so360_news_sl", "so360_news_checksl", "sogou_qz_ai", "sogou_sl", "sogou_checksl", "sogou_pr", "sogou_kz", "sogou_news_sl", "sogou_news_checksl", "sogou_backlink", "sm_qz_ai", "sm_qz_zz", "sm_uv_zz", "sm_kw_zz", "sm_sl", "sm_checksl", "toutiao_qz_zz", "toutiao_uv_zz", "toutiao_kw_zz", "icp_unitname", "icp_unitnature", "icp_license", "icp_sitename", "icp_siteurl", "icp_verifydate", "archive_first", "archive_last", "archive_frequency", "archive_savenums", "archive_title", "archive_gray", "backlink_zz", "alexa", "moz_da", "moz_pa", "daochu", "title", "createdtime", "qqaq", "wxaq", "icp", "gfw", "ip", "checklink", "pr", "checked", "attr", ".func_select #chk_", ":visible", "is", "parent", "push", "checklink_type", "getElementsByName", "value", "mysite=", "checklink_type=", "mysite_status", "getElementById", "get.php?func=outlink&site=", "undefined", "func=", "|", "join", "getDate", "setDate", "cookie", "preference=", ";expires=", "toGMTString", "#thousands", "slice", "websites=", "&", "click", "#tj, #btn_checklink", "removeClass", ".radio", "siblings", "input[type=radio]", "find", "radio", "hasClass", "addClass", "prev", ".radio, .radio + span", "selected", "toggleClass", ".checkbox", "#func_area", "input[type=checkbox]", "red", ".func_select", ".func_selectall", "btn_more_highlight", "btn_more=1;expires=", "show", "#func_more", "收起︽", "html", ".btn_more", "btn_more=0;expires=", "hide", "更多︾"];
var mysiteOutlinks;
$(function () {
    $(_0xff16[124])[_0xff16[123]](function () {
        var ip_websites = $(_0xff16[3])[_0xff16[2]]()[_0xff16[1]](/(?:^\s*)|(?:\s*$)/g, _0xff16[0]);
        ip_websites = filter(ip_websites);
        var mysite = filter($(_0xff16[5])[_0xff16[2]]())[_0xff16[4]]();
        if (ip_websites[_0xff16[6]] > 0 || mysite) {
            var query = new Array;
            var query_func = new Array;
            var userSet = new Array;
            var cha_func_array = [_0xff16[7], _0xff16[8], _0xff16[9], _0xff16[10], _0xff16[11], _0xff16[12], _0xff16[13], _0xff16[14], _0xff16[15], _0xff16[16], _0xff16[17], _0xff16[18], _0xff16[19], _0xff16[20], _0xff16[21], _0xff16[22], _0xff16[23], _0xff16[24], _0xff16[25], _0xff16[26], _0xff16[27], _0xff16[28], _0xff16[29], _0xff16[30], _0xff16[31], _0xff16[32], _0xff16[33], _0xff16[34], _0xff16[35], _0xff16[36], _0xff16[37], _0xff16[38], _0xff16[39], _0xff16[40], _0xff16[41], _0xff16[42], _0xff16[43], _0xff16[44], _0xff16[45], _0xff16[46], _0xff16[47], _0xff16[48], _0xff16[49], _0xff16[50], _0xff16[51], _0xff16[52], _0xff16[53], _0xff16[54], _0xff16[55], _0xff16[56], _0xff16[57], _0xff16[58], _0xff16[59], _0xff16[60], _0xff16[61], _0xff16[62], _0xff16[63], _0xff16[64], _0xff16[65], _0xff16[66], _0xff16[67], _0xff16[68], _0xff16[69], _0xff16[70], _0xff16[71], _0xff16[72], _0xff16[73], _0xff16[74], _0xff16[75], _0xff16[76], _0xff16[77], _0xff16[78], _0xff16[79], _0xff16[80], _0xff16[81], _0xff16[82], _0xff16[83], _0xff16[84], _0xff16[85], _0xff16[86], _0xff16[87], _0xff16[88], _0xff16[89], _0xff16[90], _0xff16[91], _0xff16[92], _0xff16[93]];
            for (i = 0; i < cha_func_array[_0xff16[6]]; i++) {
                var func_name = cha_func_array[i];
                if ($(_0xff16[96] + func_name)[_0xff16[95]](_0xff16[94]) == _0xff16[94]) {
                    if ($(_0xff16[96] + func_name)[_0xff16[99]]()[_0xff16[98]](_0xff16[97])) {
                        query_func[_0xff16[100]](func_name)
                    }
                    ;
                    userSet[_0xff16[100]](func_name)
                }
            }
            ;
            if (mysite) {
                query_func[_0xff16[100]](_0xff16[92]);
                var checklink_type = _0xff16[0];
                var chk_checklink_type = document[_0xff16[102]](_0xff16[101]);
                for (var i = 0; i < chk_checklink_type[_0xff16[6]]; i++) {
                    if (chk_checklink_type[i][_0xff16[94]]) {
                        checklink_type = chk_checklink_type[i][_0xff16[103]];
                        break
                    }
                }
                ;
                query[_0xff16[100]](_0xff16[104] + mysite);
                query[_0xff16[100]](_0xff16[105] + checklink_type);
                if (!ip_websites || ip_websites[_0xff16[6]] == 0) {
                    var mysite_status = document[_0xff16[107]](_0xff16[106]);
                    mysite = decodeURIComponent(mysite);
                    mysite = str_reverse(mysite);
                    mysite = encodeURIComponent(mysite);
                    getContent(_0xff16[108] + mysite, outlink, mysite_status, false);
                    if (mysiteOutlinks != _0xff16[109]) {
                        ip_websites = filter(mysiteOutlinks);
                        mysiteOutlinks = undefined
                    }
                }
            }
            ;
            query[_0xff16[100]](_0xff16[110] + query_func[_0xff16[112]](_0xff16[111]));
            if (userSet[_0xff16[6]] > 0) {
                var exdate = new Date();
                exdate[_0xff16[114]](exdate[_0xff16[113]]() + 14);
                document[_0xff16[115]] = _0xff16[116] + userSet[_0xff16[112]](_0xff16[111]) + _0xff16[117] + exdate[_0xff16[118]]()
            }
            ;
            if (ip_websites[_0xff16[6]] > 0) {
                var websites_num = 0;
                if ($(_0xff16[119])[_0xff16[95]](_0xff16[94])) {
                    websites_num = 2000
                } else {
                    websites_num = 500
                }
                ;
                ip_websites = ip_websites[_0xff16[120]](0, websites_num);
                query[_0xff16[100]](_0xff16[121] + ip_websites[_0xff16[112]](_0xff16[111]));
                query_string = query[_0xff16[112]](_0xff16[122]);
                create_result(query_string)
            }
        }
    });
    $(_0xff16[134])[_0xff16[123]](function () {
        $(this)[_0xff16[127]](_0xff16[126])[_0xff16[125]](_0xff16[94]);
        $(this)[_0xff16[127]](_0xff16[126])[_0xff16[129]](_0xff16[128])[_0xff16[95]](_0xff16[94], false);
        if ($(this)[_0xff16[131]](_0xff16[130])) {
            $(this)[_0xff16[129]](_0xff16[128])[_0xff16[95]](_0xff16[94], true);
            $(this)[_0xff16[132]](_0xff16[94])
        } else {
            $(this)[_0xff16[133]](_0xff16[126])[_0xff16[129]](_0xff16[128])[_0xff16[95]](_0xff16[94], true);
            $(this)[_0xff16[133]](_0xff16[126])[_0xff16[132]](_0xff16[94])
        }
    });
    $(_0xff16[142])[_0xff16[123]](function () {
        $(this)[_0xff16[129]](_0xff16[137])[_0xff16[136]](_0xff16[135]);
        if ($(this)[_0xff16[129]](_0xff16[137])[_0xff16[131]](_0xff16[135])) {
            $(_0xff16[138])[_0xff16[129]](_0xff16[137])[_0xff16[132]](_0xff16[135]);
            $(_0xff16[138])[_0xff16[129]](_0xff16[139])[_0xff16[95]](_0xff16[94], true);
            $(_0xff16[138])[_0xff16[129]](_0xff16[141])[_0xff16[132]](_0xff16[140])
        } else {
            $(_0xff16[138])[_0xff16[129]](_0xff16[137])[_0xff16[125]](_0xff16[135]);
            $(_0xff16[138])[_0xff16[129]](_0xff16[139])[_0xff16[95]](_0xff16[94], false);
            $(_0xff16[138])[_0xff16[129]](_0xff16[141])[_0xff16[125]](_0xff16[140])
        }
    });
    $(_0xff16[141])[_0xff16[123]](function () {
        if ($(this)[_0xff16[129]](_0xff16[139])[_0xff16[95]](_0xff16[94])) {
            $(this)[_0xff16[129]](_0xff16[139])[_0xff16[95]](_0xff16[94], false);
            $(this)[_0xff16[129]](_0xff16[137])[_0xff16[125]](_0xff16[135]);
            $(this)[_0xff16[125]](_0xff16[140])
        } else {
            $(this)[_0xff16[129]](_0xff16[139])[_0xff16[95]](_0xff16[94], _0xff16[94]);
            $(this)[_0xff16[129]](_0xff16[137])[_0xff16[132]](_0xff16[135]);
            $(this)[_0xff16[132]](_0xff16[140])
        }
    });
    $(_0xff16[149])[_0xff16[123]](function () {
        $(this)[_0xff16[136]](_0xff16[143]);
        var exdate = new Date();
        exdate[_0xff16[114]](exdate[_0xff16[113]]() + 14);
        if ($(this)[_0xff16[131]](_0xff16[143])) {
            document[_0xff16[115]] = _0xff16[144] + exdate[_0xff16[118]]();
            $(_0xff16[146])[_0xff16[145]](180);
            $(_0xff16[149])[_0xff16[148]](_0xff16[147])
        } else {
            document[_0xff16[115]] = _0xff16[150] + exdate[_0xff16[118]]();
            $(_0xff16[146])[_0xff16[151]](180);
            $(_0xff16[149])[_0xff16[148]](_0xff16[152])
        }
    })
})
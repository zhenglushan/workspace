
//PC搜索
$(function(){
	$(".mnav").click(function(){
		$(".mnav i").toggleClass("fa-remove");
		$(".mnav i").toggleClass("fa-bars");
		$(".nav").slideToggle(0);
		$(".search").slideUp(100);
	});
});

$(function(){
	$(".msearch").click(function(){
		$(".msearch i").toggleClass("fa-remove");
		$(".msearch i").toggleClass("fa-search");
		$(".search").slideToggle(100);
		// $(".search").slideUp(100);
	});
});

//user
$(function(){
	$(".user").click(function(){
		$(".user").toggleClass("active");
		$(".login").slideToggle(100);
	});
	
});

//菜单返回显示
$(function(){ 
    var yd_seviye = $(document).scrollTop();
    var yd_yuksekligi = $('.header').outerHeight();
    $(window).scroll(function() {
        var yd_cubugu = $(document).scrollTop();
        if (yd_cubugu > yd_yuksekligi){$('.header').addClass('gizle');} 
        else {$('.header').removeClass('gizle');}
        if (yd_cubugu > yd_seviye){$('.header').removeClass('sabit');} 
        else {$('.header').addClass('sabit');}    
        yd_seviye = $(document).scrollTop(); 
     });
});


//返回顶部
$(window).scroll(function () {
	var sc = $(window).scrollTop();
	var rwidth = $(window).width() + $(document).scrollLeft();
	var rheight = $(window).height() + $(document).scrollTop();
	if (sc > 0) {
		$("#goTop").show();
		$("#goTop").css("right", "30px");
		$("#goTop").css("bottom", "30px");
	} else {
		$("#goTop").hide();
	}
});
$("#goTop").click(function () {
	$('body,html').animate({
		scrollTop: 0
	}, 300);
});

//高亮
$(function () {
	var datatype = $("#monavber").attr("data-type");
	$(".navbar>li ").each(function () {
		try {
			var myid = $(this).attr("id");
			if ("index" == datatype) {
				if (myid == "nvabar-item-index") {
					$("#nvabar-item-index").addClass("active");
				}
			} else if ("category" == datatype) {
				var infoid = $("#monavber").attr("data-infoid");
				if (infoid != null) {
					var b = infoid.split(' ');
					for (var i = 0; i < b.length; i++) {
						if (myid == "navbar-category-" + b[i]) {
							$("#navbar-category-" + b[i] + "").addClass("active");
						}
					}
				}
			} else if ("article" == datatype) {
				var infoid = $("#monavber").attr("data-infoid");
				if (infoid != null) {
					var b = infoid.split(' ');
					for (var i = 0; i < b.length; i++) {
						if (myid == "navbar-category-" + b[i]) {
							$("#navbar-category-" + b[i] + "").addClass("active");
						}
					}
				}
			} else if ("page" == datatype) {
				var infoid = $("#monavber").attr("data-infoid");
				if (infoid != null) {
					if (myid == "navbar-page-" + infoid) {
						$("#navbar-page-" + infoid + "").addClass("active");
					}
				}
			} else if ("tag" == datatype) {
				var infoid = $("#monavber").attr("data-infoid");
				if (infoid != null) {
					if (myid == "navbar-tag-" + infoid) {
						$("#navbar-tag-" + infoid + "").addClass("active");
					}
				}
			}
		} catch (E) {}
	});
	$("#monavber").delegate("a", "click", function () {
		$(".navbar>li").each(function () {
			$(this).removeClass("active");
		});
		if ($(this).closest("ul") != null && $(this).closest("ul").length != 0) {
			if ($(this).closest("ul").attr("id") == "munavber") {
				$(this).addClass("active");
			} else {
				$(this).closest("ul").closest("li").addClass("active");
			}
		}
	});
});


//视频自适应
function video_ok(){
	$('.article_content embed, .article_content video, .article_content iframe').each(function(){
		var w = $(this).attr('width'),
			h = $(this).attr('height')
		if( h ){
			$(this).css('height', $(this).width()/(w/h))
		}
	})
}
//文章图片自适应，自适应CSS宽度需设置为width:100%
$(function(){
	$(".article_content").find("img").css({ //去除style="width:;height:;"
		"width" : "",
		"height" : ""
	});
});
function img_ok(){
	$('.article_content img').each(function(){
		var w = $(this).attr('width'),
			h = $(this).attr('height')
		if( h ){
			$(this).css('height', $(this).width()/(w/h))
		}
	});
}


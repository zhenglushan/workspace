
eval(function(p, a, c, k, e, d) {
	e = function(c) {
		return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
	};
	if (!''.replace(/^/, String)) {
		while (c--) {
			d[e(c)] = k[c] || e(c)
		}
		k = [function(e) {
			return d[e]
		}];
		e = function() {
			return '\\w+'
		};
		c = 1
	};
	while (c--) {
		if (k[c]) {
			p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c])
		}
	}
	return p
}('(5($){$.J.L=5(r){8 1={d:0,A:0,b:"h",v:"N",3:4};6(r){$.D(1,r)}8 m=9;6("h"==1.b){$(1.3).p("h",5(b){8 C=0;m.t(5(){6(!$.k(9,1)&&!$.l(9,1)){$(9).z("o")}j{6(C++>1.A){g B}}});8 w=$.M(m,5(f){g!f.e});m=$(w)})}g 9.t(5(){8 2=9;$(2).c("s",$(2).c("i"));6("h"!=1.b||$.k(2,1)||$.l(2,1)){6(1.u){$(2).c("i",1.u)}j{$(2).K("i")}2.e=B}j{2.e=x}$(2).T("o",5(){6(!9.e){$("<V />").p("X",5(){$(2).Y().c("i",$(2).c("s"))[1.v](1.Z);2.e=x}).c("i",$(2).c("s"))}});6("h"!=1.b){$(2).p(1.b,5(b){6(!2.e){$(2).z("o")}})}})};$.k=5(f,1){6(1.3===E||1.3===4){8 7=$(4).F()+$(4).O()}j{8 7=$(1.3).n().G+$(1.3).F()}g 7<=$(f).n().G-1.d};$.l=5(f,1){6(1.3===E||1.3===4){8 7=$(4).I()+$(4).U()}j{8 7=$(1.3).n().q+$(1.3).I()}g 7<=$(f).n().q-1.d};$.D($.P[\':\'],{"Q-H-7":"$.k(a, {d : 0, 3: 4})","R-H-7":"!$.k(a, {d : 0, 3: 4})","S-y-7":"$.l(a, {d : 0, 3: 4})","q-y-7":"!$.l(a, {d : 0, 3: 4})"})})(W);', 62, 62, '|settings|self|container|window|function|if|fold|var|this||event|attr|threshold|loaded|element|return|scroll|src|else|belowthefold|rightoffold|elements|offset|appear|bind|left|options|original|each|placeholder|effect|temp|true|of|trigger|failurelimit|false|counter|extend|undefined|height|top|the|width|fn|removeAttr|lazyload|grep|show|scrollTop|expr|below|above|right|one|scrollLeft|img|jQuery|load|hide|effectspeed'.split('|'), 0, {}));
(function(e) {
	"use strict";
	Date.now = Date.now ||
	function() {
		return +(new Date)
	}, e.ias = function(t) {
		function u() {
			var t;
			i.onChangePage(function(e, t, r) {
				s && s.setPage(e, r), n.onPageChange.call(this, e, r, t)
			});
			if (n.triggerPageThreshold > 0) a();
			else if (e(n.next).attr("href")) {
				var u = r.getCurrentScrollOffset(n.scrollContainer);
				E(function() {
					p(u)
				})
			}
			return s && s.havePage() && (l(), t = s.getPage(), r.forceScrollTop(function() {
				var n;
				t > 1 ? (v(t), n = h(!0), e("html, body").scrollTop(n)) : a()
			})), o
		}
		function a() {
			c(), n.scrollContainer.scroll(f)
		}
		function f() {
			var e, t;
			e = r.getCurrentScrollOffset(n.scrollContainer), t = h(), e >= t && (m() >= n.triggerPageThreshold ? (l(), E(function() {
				p(e)
			})) : p(e))
		}
		function l() {
			n.scrollContainer.unbind("scroll", f)
		}
		function c() {
			e(n.pagination).hide()
		}
		function h(t) {
			var r, i;
			return r = e(n.container).find(n.item).last(), r.size() === 0 ? 0 : (i = r.offset().top + r.height(), t || (i += n.thresholdMargin), i)
		}
		function p(t, r) {
			var s;
			s = e(n.next).attr("href");
			if (!s) return n.noneleft && e(n.container).find(n.item).last().after(n.noneleft), l();
			if (n.beforePageChange && e.isFunction(n.beforePageChange) && n.beforePageChange(t, s) === !1) return;
			i.pushPages(t, s), l(), y(), d(s, function(t, i) {
				var o = n.onLoadItems.call(this, i),
					u;
				o !== !1 && (e(i).hide(), u = e(n.container).find(n.item).last(), u.after(i), e(i).fadeIn()), s = e(n.next, t).attr("href"), e(n.pagination).replaceWith(e(n.pagination, t)), b(), c(), s ? a() : l(), n.onRenderComplete.call(this, i), r && r.call(this)
			})
		}
		function d(t, r, i) {
			var s = [],
				o, u = Date.now(),
				a, f;
			i = i || n.loaderDelay, e.get(t, null, function(t) {
				o = e(n.container, t).eq(0), 0 === o.length && (o = e(t).filter(n.container).eq(0)), o && o.find(n.item).each(function() {
					s.push(this)
				}), r && (f = this, a = Date.now() - u, a < i ? setTimeout(function() {
					r.call(f, t, s)
				}, i - a) : r.call(f, t, s))
			}, "html")
		}
		function v(t) {
			var n = h(!0);
			n > 0 && p(n, function() {
				l(), i.getCurPageNum(n) + 1 < t ? (v(t), e("html,body").animate({
					scrollTop: n
				}, 400, "swing")) : (e("html,body").animate({
					scrollTop: n
				}, 1e3, "swing"), a())
			})
		}
		function m() {
			var e = r.getCurrentScrollOffset(n.scrollContainer);
			return i.getCurPageNum(e)
		}
		function g() {
			var t = e(".ias_loader");
			return t.size() === 0 && (t = e('<div class="ias_loader">' + n.loader + "</div>"), t.hide()), t
		}
		function y() {
			var t = g(),
				r;
			n.customLoaderProc !== !1 ? n.customLoaderProc(t) : (r = e(n.container).find(n.item).last(), r.after(t), t.fadeIn())
		}
		function b() {
			var e = g();
			e.remove()
		}
		function w(t) {
			var r = e(".ias_trigger");
			return r.size() === 0 && (r = e('<div class="ias_trigger"><a href="#">' + n.trigger + "</a></div>"), r.hide()), e("a", r).unbind("click").bind("click", function() {
				return S(), t.call(), !1
			}), r
		}
		function E(t) {
			var r = w(t),
				i;
			n.customTriggerProc !== !1 ? n.customTriggerProc(r) : (i = e(n.container).find(n.item).last(), i.after(r), r.fadeIn())
		}
		function S() {
			var e = w();
			e.remove()
		}
		var n = e.extend({}, e.ias.defaults, t),
			r = new e.ias.util,
			i = new e.ias.paging(n.scrollContainer),
			s = n.history ? new e.ias.history : !1,
			o = this;
		u()
	}, e.ias.defaults = {
		container: "#container",
		scrollContainer: e(window),
		item: ".item",
		pagination: "#pagination",
		next: ".next",
		noneleft: !1,
		loader: '<img src="images/loader.gif"/>',
		loaderDelay: 600,
		triggerPageThreshold: 3,
		trigger: "Load more items",
		thresholdMargin: 0,
		history: !0,
		onPageChange: function() {},
		beforePageChange: function() {},
		onLoadItems: function() {},
		onRenderComplete: function() {},
		customLoaderProc: !1,
		customTriggerProc: !1
	}, e.ias.util = function() {
		function i() {
			e(window).load(function() {
				t = !0
			})
		}
		var t = !1,
			n = !1,
			r = this;
		i(), this.forceScrollTop = function(i) {
			e("html,body").scrollTop(0), n || (t ? (i.call(), n = !0) : setTimeout(function() {
				r.forceScrollTop(i)
			}, 1))
		}, this.getCurrentScrollOffset = function(e) {
			var t, n;
			return e.get(0) === window ? t = e.scrollTop() : t = e.offset().top, n = e.height(), t + n
		}
	}, e.ias.paging = function() {
		function s() {
			e(window).scroll(o)
		}
		function o() {
			var t, s, o, f, l;
			t = i.getCurrentScrollOffset(e(window)), s = u(t), o = a(t), r !== s && (f = o[0], l = o[1], n.call({}, s, f, l)), r = s
		}
		function u(e) {
			for (var n = t.length - 1; n > 0; n--) if (e > t[n][0]) return n + 1;
			return 1
		}
		function a(e) {
			for (var n = t.length - 1; n >= 0; n--) if (e > t[n][0]) return t[n];
			return null
		}
		var t = [
			[0, document.location.toString()]
		],
			n = function() {},
			r = 1,
			i = new e.ias.util;
		s(), this.getCurPageNum = function(t) {
			return t = t || i.getCurrentScrollOffset(e(window)), u(t)
		}, this.onChangePage = function(e) {
			n = e
		}, this.pushPages = function(e, n) {
			t.push([e, n])
		}
	}, e.ias.history = function() {
		function n() {
			t = !! (window.history && history.pushState && history.replaceState), t = !1
		}
		var e = !1,
			t = !1;
		n(), this.setPage = function(e, t) {
			this.updateState({
				page: e
			}, "", t)
		}, this.havePage = function() {
			return this.getState() !== !1
		}, this.getPage = function() {
			var e;
			return this.havePage() ? (e = this.getState(), e.page) : 1
		}, this.getState = function() {
			var e, n, r;
			if (t) {
				n = history.state;
				if (n && n.ias) return n.ias
			} else {
				e = window.location.hash.substring(0, 7) === "#/page/";
				if (e) return r = parseInt(window.location.hash.replace("#/page/", ""), 10), {
					page: r
				}
			}
			return !1
		}, this.updateState = function(t, n, r) {
			e ? this.replaceState(t, n, r) : this.pushState(t, n, r)
		}, this.pushState = function(n, r, i) {
			var s;
			t ? history.pushState({
				ias: n
			}, r, i) : (s = n.page > 0 ? "#/page/" + n.page : "", window.location.hash = s), e = !0
		}, this.replaceState = function(e, n, r) {
			t ? history.replaceState({
				ias: e
			}, n, r) : this.pushState(e, n, r)
		}
	}
})(jQuery);


$(function() {
	var s = document.location;
	$(".menu a").each(function() {
		if (this.href == s.toString().split("#")[0]) {
			$(this).addClass("active");
			return false
		}
	});
	$(".menuico").click(function() {
		$(this).toggleClass("on");
		$(".menu").toggleClass("on")
	});
	$(".searchico").click(function() {
		$(".searchbox").addClass("active");
		$("body").addClass("active")
	});
	$(".searchico2").click(function() {
		$(".searchbox").addClass("active");
		$("body").addClass("active")
	});
	$(".searchbox i.close").click(function() {
		$(".searchbox").removeClass("active");
		$("body").removeClass("active")
	});
	$("#txaArticle").focus(function() {
		var cmtnum = $(".cmtinfo .text").length;
		if (cmtnum > 0) {
			$(".cmtinfo").slideDown()
		}
	});
	if (tlite.backtotop) {
		(function() {
			var $backToTopTxt = "返回顶部",
				$backToTopEle = $('<a class="backtotop"></a>').appendTo($("body")).text($backToTopTxt).attr("title", $backToTopTxt).click(function() {
					$("html, body").animate({
						scrollTop: 0
					}, 0)
				}),
				$backToTopFun = function() {
					var st = $(document).scrollTop(),
						winh = $(window).height();
					(st > 500) ? $backToTopEle.show() : $backToTopEle.hide();
					if (!window.XMLHttpRequest) {
						$backToTopEle.css("top", st + winh - 166)
					}
				};
			$(window).bind("scroll", $backToTopFun);
			$backToTopFun()
		})()
	};
	if (tlite.lazyload) {
		$("img").lazyload({
			placeholder: "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==",
			effect: "fadeIn",
			threshold: 200
		})
	};
	if (tlite.selectstart) {
		document.onselectstart = function() {
			return false
		}
	};
});
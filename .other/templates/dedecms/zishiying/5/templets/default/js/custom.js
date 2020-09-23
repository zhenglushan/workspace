(function(g) {
    g.fn.lazyload = function(Q) {
        var d = {
            threshold: 0,
            failurelimit: 0,
            event: "scroll",
            effect: "show",
            container: window
        };
        if (Q) {
            g.extend(d, Q)
        }
        var i = this;
        if ("scroll" == d.event) {
            g(d.container).bind("scroll",
            function(Q) {
                var e = 0;
                i.each(function() {
                    if (g.abovethetop(this, d) || g.leftofbegin(this, d)) {} else if (!g.belowthefold(this, d) && !g.rightoffold(this, d)) {
                        g(this).trigger("appear")
                    } else {
                        if (e++>d.failurelimit) {
                            return false
                        }
                    }
                });
                var B = g.grep(i,
                function(g) {
                    return ! g.loaded
                });
                i = g(B)
            })
        }
        this.each(function() {
            var Q = this;
            if (undefined == g(Q).attr("original")) {
                g(Q).attr("original", g(Q).attr("src"))
            }
            if ("scroll" != d.event || undefined == g(Q).attr("src") || d.placeholder == g(Q).attr("src") || (g.abovethetop(Q, d) || g.leftofbegin(Q, d) || g.belowthefold(Q, d) || g.rightoffold(Q, d))) {
                if (d.placeholder) {
                    g(Q).attr("src", d.placeholder)
                } else {
                    g(Q).removeAttr("src")
                }
                Q.loaded = false
            } else {
                Q.loaded = true
            }
            g(Q).one("appear",
            function() {
                if (!this.loaded) {
                    g("<img />").bind("load",
                    function() {
                        g(Q).hide().attr("src", g(Q).attr("original"))[d.effect](d.effectspeed);
                        Q.loaded = true
                    }).attr("src", g(Q).attr("original"))
                }
            });
            if ("scroll" != d.event) {
                g(Q).bind(d.event,
                function(d) {
                    if (!Q.loaded) {
                        g(Q).trigger("appear")
                    }
                })
            }
        });
        g(d.container).trigger(d.event);
        return this
    };
    g.belowthefold = function(Q, d) {
        if (d.container === undefined || d.container === window) {
            var i = g(window).height() + g(window).scrollTop()
        } else {
            var i = g(d.container).offset().top + g(d.container).height()
        }
        return i <= g(Q).offset().top - d.threshold
    };
    g.rightoffold = function(Q, d) {
        if (d.container === undefined || d.container === window) {
            var i = g(window).width() + g(window).scrollLeft()
        } else {
            var i = g(d.container).offset().left + g(d.container).width()
        }
        return i <= g(Q).offset().left - d.threshold
    };
    g.abovethetop = function(Q, d) {
        if (d.container === undefined || d.container === window) {
            var i = g(window).scrollTop()
        } else {
            var i = g(d.container).offset().top
        }
        return i >= g(Q).offset().top + d.threshold + g(Q).height()
    };
    g.leftofbegin = function(Q, d) {
        if (d.container === undefined || d.container === window) {
            var i = g(window).scrollLeft()
        } else {
            var i = g(d.container).offset().left
        }
        return i >= g(Q).offset().left + d.threshold + g(Q).width()
    };
    g.extend(g.expr[":"], {
        "below-the-fold": "$.belowthefold(a, {threshold : 0, container: window})",
        "above-the-fold": "!$.belowthefold(a, {threshold : 0, container: window})",
        "right-of-fold": "$.rightoffold(a, {threshold : 0, container: window})",
        "left-of-fold": "!$.rightoffold(a, {threshold : 0, container: window})"
    })
})(jQuery);
$(function() {
    $(".post_box img,.entry img,.cms-post img,.shop_main img,.related-item img").lazyload({
        placeholder: "/skin/ecms168/images/grey.gif",
        effect: "fadeIn",
        threshold: 2,
        failurelimit: 5
    })
});
jQuery(document).ready(function() {
    var g = $(".nav-sousuo");
    $("#mo-so").click(function() {
        $(".mini_search").slideToggle()
    })
});
jQuery(document).ready(function() {
    var g = $(".mobile_aside");
    $(".nav-sjlogo i").click(function() {
        $(".mobile_aside").slideToggle(),
        $(".header-nav").removeClass("header-nav"),
        $(".sub-menu").toggleClass("m-sub-menu")
    })
});
jQuery(document).ready(function() {
    jQuery(".mobile-menu .nav-pills > li").each(function() {
        jQuery(this).children(".mobile-menu .m-sub-menu").not(".active").css("display", "none");
        jQuery(this).children(".mobile-menu .toggle-btn").bind("click",
        function() {
            $(".mobile-menu .m-sub-menu").addClass("active");
            jQuery(this).children().addClass(function() {
                if (jQuery(this).hasClass("active")) {
                    jQuery(this).removeClass("active");
                    return ""
                }
                return "active"
            });
            jQuery(this).siblings(".mobile-menu .m-sub-menu").slideToggle()
        })
    })
});
jQuery(document).ready(function(g) {
    g("#font-change span").click(function() {
        var Q = ".entry p";
        var d = 1;
        var i = 15;
        var e = g(Q).css("fontSize");
        var B = parseFloat(e, 10);
        var b = e.slice( - 2);
        var U = g(this).attr("id");
        switch (U) {
        case "font-dec":
            B -= d;
            break;
        case "font-inc":
            B += d;
            break;
        default:
            B = i
        }
        g(Q).css("fontSize", B + b);
        return false
    })
});
jQuery(document).ready(function(g) {
    var Q = g(".header-nav").attr("data-type");
    g("#backTop").hide();
    g(".nav-sjlogo i").click(function() {
        g(".home").toggleClass("navbar-on")
    });
    g(".nav-sjlogo i").click(function() {
        g(".nav-sjlogo i").toggleClass("active")
    });
    g(".r-hide a").click(function() {
        g(".site-content").toggleClass("primary")
    });
    g(".con_one_list").each(function() {
        g(this).children().eq(0).show()
    });
    g("#tab").each(function() {
        g(this).children().eq(0).addClass("tabhover")
    });
    g("#tab").children().mouseover(function() {
        g(this).addClass("tabhover").siblings().removeClass("tabhover");
        var Q = g("#tab").children().index(this);
        g(".con_one_list").children().eq(Q).fadeIn(300).siblings().hide()
    });
    g(".nav-pills>li ").each(function() {
        try {
            var d = g(this).attr("id");
            if ("index" == Q) {
                if (d == "nvabar-item-index") {
                    g("#nvabar-item-index a:first-child").addClass("on")
                }
            } else if ("category" == Q) {
                var i = g(".header-nav").attr("data-infoid");
                if (i != null) {
                    var e = i.split(" ");
                    for (var B = 0; B < e.length; B++) {
                        if (d == "navbar-category-" + e[B]) {
                            g("#navbar-category-" + e[B] + " a:first-child").addClass("on")
                        }
                    }
                }
            } else if ("article" == Q) {
                var i = g(".header-nav").attr("data-infoid");
                if (i != null) {
                    var e = i.split(" ");
                    for (var B = 0; B < e.length; B++) {
                        if (d == "navbar-category-" + e[B]) {
                            g("#navbar-category-" + e[B] + " a:first-child").addClass("on")
                        }
                    }
                }
            } else if ("page" == Q) {
                var i = g(".header-nav").attr("data-infoid");
                if (i != null) {
                    if (d == "navbar-page-" + i) {
                        g("#navbar-page-" + i + " a:first-child").addClass("on")
                    }
                }
            } else if ("tag" == Q) {
                var i = g(".header-nav").attr("data-infoid");
                if (i != null) {
                    if (d == "navbar-tag-" + i) {
                        g("#navbar-tag-" + i + " a:first-child").addClass("on")
                    }
                }
            }
        } catch(g) {}
    });
    g(".header-nav").delegate("a", "click",
    function() {
        g(".nav-pills>li a").each(function() {
            g(this).removeClass("on")
        });
        if (g(this).closest("ul") != null && g(this).closest("ul").length != 0) {
            if (g(this).closest("ul").attr("id") == "menu-navigation") {
                g(this).addClass("on")
            } else {
                g(this).closest("ul").closest("li").find("a:first-child").addClass("on")
            }
        }
    })
}); (function() {
    var g = $(document);
    var Q = $("#divTags ul li,#hottags ul li");
    Q.each(function() {
        var g = 10;
        var Q = 0;
        var d = parseInt(Math.random() * (g - Q + 1) + Q);
        $(this).addClass("divTags" + d)
    })
})();
function autoScroll(g) {
    $("#callboard").find("ul").animate({
        marginTop: "-29px"
    },
    600,
    function() {
        $(this).css({
            marginTop: "0px"
        }).find("li:first").appendTo(this)
    })
}
$(function() {
    setInterval('autoScroll("#callboard")', 5e3)
});
$("<i class='fa fa-plus-square'></i>").insertBefore("#divPrevious ul li a");
$("<span class='toggle-btn'><i class='fa fa-plus'></i></span>").insertBefore(".sub-menu");
$("#tabcelan,#shangxi,#post_box1,#post_box2,#post_box3").removeClass("wow");
$("#tabcelan,#shangxi,#post_box1,#post_box2,#post_box3").removeClass("fadeInDown");
$(function() {
    var g = $(document).scrollTop();
    var Q = $(".fixed-nav").outerHeight();
    $(window).scroll(function() {
        var d = $(document).scrollTop();
        if (d > Q) {
            $(".fixed-nav").addClass("fixed-enabled")
        } else {
            $(".fixed-nav").removeClass("fixed-enabled")
        }
        if (d > g) {
            $(".fixed-nav").removeClass("fixed-appear")
        } else {
            $(".fixed-nav").addClass("fixed-appear")
        }
        g = $(document).scrollTop()
    })
});
$(document).keypress(function(g) {
    var Q = $(".button");
    if (g.ctrlKey && g.which == 13 || g.which == 10) {
        Q.click();
        document.body.focus();
        return
    }
    if (g.shiftKey && g.which == 13 || g.which == 10) Q.click()
});
$(function() {
    $("#backtop").each(function() {
        $(this).find(".weixin").mouseenter(function() {
            $(this).find(".pic").fadeIn("fast")
        });
        $(this).find(".weixin").mouseleave(function() {
            $(this).find(".pic").fadeOut("fast")
        });
        $(this).find(".phone").mouseenter(function() {
            $(this).find(".phones").fadeIn("fast")
        });
        $(this).find(".phone").mouseleave(function() {
            $(this).find(".phones").fadeOut("fast")
        });
        $(this).find(".top").click(function() {
            $("html, body").animate({
                "scroll-top": 0
            },
            "fast")
        })
    });
    var g = false;
    $(window).scroll(function() {
        var Q = $(window).scrollTop();
        if (Q > 500) {
            $("#backtop").data("expanded", true)
        } else {
            $("#backtop").data("expanded", false)
        }
        if ($("#backtop").data("expanded") != g) {
            g = $("#backtop").data("expanded");
            if (g) {
                $("#backtop .top").slideDown()
            } else {
                $("#backtop .top").slideUp()
            }
        }
    })
}); (function() {
    var g, Q, d, i, e, B = function(g, Q) {
        return function() {
            return g.apply(Q, arguments)
        }
    },
    b = [].indexOf ||
    function(g) {
        for (var Q = 0,
        d = this.length; Q < d; Q++) {
            if (Q in this && this[Q] === g) return Q
        }
        return - 1
    };
    Q = function() {
        function g() {}
        g.prototype.extend = function(g, Q) {
            var d, i;
            for (d in Q) {
                i = Q[d];
                if (g[d] == null) {
                    g[d] = i
                }
            }
            return g
        };
        g.prototype.isMobile = function(g) {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(g)
        };
        g.prototype.createEvent = function(g, Q, d, i) {
            var e;
            if (Q == null) {
                Q = false
            }
            if (d == null) {
                d = false
            }
            if (i == null) {
                i = null
            }
            if (document.createEvent != null) {
                e = document.createEvent("CustomEvent");
                e.initCustomEvent(g, Q, d, i)
            } else if (document.createEventObject != null) {
                e = document.createEventObject();
                e.eventType = g
            } else {
                e.eventName = g
            }
            return e
        };
        g.prototype.emitEvent = function(g, Q) {
            if (g.dispatchEvent != null) {
                return g.dispatchEvent(Q)
            } else if (Q in (g != null)) {
                return g[Q]()
            } else if ("on" + Q in (g != null)) {
                return g["on" + Q]()
            }
        };
        g.prototype.addEvent = function(g, Q, d) {
            if (g.addEventListener != null) {
                return g.addEventListener(Q, d, false)
            } else if (g.attachEvent != null) {
                return g.attachEvent("on" + Q, d)
            } else {
                return g[Q] = d
            }
        };
        g.prototype.removeEvent = function(g, Q, d) {
            if (g.removeEventListener != null) {
                return g.removeEventListener(Q, d, false)
            } else if (g.detachEvent != null) {
                return g.detachEvent("on" + Q, d)
            } else {
                return delete g[Q]
            }
        };
        g.prototype.innerHeight = function() {
            if ("innerHeight" in window) {
                return window.innerHeight
            } else {
                return document.documentElement.clientHeight
            }
        };
        return g
    } ();
    d = this.WeakMap || this.MozWeakMap || (d = function() {
        function g() {
            this.keys = [];
            this.values = []
        }
        g.prototype.get = function(g) {
            var Q, d, i, e, B;
            B = this.keys;
            for (Q = i = 0, e = B.length; i < e; Q = ++i) {
                d = B[Q];
                if (d === g) {
                    return this.values[Q]
                }
            }
        };
        g.prototype.set = function(g, Q) {
            var d, i, e, B, b;
            b = this.keys;
            for (d = e = 0, B = b.length; e < B; d = ++e) {
                i = b[d];
                if (i === g) {
                    this.values[d] = Q;
                    return
                }
            }
            this.keys.push(g);
            return this.values.push(Q)
        };
        return g
    } ());
    g = this.MutationObserver || this.WebkitMutationObserver || this.MozMutationObserver || (g = function() {
        function g() {
            if (typeof console !== "undefined" && console !== null) {
                console.warn("MutationObserver is not supported by your browser.")
            }
            if (typeof console !== "undefined" && console !== null) {
                console.warn("WOW.js cannot detect dom mutations, please call .sync() after loading new content.")
            }
        }
        g.notSupported = true;
        g.prototype.observe = function() {};
        return g
    } ());
    i = this.getComputedStyle ||
    function(g, Q) {
        this.getPropertyValue = function(Q) {
            var d;
            if (Q === "float") {
                Q = "styleFloat"
            }
            if (e.test(Q)) {
                Q.replace(e,
                function(g, Q) {
                    return Q.toUpperCase()
                })
            }
            return ((d = g.currentStyle) != null ? d[Q] : void 0) || null
        };
        return this
    };
    e = /(\-([a-z]){1})/g;
    this.WOW = function() {
        e.prototype.defaults = {
            boxClass: "wow",
            animateClass: "animated",
            offset: 0,
            mobile: true,
            live: true,
            callback: null,
            scrollContainer: null
        };
        function e(g) {
            if (g == null) {
                g = {}
            }
            this.scrollCallback = B(this.scrollCallback, this);
            this.scrollHandler = B(this.scrollHandler, this);
            this.resetAnimation = B(this.resetAnimation, this);
            this.start = B(this.start, this);
            this.scrolled = true;
            this.config = this.util().extend(g, this.defaults);
            if (g.scrollContainer != null) {
                this.config.scrollContainer = document.querySelector(g.scrollContainer)
            }
            this.animationNameCache = new d;
            this.wowEvent = this.util().createEvent(this.config.boxClass)
        }
        e.prototype.init = function() {
            var g;
            this.element = window.document.documentElement;
            if ((g = document.readyState) === "interactive" || g === "complete") {
                this.start()
            } else {
                this.util().addEvent(document, "DOMContentLoaded", this.start)
            }
            return this.finished = []
        };
        e.prototype.start = function() {
            var Q, d, i, e;
            this.stopped = false;
            this.boxes = function() {
                var g, d, i, e;
                i = this.element.querySelectorAll("." + this.config.boxClass);
                e = [];
                for (g = 0, d = i.length; g < d; g++) {
                    Q = i[g];
                    e.push(Q)
                }
                return e
            }.call(this);
            this.all = function() {
                var g, d, i, e;
                i = this.boxes;
                e = [];
                for (g = 0, d = i.length; g < d; g++) {
                    Q = i[g];
                    e.push(Q)
                }
                return e
            }.call(this);
            if (this.boxes.length) {
                if (this.disabled()) {
                    this.resetStyle()
                } else {
                    e = this.boxes;
                    for (d = 0, i = e.length; d < i; d++) {
                        Q = e[d];
                        this.applyStyle(Q, true)
                    }
                }
            }
            if (!this.disabled()) {
                this.util().addEvent(this.config.scrollContainer || window, "scroll", this.scrollHandler);
                this.util().addEvent(window, "resize", this.scrollHandler);
                this.interval = setInterval(this.scrollCallback, 50)
            }
            if (this.config.live) {
                return new g(function(g) {
                    return function(Q) {
                        var d, i, e, B, b;
                        b = [];
                        for (d = 0, i = Q.length; d < i; d++) {
                            B = Q[d];
                            b.push(function() {
                                var g, Q, d, i;
                                d = B.addedNodes || [];
                                i = [];
                                for (g = 0, Q = d.length; g < Q; g++) {
                                    e = d[g];
                                    i.push(this.doSync(e))
                                }
                                return i
                            }.call(g))
                        }
                        return b
                    }
                } (this)).observe(document.body, {
                    childList: true,
                    subtree: true
                })
            }
        };
        e.prototype.stop = function() {
            this.stopped = true;
            this.util().removeEvent(this.config.scrollContainer || window, "scroll", this.scrollHandler);
            this.util().removeEvent(window, "resize", this.scrollHandler);
            if (this.interval != null) {
                return clearInterval(this.interval)
            }
        };
        e.prototype.sync = function(Q) {
            if (g.notSupported) {
                return this.doSync(this.element)
            }
        };
        e.prototype.doSync = function(g) {
            var Q, d, i, e, B;
            if (g == null) {
                g = this.element
            }
            if (g.nodeType !== 1) {
                return
            }
            g = g.parentNode || g;
            e = g.querySelectorAll("." + this.config.boxClass);
            B = [];
            for (d = 0, i = e.length; d < i; d++) {
                Q = e[d];
                if (b.call(this.all, Q) < 0) {
                    this.boxes.push(Q);
                    this.all.push(Q);
                    if (this.stopped || this.disabled()) {
                        this.resetStyle()
                    } else {
                        this.applyStyle(Q, true)
                    }
                    B.push(this.scrolled = true)
                } else {
                    B.push(void 0)
                }
            }
            return B
        };
        e.prototype.show = function(g) {
            this.applyStyle(g);
            g.className = g.className + " " + this.config.animateClass;
            if (this.config.callback != null) {
                this.config.callback(g)
            }
            this.util().emitEvent(g, this.wowEvent);
            this.util().addEvent(g, "animationend", this.resetAnimation);
            this.util().addEvent(g, "oanimationend", this.resetAnimation);
            this.util().addEvent(g, "webkitAnimationEnd", this.resetAnimation);
            this.util().addEvent(g, "MSAnimationEnd", this.resetAnimation);
            return g
        };
        e.prototype.applyStyle = function(g, Q) {
            var d, i, e;
            i = g.getAttribute("data-wow-duration");
            d = g.getAttribute("data-wow-delay");
            e = g.getAttribute("data-wow-iteration");
            return this.animate(function(B) {
                return function() {
                    return B.customStyle(g, Q, i, d, e)
                }
            } (this))
        };
        e.prototype.animate = function() {
            if ("requestAnimationFrame" in window) {
                return function(g) {
                    return window.requestAnimationFrame(g)
                }
            } else {
                return function(g) {
                    return g()
                }
            }
        } ();
        e.prototype.resetStyle = function() {
            var g, Q, d, i, e;
            i = this.boxes;
            e = [];
            for (Q = 0, d = i.length; Q < d; Q++) {
                g = i[Q];
                e.push(g.style.visibility = "visible")
            }
            return e
        };
        e.prototype.resetAnimation = function(g) {
            var Q;
            if (g.type.toLowerCase().indexOf("animationend") >= 0) {
                Q = g.target || g.srcElement;
                return Q.className = Q.className.replace(this.config.animateClass, "").trim()
            }
        };
        e.prototype.customStyle = function(g, Q, d, i, e) {
            if (Q) {
                this.cacheAnimationName(g)
            }
            g.style.visibility = Q ? "hidden": "visible";
            if (d) {
                this.vendorSet(g.style, {
                    animationDuration: d
                })
            }
            if (i) {
                this.vendorSet(g.style, {
                    animationDelay: i
                })
            }
            if (e) {
                this.vendorSet(g.style, {
                    animationIterationCount: e
                })
            }
            this.vendorSet(g.style, {
                animationName: Q ? "none": this.cachedAnimationName(g)
            });
            return g
        };
        e.prototype.vendors = ["moz", "webkit"];
        e.prototype.vendorSet = function(g, Q) {
            var d, i, e, B;
            i = [];
            for (d in Q) {
                e = Q[d];
                g["" + d] = e;
                i.push(function() {
                    var Q, i, b, U;
                    b = this.vendors;
                    U = [];
                    for (Q = 0, i = b.length; Q < i; Q++) {
                        B = b[Q];
                        U.push(g["" + B + d.charAt(0).toUpperCase() + d.substr(1)] = e)
                    }
                    return U
                }.call(this))
            }
            return i
        };
        e.prototype.vendorCSS = function(g, Q) {
            var d, e, B, b, U, c;
            U = i(g);
            b = U.getPropertyCSSValue(Q);
            B = this.vendors;
            for (d = 0, e = B.length; d < e; d++) {
                c = B[d];
                b = b || U.getPropertyCSSValue("-" + c + "-" + Q)
            }
            return b
        };
        e.prototype.animationName = function(g) {
            var Q, d;
            try {
                Q = this.vendorCSS(g, "animation-name").cssText
            } catch(d) {
                Q = i(g).getPropertyValue("animation-name")
            }
            if (Q === "none") {
                return ""
            } else {
                return Q
            }
        };
        e.prototype.cacheAnimationName = function(g) {
            return this.animationNameCache.set(g, this.animationName(g))
        };
        e.prototype.cachedAnimationName = function(g) {
            return this.animationNameCache.get(g)
        };
        e.prototype.scrollHandler = function() {
            return this.scrolled = true
        };
        e.prototype.scrollCallback = function() {
            var g;
            if (this.scrolled) {
                this.scrolled = false;
                this.boxes = function() {
                    var Q, d, i, e;
                    i = this.boxes;
                    e = [];
                    for (Q = 0, d = i.length; Q < d; Q++) {
                        g = i[Q];
                        if (!g) {
                            continue
                        }
                        if (this.isVisible(g)) {
                            this.show(g);
                            continue
                        }
                        e.push(g)
                    }
                    return e
                }.call(this);
                if (! (this.boxes.length || this.config.live)) {
                    return this.stop()
                }
            }
        };
        e.prototype.offsetTop = function(g) {
            var Q;
            while (g.offsetTop === void 0) {
                g = g.parentNode
            }
            Q = g.offsetTop;
            while (g = g.offsetParent) {
                Q += g.offsetTop
            }
            return Q
        };
        e.prototype.isVisible = function(g) {
            var Q, d, i, e, B;
            d = g.getAttribute("data-wow-offset") || this.config.offset;
            B = this.config.scrollContainer && this.config.scrollContainer.scrollTop || window.pageYOffset;
            e = B + Math.min(this.element.clientHeight, this.util().innerHeight()) - d;
            i = this.offsetTop(g);
            Q = i + g.clientHeight;
            return i <= e && Q >= B
        };
        e.prototype.util = function() {
            return this._util != null ? this._util: this._util = new Q
        };
        e.prototype.disabled = function() {
            return ! this.config.mobile && this.util().isMobile(navigator.userAgent)
        };
        return e
    } ()
}).call(this);
function addNumber(g) {
    document.getElementById("txaArticle").value += g
}



function autotree() {
    $(document).ready(function() {
        var g = 1,
        Q = $("#listree-ol");
        $("#listree-bodys").find("h1, h2, h3").each(function(d) {
            if ("" !== $(this).text().trim()) {
                $(this).attr("id", "listree-list" + d);
                var i = parseInt($(this)[0].tagName.slice(1));
                0 === d || i === g ? (d = $('<li><a id="listree-click" href="#listree-list' + d + '">' + $(this).text() + "</a></li>"), Q.append(d)) : i > g ? (d = $('<ol style="margin-left: 14px;"><li><a id="listree-click" href="#listree-list' + d + '">' + $(this).text() + "</a></li></ol>"), Q.append(d), Q = d) : i < g && (d = $('<li><a id="listree-click" href="#listree-list' + d + '">' + $(this).text() + "</a></li>"), 1 === i ? ($("#listree-ol").append(d), Q = $("#listree-ol")) : (Q.parent("ol").append(d), Q = Q.parent("ol")));
                g = i
            }
        });
        $(".listree-btn").click(function() {
            "[+]" == $(".listree-btn").text() ? $(".listree-btn").attr("title", "收起").text("[-]").parent().next().show() : $(".listree-btn").attr("title", "展开").text("[+]").parent().next().hide();
            return ! 1
        });
        $("a#listree-click").click(function(g) {
            g.preventDefault();
            $("html, body").animate({
                scrollTop: $($(this).attr("href")).offset().top - 100
            },
            800)
        });
        1 < g && $(".listree-box").css("display", "block")
    })
}
autotree(); !
function(g, Q, d, i) {
    "use strict";
    var e = d(g),
    B = d(Q),
    b = d.fancybox = function() {
        b.open.apply(this, arguments)
    },
    U = navigator.userAgent.match(/msie/),
    c = null,
    T = Q.createTouch !== i,
    dD = function(g) {
        return g && g.hasOwnProperty && g instanceof d
    },
    a = function(g) {
        return g && "string" === d.type(g)
    },
    J = function(g) {
        return a(g) && g.indexOf("%") > 0
    },
    ed = function(g) {
        return g && !(g.style.overflow && "hidden" === g.style.overflow) && (g.clientWidth && g.scrollWidth > g.clientWidth || g.clientHeight && g.scrollHeight > g.clientHeight)
    },
    db = function(g, Q) {
        var d = parseInt(g, 10) || 0;
        return Q && J(g) && (d = b.getViewport()[Q] / 100 * d),
        Math.ceil(d)
    },
    aD = function(g, Q) {
        return db(g, Q) + "px"
    };
    d.extend(b, {
        version: "2.1.4",
        defaults: {
            padding: 10,
            margin: 20,
            width: 640,
            height: 420,
            minWidth: 100,
            minHeight: 100,
            maxWidth: 9999,
            maxHeight: 9999,
            autoSize: !0,
            autoHeight: !1,
            autoWidth: !1,
            autoResize: !0,
            autoCenter: !T,
            fitToView: !0,
            aspectRatio: !1,
            topRatio: .5,
            leftRatio: .5,
            scrolling: "auto",
            wrapCSS: "",
            arrows: !0,
            closeBtn: !0,
            closeClick: !0,
            nextClick: !1,
            mouseWheel: !0,
            autoPlay: !1,
            playSpeed: 3e3,
            preload: 3,
            modal: !1,
            loop: !0,
            ajax: {
                dataType: "html",
                headers: {
                    "X-fancyBox": !0
                }
            },
            iframe: {
                scrolling: "auto",
                preload: !0
            },
            swf: {
                wmode: "transparent",
                allowfullscreen: "true",
                allowscriptaccess: "always"
            },
            keys: {
                next: {
                    13 : "left",
                    34 : "up",
                    39 : "left",
                    40 : "up"
                },
                prev: {
                    8 : "right",
                    33 : "down",
                    37 : "right",
                    38 : "down"
                },
                close: [27],
                play: [32],
                toggle: [70]
            },
            direction: {
                next: "left",
                prev: "right"
            },
            scrollOutside: !0,
            index: 0,
            type: null,
            href: null,
            content: null,
            title: null,
            tpl: {
                wrap: '<div class="fancybox-wrap" tabIndex="-1"><div class="fancybox-skin"><div class="fancybox-outer"><div class="fancybox-inner"></div></div></div></div>',
                image: '<img class="fancybox-image" src="{href}" alt="" />',
                iframe: '<iframe id="fancybox-frame{rnd}" name="fancybox-frame{rnd}" class="fancybox-iframe" frameborder="0" vspace="0" hspace="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen' + (U ? ' allowtransparency="true"': "") + "></iframe>",
                error: '<p class="fancybox-error">The requested content cannot be loaded.<br/>Please try again later.</p>',
                closeBtn: '<a title="关闭" class="fancybox-item fancybox-close" href="javascript:;"></a>',
                next: '<a title="下一张" class="fancybox-nav fancybox-next" href="javascript:;"><span></span></a>',
                prev: '<a title="上一张" class="fancybox-nav fancybox-prev" href="javascript:;"><span></span></a>'
            },
            openEffect: "fade",
            openSpeed: 150,
            openEasing: "swing",
            openOpacity: !0,
            openMethod: "zoomIn",
            closeEffect: "fade",
            closeSpeed: 150,
            closeEasing: "swing",
            closeOpacity: !0,
            closeMethod: "zoomOut",
            nextEffect: "elastic",
            nextSpeed: 250,
            nextEasing: "swing",
            nextMethod: "changeIn",
            prevEffect: "elastic",
            prevSpeed: 250,
            prevEasing: "swing",
            prevMethod: "changeOut",
            helpers: {
                overlay: !0,
                title: !0
            },
            onCancel: d.noop,
            beforeLoad: d.noop,
            afterLoad: d.noop,
            beforeShow: d.noop,
            afterShow: d.noop,
            beforeChange: d.noop,
            beforeClose: d.noop,
            afterClose: d.noop
        },
        group: {},
        opts: {},
        previous: null,
        coming: null,
        current: null,
        isActive: !1,
        isOpen: !1,
        isOpened: !1,
        wrap: null,
        skin: null,
        outer: null,
        inner: null,
        player: {
            timer: null,
            isActive: !1
        },
        ajaxLoad: null,
        imgPreload: null,
        transitions: {},
        helpers: {},
        open: function(g, Q) {
            return g && (d.isPlainObject(Q) || (Q = {}), !1 !== b.close(!0)) ? (d.isArray(g) || (g = dD(g) ? d(g).get() : [g]), d.each(g,
            function(e, B) {
                var U, c, T, J, ed, db, aD, bh = {};
                "object" === d.type(B) && (B.nodeType && (B = d(B)), dD(B) ? (bh = {
                    href: B.data("fancybox-href") || B.attr("href"),
                    title: B.data("fancybox-title") || B.attr("title"),
                    isDom: !0,
                    element: B
                },
                d.metadata && d.extend(!0, bh, B.metadata())) : bh = B),
                U = Q.href || bh.href || (a(B) ? B: null),
                c = Q.title !== i ? Q.title: bh.title || "",
                T = Q.content || bh.content,
                J = T ? "html": Q.type || bh.type,
                !J && bh.isDom && (J = B.data("fancybox-type"), J || (ed = B.prop("class").match(/fancybox\.(\w+)/), J = ed ? ed[1] : null)),
                a(U) && (J || (b.isImage(U) ? J = "image": b.isSWF(U) ? J = "swf": "#" === U.charAt(0) ? J = "inline": a(B) && (J = "html", T = B)), "ajax" === J && (db = U.split(/\s+/, 2), U = db.shift(), aD = db.shift())),
                T || ("inline" === J ? U ? T = d(a(U) ? U.replace(/.*(?=#[^\s]+$)/, "") : U) : bh.isDom && (T = B) : "html" === J ? T = U: J || U || !bh.isDom || (J = "inline", T = B)),
                d.extend(bh, {
                    href: U,
                    type: J,
                    content: T,
                    title: c,
                    selector: aD
                }),
                g[e] = bh
            }), b.opts = d.extend(!0, {},
            b.defaults, Q), Q.keys !== i && (b.opts.keys = Q.keys ? d.extend({},
            b.defaults.keys, Q.keys) : !1), b.group = g, b._start(b.opts.index)) : void 0
        },
        cancel: function() {
            var g = b.coming;
            g && !1 !== b.trigger("onCancel") && (b.hideLoading(), b.ajaxLoad && b.ajaxLoad.abort(), b.ajaxLoad = null, b.imgPreload && (b.imgPreload.onload = b.imgPreload.onerror = null), g.wrap && g.wrap.stop(!0, !0).trigger("onReset").remove(), b.coming = null, b.current || b._afterZoomOut(g))
        },
        close: function(g) {
            b.cancel(),
            !1 !== b.trigger("beforeClose") && (b.unbindEvents(), b.isActive && (b.isOpen && g !== !0 ? (b.isOpen = b.isOpened = !1, b.isClosing = !0, d(".fancybox-item, .fancybox-nav").remove(), b.wrap.stop(!0, !0).removeClass("fancybox-opened"), b.transitions[b.current.closeMethod]()) : (d(".fancybox-wrap").stop(!0).trigger("onReset").remove(), b._afterZoomOut())))
        },
        play: function(g) {
            var Q = function() {
                clearTimeout(b.player.timer)
            },
            i = function() {
                Q(),
                b.current && b.player.isActive && (b.player.timer = setTimeout(b.next, b.current.playSpeed))
            },
            e = function() {
                Q(),
                d("body").unbind(".player"),
                b.player.isActive = !1,
                b.trigger("onPlayEnd")
            },
            B = function() {
                b.current && (b.current.loop || b.current.index < b.group.length - 1) && (b.player.isActive = !0, d("body").bind({
                    "afterShow.player onUpdate.player": i,
                    "onCancel.player beforeClose.player": e,
                    "beforeLoad.player": Q
                }), i(), b.trigger("onPlayStart"))
            };
            g === !0 || !b.player.isActive && g !== !1 ? B() : e()
        },
        next: function(g) {
            var Q = b.current;
            Q && (a(g) || (g = Q.direction.next), b.jumpto(Q.index + 1, g, "next"))
        },
        prev: function(g) {
            var Q = b.current;
            Q && (a(g) || (g = Q.direction.prev), b.jumpto(Q.index - 1, g, "prev"))
        },
        jumpto: function(g, Q, d) {
            var e = b.current;
            e && (g = db(g), b.direction = Q || e.direction[g >= e.index ? "next": "prev"], b.router = d || "jumpto", e.loop && (0 > g && (g = e.group.length + g % e.group.length), g %= e.group.length), e.group[g] !== i && (b.cancel(), b._start(g)))
        },
        reposition: function(g, Q) {
            var i, e = b.current,
            B = e ? e.wrap: null;
            B && (i = b._getPosition(Q), g && "scroll" === g.type ? (delete i.position, B.stop(!0, !0).animate(i, 200)) : (B.css(i), e.pos = d.extend({},
            e.dim, i)))
        },
        update: function(g) {
            var Q = g && g.type,
            d = !Q || "orientationchange" === Q;
            d && (clearTimeout(c), c = null),
            b.isOpen && !c && (c = setTimeout(function() {
                var i = b.current;
                i && !b.isClosing && (b.wrap.removeClass("fancybox-tmp"), (d || "load" === Q || "resize" === Q && i.autoResize) && b._setDimension(), "scroll" === Q && i.canShrink || b.reposition(g), b.trigger("onUpdate"), c = null)
            },
            d && !T ? 0 : 300))
        },
        toggle: function(g) {
            b.isOpen && (b.current.fitToView = "boolean" === d.type(g) ? g: !b.current.fitToView, T && (b.wrap.removeAttr("style").addClass("fancybox-tmp"), b.trigger("onUpdate")), b.update())
        },
        hideLoading: function() {
            B.unbind(".loading"),
            d("#fancybox-loading").remove()
        },
        showLoading: function() {
            var g, Q;
            b.hideLoading(),
            g = d('<div id="fancybox-loading"><div></div></div>').click(b.cancel).appendTo("body"),
            B.bind("keydown.loading",
            function(g) {
                27 === (g.which || g.keyCode) && (g.preventDefault(), b.cancel())
            }),
            b.defaults.fixed || (Q = b.getViewport(), g.css({
                position: "absolute",
                top: .5 * Q.h + Q.y,
                left: .5 * Q.w + Q.x
            }))
        },
        getViewport: function() {
            var Q = b.current && b.current.locked || !1,
            d = {
                x: e.scrollLeft(),
                y: e.scrollTop()
            };
            return Q ? (d.w = Q[0].clientWidth, d.h = Q[0].clientHeight) : (d.w = T && g.innerWidth ? g.innerWidth: e.width(), d.h = T && g.innerHeight ? g.innerHeight: e.height()),
            d
        },
        unbindEvents: function() {
            b.wrap && dD(b.wrap) && b.wrap.unbind(".fb"),
            B.unbind(".fb"),
            e.unbind(".fb")
        },
        bindEvents: function() {
            var g, Q = b.current;
            Q && (e.bind("orientationchange.fb" + (T ? "": " resize.fb") + (Q.autoCenter && !Q.locked ? " scroll.fb": ""), b.update), g = Q.keys, g && B.bind("keydown.fb",
            function(e) {
                var B = e.which || e.keyCode,
                U = e.target || e.srcElement;
                return 27 === B && b.coming ? !1 : (e.ctrlKey || e.altKey || e.shiftKey || e.metaKey || U && (U.type || d(U).is("[contenteditable]")) || d.each(g,
                function(g, U) {
                    return Q.group.length > 1 && U[B] !== i ? (b[g](U[B]), e.preventDefault(), !1) : d.inArray(B, U) > -1 ? (b[g](), e.preventDefault(), !1) : void 0
                }), void 0)
            }), d.fn.mousewheel && Q.mouseWheel && b.wrap.bind("mousewheel.fb",
            function(g, i, e, B) {
                for (var U = g.target || null,
                c = d(U), T = !1; c.length && !(T || c.is(".fancybox-skin") || c.is(".fancybox-wrap"));) T = ed(c[0]),
                c = d(c).parent();
                0 === i || T || b.group.length > 1 && !Q.canShrink && (B > 0 || e > 0 ? b.prev(B > 0 ? "down": "left") : (0 > B || 0 > e) && b.next(0 > B ? "up": "right"), g.preventDefault())
            }))
        },
        trigger: function(g, Q) {
            var i, e = Q || b.coming || b.current;
            if (e) {
                if (d.isFunction(e[g]) && (i = e[g].apply(e, Array.prototype.slice.call(arguments, 1))), i === !1) return ! 1;
                e.helpers && d.each(e.helpers,
                function(Q, i) {
                    i && b.helpers[Q] && d.isFunction(b.helpers[Q][g]) && (i = d.extend(!0, {},
                    b.helpers[Q].defaults, i), b.helpers[Q][g](i, e))
                }),
                d.event.trigger(g + ".fb")
            }
        },
        isImage: function(g) {
            return a(g) && g.match(/(^data:image\/.*,)|(\.(jp(e|g|eg)|gif|png|bmp|webp)((\?|#).*)?$)/i)
        },
        isSWF: function(g) {
            return a(g) && g.match(/\.(swf)((\?|#).*)?$/i)
        },
        _start: function(g) {
            var Q, i, e, B, U, c = {};
            if (g = db(g), Q = b.group[g] || null, !Q) return ! 1;
            if (c = d.extend(!0, {},
            b.opts, Q), B = c.margin, U = c.padding, "number" === d.type(B) && (c.margin = [B, B, B, B]), "number" === d.type(U) && (c.padding = [U, U, U, U]), c.modal && d.extend(!0, c, {
                closeBtn: !1,
                closeClick: !1,
                nextClick: !1,
                arrows: !1,
                mouseWheel: !1,
                keys: null,
                helpers: {
                    overlay: {
                        closeClick: !1
                    }
                }
            }), c.autoSize && (c.autoWidth = c.autoHeight = !0), "auto" === c.width && (c.autoWidth = !0), "auto" === c.height && (c.autoHeight = !0), c.group = b.group, c.index = g, b.coming = c, !1 === b.trigger("beforeLoad")) return b.coming = null,
            void 0;
            if (e = c.type, i = c.href, !e) return b.coming = null,
            b.current && b.router && "jumpto" !== b.router ? (b.current.index = g, b[b.router](b.direction)) : !1;
            if (b.isActive = !0, ("image" === e || "swf" === e) && (c.autoHeight = c.autoWidth = !1, c.scrolling = "visible"), "image" === e && (c.aspectRatio = !0), "iframe" === e && T && (c.scrolling = "scroll"), c.wrap = d(c.tpl.wrap).addClass("fancybox-" + (T ? "mobile": "desktop") + " fancybox-type-" + e + " fancybox-tmp " + c.wrapCSS).appendTo(c.parent || "body"), d.extend(c, {
                skin: d(".fancybox-skin", c.wrap),
                outer: d(".fancybox-outer", c.wrap),
                inner: d(".fancybox-inner", c.wrap)
            }), d.each(["Top", "Right", "Bottom", "Left"],
            function(g, Q) {
                c.skin.css("padding" + Q, aD(c.padding[g]))
            }), b.trigger("onReady"), "inline" === e || "html" === e) {
                if (!c.content || !c.content.length) return b._error("content")
            } else if (!i) return b._error("href");
            "image" === e ? b._loadImage() : "ajax" === e ? b._loadAjax() : "iframe" === e ? b._loadIframe() : b._afterLoad()
        },
        _error: function(g) {
            d.extend(b.coming, {
                type: "html",
                autoWidth: !0,
                autoHeight: !0,
                minWidth: 0,
                minHeight: 0,
                scrolling: "no",
                hasError: g,
                content: b.coming.tpl.error
            }),
            b._afterLoad()
        },
        _loadImage: function() {
            var g = b.imgPreload = new Image;
            g.onload = function() {
                this.onload = this.onerror = null,
                b.coming.width = this.width,
                b.coming.height = this.height,
                b._afterLoad()
            },
            g.onerror = function() {
                this.onload = this.onerror = null,
                b._error("image")
            },
            g.src = b.coming.href,
            g.complete !== !0 && b.showLoading()
        },
        _loadAjax: function() {
            var g = b.coming;
            b.showLoading(),
            b.ajaxLoad = d.ajax(d.extend({},
            g.ajax, {
                url: g.href,
                error: function(g, Q) {
                    b.coming && "abort" !== Q ? b._error("ajax", g) : b.hideLoading()
                },
                success: function(Q, d) {
                    "success" === d && (g.content = Q, b._afterLoad())
                }
            }))
        },
        _loadIframe: function() {
            var g = b.coming,
            Q = d(g.tpl.iframe.replace(/\{rnd\}/g, (new Date).getTime())).attr("scrolling", T ? "auto": g.iframe.scrolling).attr("src", g.href);
            d(g.wrap).bind("onReset",
            function() {
                try {
                    d(this).find("iframe").hide().attr("src", "//about:blank").end().empty()
                } catch(g) {}
            }),
            g.iframe.preload && (b.showLoading(), Q.one("load",
            function() {
                d(this).data("ready", 1),
                T || d(this).bind("load.fb", b.update),
                d(this).parents(".fancybox-wrap").width("100%").removeClass("fancybox-tmp").show(),
                b._afterLoad()
            })),
            g.content = Q.appendTo(g.inner),
            g.iframe.preload || b._afterLoad()
        },
        _preloadImages: function() {
            var g, Q, d = b.group,
            i = b.current,
            e = d.length,
            B = i.preload ? Math.min(i.preload, e - 1) : 0;
            for (Q = 1; B >= Q; Q += 1) g = d[(i.index + Q) % e],
            "image" === g.type && g.href && ((new Image).src = g.href)
        },
        _afterLoad: function() {
            var g, Q, i, e, B, U, c = b.coming,
            T = b.current,
            a = "fancybox-placeholder";
            if (b.hideLoading(), c && b.isActive !== !1) {
                if (!1 === b.trigger("afterLoad", c, T)) return c.wrap.stop(!0).trigger("onReset").remove(),
                b.coming = null,
                void 0;
                switch (T && (b.trigger("beforeChange", T), T.wrap.stop(!0).removeClass("fancybox-opened").find(".fancybox-item, .fancybox-nav").remove()), b.unbindEvents(), g = c, Q = c.content, i = c.type, e = c.scrolling, d.extend(b, {
                    wrap: g.wrap,
                    skin: g.skin,
                    outer: g.outer,
                    inner: g.inner,
                    current: g,
                    previous: T
                }), B = g.href, i) {
                case "inline":
                case "ajax":
                case "html":
                    g.selector ? Q = d("<div>").html(Q).find(g.selector) : dD(Q) && (Q.data(a) || Q.data(a, d('<div class="' + a + '"></div>').insertAfter(Q).hide()), Q = Q.show().detach(), g.wrap.bind("onReset",
                    function() {
                        d(this).find(Q).length && Q.hide().replaceAll(Q.data(a)).data(a, !1)
                    }));
                    break;
                case "image":
                    Q = g.tpl.image.replace("{href}", B);
                    break;
                case "swf":
                    Q = '<object id="fancybox-swf" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="100%" height="100%"><param name="movie" value="' + B + '"></param>',
                    U = "",
                    d.each(g.swf,
                    function(g, d) {
                        Q += '<param name="' + g + '" value="' + d + '"></param>',
                        U += " " + g + '="' + d + '"'
                    }),
                    Q += '<embed src="' + B + '" type="application/x-shockwave-flash" width="100%" height="100%"' + U + "></embed></object>"
                }
                dD(Q) && Q.parent().is(g.inner) || g.inner.append(Q),
                b.trigger("beforeShow"),
                g.inner.css("overflow", "yes" === e ? "scroll": "no" === e ? "hidden": e),
                b._setDimension(),
                b.reposition(),
                b.isOpen = !1,
                b.coming = null,
                b.bindEvents(),
                b.isOpened ? T.prevMethod && b.transitions[T.prevMethod]() : d(".fancybox-wrap").not(g.wrap).stop(!0).trigger("onReset").remove(),
                b.transitions[b.isOpened ? g.nextMethod: g.openMethod](),
                b._preloadImages()
            }
        },
        _setDimension: function() {
            var g, Q, i, e, B, U, c, T, dD, a, ed, bh, gG, eA, gJ, bf = b.getViewport(),
            f = 0,
            Qe = !1,
            E = !1,
            bX = b.wrap,
            fb = b.skin,
            dc = b.inner,
            ec = b.current,
            aL = ec.width,
            cb = ec.height,
            eQ = ec.minWidth,
            fR = ec.minHeight,
            fU = ec.maxWidth,
            ca = ec.maxHeight,
            eb = ec.scrolling,
            gh = ec.scrollOutside ? ec.scrollbarWidth: 0,
            bD = ec.margin,
            h = db(bD[1] + bD[3]),
            j = db(bD[0] + bD[2]);
            if (bX.add(fb).add(dc).width("auto").height("auto").removeClass("fancybox-tmp"), g = db(fb.outerWidth(!0) - fb.width()), Q = db(fb.outerHeight(!0) - fb.height()), i = h + g, e = j + Q, B = J(aL) ? (bf.w - i) * db(aL) / 100 : aL, U = J(cb) ? (bf.h - e) * db(cb) / 100 : cb, "iframe" === ec.type) {
                if (eA = ec.content, ec.autoHeight && 1 === eA.data("ready")) try {
                    eA[0].contentWindow.document.location && (dc.width(B).height(9999), gJ = eA.contents().find("body"), gh && gJ.css("overflow-x", "hidden"), U = gJ.height())
                } catch(g) {}
            } else(ec.autoWidth || ec.autoHeight) && (dc.addClass("fancybox-tmp"), ec.autoWidth || dc.width(B), ec.autoHeight || dc.height(U), ec.autoWidth && (B = dc.width()), ec.autoHeight && (U = dc.height()), dc.removeClass("fancybox-tmp"));
            if (aL = db(B), cb = db(U), dD = B / U, eQ = db(J(eQ) ? db(eQ, "w") - i: eQ), fU = db(J(fU) ? db(fU, "w") - i: fU), fR = db(J(fR) ? db(fR, "h") - e: fR), ca = db(J(ca) ? db(ca, "h") - e: ca), c = fU, T = ca, ec.fitToView && (fU = Math.min(bf.w - i, fU), ca = Math.min(bf.h - e, ca)), bh = bf.w - h, gG = bf.h - j, ec.aspectRatio ? (aL > fU && (aL = fU, cb = db(aL / dD)), cb > ca && (cb = ca, aL = db(cb * dD)), eQ > aL && (aL = eQ, cb = db(aL / dD)), fR > cb && (cb = fR, aL = db(cb * dD))) : (aL = Math.max(eQ, Math.min(aL, fU)), ec.autoHeight && "iframe" !== ec.type && (dc.width(aL), cb = dc.height()), cb = Math.max(fR, Math.min(cb, ca))), ec.fitToView) if (dc.width(aL).height(cb), bX.width(aL + g), a = bX.width(), ed = bX.height(), ec.aspectRatio) for (; (a > bh || ed > gG) && aL > eQ && cb > fR && !(f++>19);) cb = Math.max(fR, Math.min(ca, cb - 10)),
            aL = db(cb * dD),
            eQ > aL && (aL = eQ, cb = db(aL / dD)),
            aL > fU && (aL = fU, cb = db(aL / dD)),
            dc.width(aL).height(cb),
            bX.width(aL + g),
            a = bX.width(),
            ed = bX.height();
            else aL = Math.max(eQ, Math.min(aL, aL - (a - bh))),
            cb = Math.max(fR, Math.min(cb, cb - (ed - gG)));
            gh && "auto" === eb && U > cb && bh > aL + g + gh && (aL += gh),
            dc.width(aL).height(cb),
            bX.width(aL + g),
            a = bX.width(),
            ed = bX.height(),
            Qe = (a > bh || ed > gG) && aL > eQ && cb > fR,
            E = ec.aspectRatio ? c > aL && T > cb && B > aL && U > cb: (c > aL || T > cb) && (B > aL || U > cb),
            d.extend(ec, {
                dim: {
                    width: aD(a),
                    height: aD(ed)
                },
                origWidth: B,
                origHeight: U,
                canShrink: Qe,
                canExpand: E,
                wPadding: g,
                hPadding: Q,
                wrapSpace: ed - fb.outerHeight(!0),
                skinSpace: fb.height() - cb
            }),
            !eA && ec.autoHeight && cb > fR && ca > cb && !E && dc.height("auto")
        },
        _getPosition: function(g) {
            var Q = b.current,
            d = b.getViewport(),
            i = Q.margin,
            e = b.wrap.width() + i[1] + i[3],
            B = b.wrap.height() + i[0] + i[2],
            U = {
                position: "absolute",
                top: i[0],
                left: i[3]
            };
            return Q.autoCenter && Q.fixed && !g && B <= d.h && e <= d.w ? U.position = "fixed": Q.locked || (U.top += d.y, U.left += d.x),
            U.top = aD(Math.max(U.top, U.top + (d.h - B) * Q.topRatio)),
            U.left = aD(Math.max(U.left, U.left + (d.w - e) * Q.leftRatio)),
            U
        },
        _afterZoomIn: function() {
            var g = b.current;
            g && (b.isOpen = b.isOpened = !0, b.wrap.css("overflow", "visible").addClass("fancybox-opened"), b.update(), (g.closeClick || g.nextClick && b.group.length > 1) && b.inner.css("cursor", "pointer").bind("click.fb",
            function(Q) {
                d(Q.target).is("a") || d(Q.target).parent().is("a") || (Q.preventDefault(), b[g.closeClick ? "close": "next"]())
            }), g.closeBtn && d(g.tpl.closeBtn).appendTo(b.skin).bind("click.fb",
            function(g) {
                g.preventDefault(),
                b.close()
            }), g.arrows && b.group.length > 1 && ((g.loop || g.index > 0) && d(g.tpl.prev).appendTo(b.outer).bind("click.fb", b.prev), (g.loop || g.index < b.group.length - 1) && d(g.tpl.next).appendTo(b.outer).bind("click.fb", b.next)), b.trigger("afterShow"), g.loop || g.index !== g.group.length - 1 ? b.opts.autoPlay && !b.player.isActive && (b.opts.autoPlay = !1, b.play()) : b.play(!1))
        },
        _afterZoomOut: function(g) {
            g = g || b.current,
            d(".fancybox-wrap").trigger("onReset").remove(),
            d.extend(b, {
                group: {},
                opts: {},
                router: !1,
                current: null,
                isActive: !1,
                isOpened: !1,
                isOpen: !1,
                isClosing: !1,
                wrap: null,
                skin: null,
                outer: null,
                inner: null
            }),
            b.trigger("afterClose", g)
        }
    }),
    b.transitions = {
        getOrigPosition: function() {
            var g = b.current,
            Q = g.element,
            d = g.orig,
            i = {},
            e = 50,
            B = 50,
            U = g.hPadding,
            c = g.wPadding,
            T = b.getViewport();
            return ! d && g.isDom && Q.is(":visible") && (d = Q.find("img:first"), d.length || (d = Q)),
            dD(d) ? (i = d.offset(), d.is("img") && (e = d.outerWidth(), B = d.outerHeight())) : (i.top = T.y + (T.h - B) * g.topRatio, i.left = T.x + (T.w - e) * g.leftRatio),
            ("fixed" === b.wrap.css("position") || g.locked) && (i.top -= T.y, i.left -= T.x),
            i = {
                top: aD(i.top - U * g.topRatio),
                left: aD(i.left - c * g.leftRatio),
                width: aD(e + c),
                height: aD(B + U)
            }
        },
        step: function(g, Q) {
            var d, i, e, B = Q.prop,
            U = b.current,
            c = U.wrapSpace,
            T = U.skinSpace; ("width" === B || "height" === B) && (d = Q.end === Q.start ? 1 : (g - Q.start) / (Q.end - Q.start), b.isClosing && (d = 1 - d), i = "width" === B ? U.wPadding: U.hPadding, e = g - i, b.skin[B](db("width" === B ? e: e - c * d)), b.inner[B](db("width" === B ? e: e - c * d - T * d)))
        },
        zoomIn: function() {
            var g = b.current,
            Q = g.pos,
            i = g.openEffect,
            e = "elastic" === i,
            B = d.extend({
                opacity: 1
            },
            Q);
            delete B.position,
            e ? (Q = this.getOrigPosition(), g.openOpacity && (Q.opacity = .1)) : "fade" === i && (Q.opacity = .1),
            b.wrap.css(Q).animate(B, {
                duration: "none" === i ? 0 : g.openSpeed,
                easing: g.openEasing,
                step: e ? this.step: null,
                complete: b._afterZoomIn
            })
        },
        zoomOut: function() {
            var g = b.current,
            Q = g.closeEffect,
            d = "elastic" === Q,
            i = {
                opacity: .1
            };
            d && (i = this.getOrigPosition(), g.closeOpacity && (i.opacity = .1)),
            b.wrap.animate(i, {
                duration: "none" === Q ? 0 : g.closeSpeed,
                easing: g.closeEasing,
                step: d ? this.step: null,
                complete: b._afterZoomOut
            })
        },
        changeIn: function() {
            var g, Q = b.current,
            d = Q.nextEffect,
            i = Q.pos,
            e = {
                opacity: 1
            },
            B = b.direction,
            U = 200;
            i.opacity = .1,
            "elastic" === d && (g = "down" === B || "up" === B ? "top": "left", "down" === B || "right" === B ? (i[g] = aD(db(i[g]) - U), e[g] = "+=" + U + "px") : (i[g] = aD(db(i[g]) + U), e[g] = "-=" + U + "px")),
            "none" === d ? b._afterZoomIn() : b.wrap.css(i).animate(e, {
                duration: Q.nextSpeed,
                easing: Q.nextEasing,
                complete: b._afterZoomIn
            })
        },
        changeOut: function() {
            var g = b.previous,
            Q = g.prevEffect,
            i = {
                opacity: .1
            },
            e = b.direction,
            B = 200;
            "elastic" === Q && (i["down" === e || "up" === e ? "top": "left"] = ("up" === e || "left" === e ? "-": "+") + "=" + B + "px"),
            g.wrap.animate(i, {
                duration: "none" === Q ? 0 : g.prevSpeed,
                easing: g.prevEasing,
                complete: function() {
                    d(this).trigger("onReset").remove()
                }
            })
        }
    },
    b.helpers.overlay = {
        defaults: {
            closeClick: !0,
            speedOut: 200,
            showEarly: !0,
            css: {},
            locked: !T,
            fixed: !0
        },
        overlay: null,
        fixed: !1,
        create: function(g) {
            g = d.extend({},
            this.defaults, g),
            this.overlay && this.close(),
            this.overlay = d('<div class="fancybox-overlay"></div>').appendTo("body"),
            this.fixed = !1,
            g.fixed && b.defaults.fixed && (this.overlay.addClass("fancybox-overlay-fixed"), this.fixed = !1)
        },
        open: function(g) {
            var Q = this;
            g = d.extend({},
            this.defaults, g),
            this.overlay ? this.overlay.unbind(".overlay").width("auto").height("auto") : this.create(g),
            this.fixed || (e.bind("resize.overlay", d.proxy(this.update, this)), this.update()),
            g.closeClick && this.overlay.bind("click.overlay",
            function(g) {
                d(g.target).hasClass("fancybox-overlay") && (b.isActive ? b.close() : Q.close())
            }),
            this.overlay.css(g.css).show()
        },
        close: function() {
            d(".fancybox-overlay").remove(),
            e.unbind("resize.overlay"),
            this.overlay = null,
            this.margin !== !1 && (d("body").css("margin-right", this.margin), this.margin = !1),
            this.el && this.el.removeClass("fancybox-lock")
        },
        update: function() {
            var g, d = "100%";
            this.overlay.width(d).height("100%"),
            U ? (g = Math.max(Q.documentElement.offsetWidth, Q.body.offsetWidth), B.width() > g && (d = B.width())) : B.width() > e.width() && (d = B.width()),
            this.overlay.width(d).height(B.height())
        },
        onReady: function(g, i) {
            d(".fancybox-overlay").stop(!0, !0),
            this.overlay || (this.margin = B.height() > e.height() || "scroll" === d("body").css("overflow-y") ? d("body").css("margin-right") : !1, this.el = Q.all && !Q.querySelector ? d("html") : d("body"), this.create(g)),
            g.locked && this.fixed && (i.locked = this.overlay.append(i.wrap), i.fixed = !1),
            g.showEarly === !0 && this.beforeShow.apply(this, arguments)
        },
        beforeShow: function(g, Q) {
            Q.locked && (this.el.addClass("fancybox-lock"), this.margin !== !1 && d("body").css("margin-right", db(this.margin) + Q.scrollbarWidth)),
            this.open(g)
        },
        onUpdate: function() {
            this.fixed || this.update()
        },
        afterClose: function(g) {
            this.overlay && !b.isActive && this.overlay.fadeOut(g.speedOut, d.proxy(this.close, this))
        }
    },
    b.helpers.title = {
        defaults: {
            type: "inside",
            position: "bottom"
        },
        beforeShow: function(g) {
            var Q, i, e = b.current,
            B = e.title,
            c = g.type;
            if (d.isFunction(B) && (B = B.call(e.element, e)), a(B) && "" !== d.trim(B)) {
                switch (Q = d('<div class="fancybox-title fancybox-title-' + c + '-wrap">' + B + "</div>"), c) {
                case "inside":
                    i = b.skin;
                    break;
                case "outside":
                    i = b.wrap;
                    break;
                case "over":
                    i = b.inner;
                    break;
                default:
                    i = b.skin,
                    Q.appendTo("body"),
                    U && Q.width(Q.width()),
                    Q.wrapInner('<span class="child"></span>'),
                    b.current.margin[2] += Math.abs(db(Q.css("margin-bottom")))
                }
                Q["top" === g.position ? "prependTo": "appendTo"](i)
            }
        }
    },
    d.fn.fancybox = function(g) {
        var Q, i = d(this),
        e = this.selector || "",
        U = function(B) {
            var U, c, T = d(this).blur(),
            dD = Q;
            B.ctrlKey || B.altKey || B.shiftKey || B.metaKey || T.is(".fancybox-wrap") || (U = g.groupAttr || "data-fancybox-group", c = T.attr(U), c || (U = "rel", c = T.get(0)[U]), c && "" !== c && "nofollow" !== c && (T = e.length ? d(e) : i, T = T.filter("[" + U + '="' + c + '"]'), dD = T.index(this)), g.index = dD, b.open(T, g) !== !1 && B.preventDefault())
        };
        return g = g || {},
        Q = g.index || 0,
        e && g.live !== !1 ? B.undelegate(e, "click.fb-start").delegate(e + ":not('.fancybox-item, .fancybox-nav')", "click.fb-start", U) : i.unbind("click.fb-start").bind("click.fb-start", U),
        this.filter("[data-fancybox-start=1]").trigger("click"),
        this
    },
    B.ready(function() {
        d.scrollbarWidth === i && (d.scrollbarWidth = function() {
            var g = d('<div style="width:50px;height:50px;overflow:auto"><div/></div>').appendTo("body"),
            Q = g.children(),
            i = Q.innerWidth() - Q.height(99).innerWidth();
            return g.remove(),
            i
        }),
        d.support.fixedPosition === i && (d.support.fixedPosition = function() {
            var g = d('<div style="position:fixed;top:20px;"></div>').appendTo("body"),
            Q = 20 === g[0].offsetTop || 15 === g[0].offsetTop;
            return g.remove(),
            Q
        } ()),
        d.extend(b.defaults, {
            scrollbarWidth: d.scrollbarWidth(),
            fixed: d.support.fixedPosition,
            parent: d("body")
        })
    })
} (window, document, jQuery),
function(g) {
    function Q(Q) {
        var d = Q || window.event,
        i = [].slice.call(arguments, 1),
        e = 0,
        B = 0,
        b = 0,
        Q = g.event.fix(d);
        return Q.type = "mousewheel",
        d.wheelDelta && (e = d.wheelDelta / 120),
        d.detail && (e = -d.detail / 3),
        b = e,
        void 0 !== d.axis && d.axis === d.HORIZONTAL_AXIS && (b = 0, B = -1 * e),
        void 0 !== d.wheelDeltaY && (b = d.wheelDeltaY / 120),
        void 0 !== d.wheelDeltaX && (B = -1 * d.wheelDeltaX / 120),
        i.unshift(Q, e, B, b),
        (g.event.dispatch || g.event.handle).apply(this, i)
    }
    var d, i = ["DOMMouseScroll", "mousewheel"];
    if (g.event.fixHooks) for (d = i.length; d;) g.event.fixHooks[i[--d]] = g.event.mouseHooks;
    g.event.special.mousewheel = {
        setup: function() {
            if (this.addEventListener) for (var g = i.length; g;) this.addEventListener(i[--g], Q, !1);
            else this.onmousewheel = Q
        },
        teardown: function() {
            if (this.removeEventListener) for (var g = i.length; g;) this.removeEventListener(i[--g], Q, !1);
            else this.onmousewheel = null
        }
    },
    g.fn.extend({
        mousewheel: function(g) {
            return g ? this.bind("mousewheel", g) : this.trigger("mousewheel")
        },
        unmousewheel: function(g) {
            return this.unbind("mousewheel", g)
        }
    })
} (jQuery);
$(document).ready(function() {
    $(".fancybox").fancybox()
});
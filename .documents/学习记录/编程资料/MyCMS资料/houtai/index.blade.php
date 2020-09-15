<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>MyCMS 后台管理首页</title>
    <link rel="stylesheet" href="{{ url("/layui/css/layui.css") }}">
</head>
<body class="layui-layout-body">
<div class="layui-layout layui-layout-admin">
    <div class="layui-header">
        <div class="layui-logo">MyCMS 后台管理</div>
        <!-- 头部区域（可配合layui已有的水平导航） -->
        <ul class="layui-nav layui-layout-left">
            <li class="layui-nav-item"><a href="">控制台</a></li>
            <li class="layui-nav-item"><a href="">商品管理</a></li>
            <li class="layui-nav-item"><a href="">用户</a></li>
            <li class="layui-nav-item">
                <a href="javascript:;">其它系统</a>
                <dl class="layui-nav-child">
                    <dd><a href="">邮件管理</a></dd>
                    <dd><a href="">消息管理</a></dd>
                    <dd><a href="">授权管理</a></dd>
                </dl>
            </li>
        </ul>
        <ul class="layui-nav layui-layout-right">
            <li class="layui-nav-item">
                <a href="javascript:;">
                    <img src="http://t.cn/RCzsdCq" class="layui-nav-img">
                    贤心
                </a>
                <dl class="layui-nav-child">
                    <dd><a href="">基本资料</a></dd>
                    <dd><a href="">安全设置</a></dd>
                </dl>
            </li>
            <li class="layui-nav-item"><a href="">退了</a></li>
        </ul>
    </div>

    <div class="layui-side layui-bg-black">
        <div class="layui-side-scroll">
            <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
            <ul class="layui-nav layui-nav-tree" lay-shrink="all" lay-filter="test">
                <li class="layui-nav-item layui-nav-itemed">
                    <a class="" href="javascript:;">网站优化</a>
                    <dl class="layui-nav-child">
                        <dd><a href="javascript:;">首页配置</a></dd>
                        <dd><a href="javascript:;">伪静态规则</a></dd>
                        <dd><a href="javascript:;">机器人文件</a></dd>
                        <dd><a href="javascript:;">网站地图</a></dd>

                        <dd><a href="javascript:;">友情链接</a>
                            <dl class="layui-nav-child" style="margin-left: 15px;">
                                <dd><a href="javascript:;">友链列表</a></dd>
                                <dd><a href="javascript:;">新增友链</a></dd>
                            </dl>
                        </dd>

                        <dd><a href="javascript:;">标签系统</a>
                            <dl class="layui-nav-child" style="margin-left: 15px;">
                                <dd><a href="javascript:;">标签列表</a></dd>
                                <dd><a href="{{ route("manager::tag::addui") }}">新增标签</a></dd>
                            </dl>
                        </dd>

                        <dd><a href="javascript:;">内链系统</a>
                            <dl class="layui-nav-child" style="margin-left: 15px;">
                                <dd><a href="javascript:;">内链列表</a></dd>
                                <dd><a href="javascript:;">新增内链</a></dd>
                            </dl>
                        </dd>

                    </dl>
                </li>

                <li class="layui-nav-item">
                    <a href="javascript:;">栏目管理</a>
                    <dl class="layui-nav-child">
                        <dd><a href="javascript:;">栏目列表</a></dd>
                        <dd><a href="javascript:;">添加栏目</a></dd>
                    </dl>
                </li>

                <li class="layui-nav-item">
                    <a href="javascript:;">内容管理</a>
                    <dl class="layui-nav-child">
                        <dd><a href="javascript:;">内容列表</a></dd>
                        <dd><a href="javascript:;">内容添加</a></dd>
                        <dd><a href="javascript:;">待审内容</a></dd>
                    </dl>
                </li>

                <li class="layui-nav-item">
                    <a href="javascript:;">专题管理</a>
                    <dl class="layui-nav-child">
                        <dd><a href="javascript:;">专题列表</a></dd>
                        <dd><a href="javascript:;">添加专题</a></dd>
                    </dl>
                </li>

                <li class="layui-nav-item">
                    <a href="javascript:;">其它配置</a>
                    <dl class="layui-nav-child">
                        <dd><a href="javascript:;">Redis 配置</a></dd>
                        <dd><a href="javascript:;">Memcache 配置</a></dd>
                        <dd><a href="javascript:;">又拍云存储</a></dd>
                    </dl>
                </li>

            </ul>
        </div>
    </div>

    <div class="layui-body">
        <!-- 内容主体区域 -->
        <div class="layui-tab tab" lay-filter="mainTab" lay-allowclose="false" style="height: 100%;">
            <ul class="layui-tab-title">
                <li class="home"><i class="layui-icon">&#xe68e;</i>我的桌面</li>
            </ul>
            <div class="layui-tab-content" style="height: 100%;">
                <div class="layui-tab-item layui-show" style="height: 100%;">
                    <iframe src='' frameborder="0" scrolling="yes" class="x-iframe"></iframe>
                </div>
            </div>
        </div>
    </div>

    <div class="layui-footer">
        <!-- 底部固定区域 -->
        © layui.com - 底部固定区域
    </div>
</div>
<script type="text/javascript" src="{{ url("/layui/layui.js") }}"></script>

<script type="text/javascript">
    layui.use('element', function () {
        var element = layui.element;
    });
</script>

</body>
</html>

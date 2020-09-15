<?php


namespace App\Http\Controllers;

use App\Util\Tools;
use DB;
use Faker;
use Psr\SimpleCache\InvalidArgumentException;
use Str;
use Cache;
use App\Util\MakeBreadcrumb;


class TestController
{
    // 添加 category 测试数据
    public function addCategory()
    {
        $litpic_arr = [
            'https://t7.baidu.com/it/u=3616242789,1098670747&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t7.baidu.com/it/u=3204887199,3790688592&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=3363001160,1163944807&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=583874135,70653437&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=1307125826,3433407105&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=2268908537,2815455140&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t8.baidu.com/it/u=4260703909,3007700956&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t8.baidu.com/it/u=3589299979,3254072869&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t7.baidu.com/it/u=1726811931,3611243927&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=3993575087,3470587759&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=362232008,2889675535&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t7.baidu.com/it/u=4009289262,3147130468&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t7.baidu.com/it/u=3565936893,3218895147&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
            'https://t9.baidu.com/it/u=1417319747,582799067&fm=79&app=86&size=h300&n=0&g=4n&f=jpeg',
        ];
        $cates = [
            '热点资讯', '新浪新闻', '搜狐新闻', '腾讯新闻', '网易新闻', '凤凰资讯', '参考消息',
            '澎湃新闻', '厦门新闻', '社会资讯', '生活服务', '国际动态', '国内民生', '汽车新闻',
        ];
        foreach ($cates as $k => $cate) {
            /**
             * @noinspection SqlResolve
             */
            DB::insert(
                "INSERT INTO `category`(`name`,`pinyin`,`title`,`keywords`,`description`,`introduction`,`litpic`,`backpic`,`content`) VALUE (?,?,?,?,?,?,?,?,?)",
                [
                    $cate,
                    implode('', pinyin($cate, null)),
                    $cate . '标题',
                    $cate . '关键词一,' . $cate . '关键词二,' . $cate . '关键词三',
                    $cate . '最长且最优美的描述信息。',
                    $cate . '全世界写的最好的、最优秀的、最棒的、最完善的简要介绍信息。',
                    $litpic_arr[$k],
                    $litpic_arr[$k],
                    $cate . '<p>北平，1949年1月10日，农历农历腊月十二。城外炮火连天，共产党攻占北平指日可待。城内，白纸坊警察徐天和手下燕三在白纸坊辖区追捕吸毒者张帆，打斗中张帆一路窜逃到胭脂胡同找老大灯罩寻求庇护，徐天穷追不舍也跟到了胭脂胡同。同时，徐天拜把子二哥铁林，正在胭脂胡同和清吟小班班主顾小宝缠绵，结果铁林被老婆关宝慧捉个正着，楼下，徐天正和灯罩大打出手。 </p>
<p>保密局有行动，要去火车站抓捕两名来自上海的共产党，铁林第一次被允许参加行动，正好金海来找铁林，告诉铁林，徐天不想去南方，让铁林弄清楚徐天换金条的途径是否保险。燕三跑到徐天家告知小朵的噩耗，徐天等亲属赶到案发现场，徐天看着死去的贾小朵急红了眼，抱着小朵回到警署，刀美兰悲痛欲绝。徐天怀疑小朵是灯罩所杀，但徐天被提醒，灯罩昨晚一直关在牢房，而小朵的死从种种迹象看是那个被称作小红袄的连环杀手所为。</p>
<p>燕三见状，跑回去找金海搬救兵。同时，徐天闯到天桥小耳朵的斗狗场，破门而入，被小耳朵的手下暴打捉拿。徐天向小耳朵打探贾小朵的消息，小耳朵却让徐天用装了一颗子弹的左轮手枪朝自己开枪，如果四枪后徐天还没有中枪，就把打听过贾小朵的人告诉他。</p>
<p>田丹被送到金海狱中，刚刚入狱，保密局就派马天放前来向金海提走田丹。此时金海接到剿总电话，不让田丹转狱，马天放被金海打发走，田丹留在了京师监狱。燕三在保密局门口等铁林办差归来，俩人正说着话，铁林被在监狱碰了一鼻子灰的马天放叫走。田丹被狱警带向牢房，一路留心观察监狱格局，各个狱警的喜好特征，留意所关的各类罪犯，还趁乱把发卡的尖端丢给了凶煞不安的灯罩，想为日后逃走做准备。</p>'
                ]
            );
        }
        return "category 数据添加完成";
    }

    // 添加 article 测试数据
    public function addArticle()
    {
        $faker = app(Faker\Generator::class);
        for ($i = 0; $i < 5000; $i++) {
            $cate_id = random_int(1, 14);
            $title = $faker->sentence(mt_rand(1, 3));
            $keywords = join(",", $faker->words(mt_rand(3, 5)));
            $description = join(",", $faker->sentences(mt_rand(1, 2)));
            $pubdate = $faker->dateTimeBetween('-6 month', '+6 days')->getTimestamp();
            $click = random_int(1000, 10000);
            $writer = $faker->name;
            $source = $faker->name;
            $is_show = random_int(0, 1);
            $litpic = $faker->imageUrl();
            $content = join("\n\n", $faker->paragraphs(mt_rand(4, 6)));
            /**
             * @noinspection SqlResolve
             */
            DB::insert(
                "
                INSERT INTO `article`(`cate_id`,`title`,`keywords`,`description`,`pubdate`,`click`,`writer`,`source`,`is_show`,`litpic`,`content`)
                VALUE (?,?,?,?,?,?,?,?,?,?,?)",
                [$cate_id, $title, $keywords, $description, $pubdate, $click, $writer, $source, $is_show, $litpic, $content]
            );
        }
        return "article 数据添加完成";
    }

    // 添加 tag 测试数据
    public function addTag()
    {
        $faker = app(Faker\Generator::class);
        $tags = [
            "爱卡汽车", "爱卡汽车网", "宝沃汽车", "北京汽车", "标志图解", "纯电动汽车", "大众汽车", "电动汽车",
            "东风汽车", "东南汽车", "丰田汽车", "福特汽车", "福田汽车", "共享汽车", "海马汽车", "红旗汽车", "环球汽车网",
            "吉利汽车", "几何汽车", "江淮汽车", "江铃汽车", "理想汽车", "力帆汽车", "莲花汽车", "猎豹汽车", "林肯汽车",
            "铃木汽车", "领克汽车", "哪吒汽车", "奇瑞汽车", "启辰汽车", "汽车", "汽车报价", "汽车标志", "汽车大全",
            "汽车购置税", "汽车故障灯", "汽车简笔画", "汽车票", "汽车票查询", "汽车品牌", "汽车图片", "汽车网", "汽车销量",
            "汽车摇号", "汽车仪表盘", "汽车之家", "三菱汽车", "太平洋汽车", "特斯拉汽车", "威马汽车", "蔚来汽车", "沃尔沃汽车",
            "现代汽车", "小鹏汽车", "小汽车摇号", "新能源汽车", "易车网汽车", "长安汽车", "长城汽车", "众泰汽车"
        ];
        foreach ($tags as $tag) {
            $name = $tag;
            $pinyin = implode('', pinyin($tag, null));
            $title = $faker->sentence(mt_rand(3, 6));
            $keywords = join(",", $faker->words(mt_rand(3, 5)));
            $description = join(",", $faker->sentences(mt_rand(1, 2)));
            $introduction = join(",", $faker->sentences(mt_rand(1, 2)));
            $pubdate = $faker->dateTimeBetween('-6 month', '+6 days')->getTimestamp();
            $jump_url = $faker->imageUrl();
            /**
             * @noinspection SqlResolve
             */
            DB::insert(
                "
                INSERT INTO `tag`(`name`,`pinyin`,`title`,`keywords`,`description`,`introduction`,`pubdate`,`jump_url`)
                VALUE (?,?,?,?,?,?,?,?)",
                [$name, $pinyin, $title, $keywords, $description, $introduction, $pubdate, $jump_url]
            );
        }
        return "tag 数据添加完成";
    }

    // 添加 article category tag 中间表数据
    public function addArticleCategoryTag()
    {
        // 查询所有的分类ID
        /**
         * @noinspection SqlResolve
         */
        $cates = DB::select("SELECT * FROM `category`");
        $cate_ids = [];
        foreach ($cates as $cate) {
            $cate_ids[] = $cate->id;
        }

        // 查询所有的标签ID
        /**
         * @noinspection SqlResolve
         */
        $tags = DB::select("SELECT * FROM `tag`");
        $tag_ids = [];
        foreach ($tags as $tag) {
            $tag_ids[] = $tag->id;
        }

        // 查询所有的文章
        /**
         * @noinspection SqlResolve
         */
        $articles = DB::select("SELECT * FROM `article`");
        $article_ids = [];
        foreach ($articles as $article) {
            $article_ids[] = $article->id;
        }

        // 添加 article category tag 中间表数据
        /**
         * 每篇文章有 3~5 个标签
         */
        ini_set('memory_limit', '2560M'); // 临时设置内存
        set_time_limit(0); // 临时设置脚本最大执行时间为永不过期
        foreach ($article_ids as $article_id) {
            // 获取 category 的 ID
            $cate_id_key = array_rand($cate_ids, 1);
            $cate_id = $cate_ids[$cate_id_key];

            // 获取 tag 的 IDs
            $nums = random_int(2, 4);
            $temp_tags = array_rand($tag_ids, $nums);
            foreach ($temp_tags as $temp_tag) {
                $tag_id = $tag_ids[$temp_tag];
                /**
                 * @noinspection SqlResolve
                 */
                DB::insert(
                    'INSERT INTO article_tag_category (article_id, cate_id, tag_id) VALUE (?, ?, ?)',
                    [$article_id, $cate_id, $tag_id]
                );
            }
        }
        return "article category tag 中间表数据添加完成";
    }

    // 添加 user 数据

    /**
     * @noinspection SqlResolve
     */
    public function addUser()
    {
        $faker = app(Faker\Generator::class);
        for ($i = 0; $i < 100; $i++) {
            $username = $faker->name;
            $email = $faker->unique()->safeEmail;
            $email_is_verified = random_int(0, 1);
            $email_verified_at = now()->getTimestamp();
            $pwd = md5('a5s7sh4u');
            $mobile = $faker->phoneNumber;
            $fax = $faker->phoneNumber;
            $wechat = Str::random(10);
            $gender = random_int(0, 2);
            $address = $faker->address;
            $reg_date = now()->getTimestamp();
            $last_login_date = now()->getTimestamp();
            DB::insert(
                'INSERT INTO user (username, email, email_is_verified,email_verified_at,pwd,mobile,fax,wechat,gender,address,reg_date,last_login_date) VALUE (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [$username, $email, $email_is_verified, $email_verified_at, $pwd, $mobile, $fax, $wechat, $gender, $address, $reg_date, $last_login_date]
            );
        }
        return "user 数据添加完成";
    }

    // redis 使用测试
    public function testRedis()
    {
        try {
            Cache::set('name', '我使用 Redis 作为 Cache 还曾', 11000);
            Cache::set('age', 38);
            Cache::set('collage', '');
            Cache::put('collage', '大学');
            Cache::put('collage', '中学');
            Cache::put('collage', '小学');
            Cache::putMany(['collage' => ['北京', '天津', '福建'], 'age' => 18, 'name' => 'orange']);
        } catch (InvalidArgumentException $e) {
            return "发生异常现象";
        }
        return "程序正常执行完成了！！！";
    }

    /**
     * 测试面包屑导航
     */
    public function testBreadcrumb()
    {
        $cates = DB::select('select id, reid, name, pinyin from category');
        $cates = Tools::object_array_to_array($cates);
        $makeBreadcrumb = new MakeBreadcrumb('id', 'reid', 'name');
        $breadcrumbs_arr = $makeBreadcrumb->breadcrumb($cates);
        $new_breadcrumbs_arr = $makeBreadcrumb->makeBreadcrumb($breadcrumbs_arr);
        return $new_breadcrumbs_arr;
    }

    /**
     * @return string
     * 测试生成不重复的字符串
     */
    public function testNoRepeatStr()
    {
        return Tools::no_repeat_string();
    }
}

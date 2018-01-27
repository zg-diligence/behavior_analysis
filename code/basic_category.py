categories = ['电影', '电视剧', '综艺', '新闻', '体育',
              '财经', '法制',   '军事', '农业', '纪实',
              '科教', '音乐',   '戏曲', '少儿', '健康',
              '时尚', '美食',   '汽车', '旅游', '生活',  # life is in the later
              '亲子', '购物',   '电台', '其它']

classified_channels = dict([
                 ('高清点点亲子', '亲子'),
                 ('优优宝贝', '亲子'),
                 ('育婴宝典', '亲子'),
                 ('CCTV5', '体育'),
                 ('CCTV5+', '体育'),
                 ('CCTV5体育赛事', '体育'),
                 ('中央五套', '体育'),
                 ('先锋乒羽', '体育'),
                 ('劲爆体育', '体育'),
                 ('四海钓鱼', '体育'),
                 ('天元围棋', '体育'),
                 ('央视高清', '体育'),
                 ('搏击频道', '体育'),
                 ('新视觉', '体育'),
                 ('新视觉体育', '体育'),
                 ('新视觉英超', '体育'),
                 ('欧洲足球', '体育'),
                 ('武术世界', '体育'),
                 ('游戏竞技', '体育'),
                 ('游戏风云', '体育'),
                 ('网络棋牌', '体育'),
                 ('风云足球', '体育'),
                 ('高尔夫网球', '体育'),
                 ('卫生健康', '健康'),
                 ('央广健康', '健康'),
                 ('家庭健康', '健康'),
                 ('百姓健康', '健康'),
                 ('金色频道', '健康'),
                 ('内部电视台', '其它'),
                 ('南通数字电视宣传', '其它'),
                 ('城市建设', '其它'),
                 ('快乐宠物', '其它'),
                 ('摄影频道', '其它'),
                 ('数字电视导视', '其它'),
                 ('数字电视指南', '其它'),
                 ('高淳转播1', '其它'),
                 ('高淳转播2', '其它'),
                 ('国防军事', '军事'),
                 ('高清动画', '少儿'),
                 ('优漫卡通', '少儿'),
                 ('动漫秀场', '少儿'),
                 ('南京少儿', '少儿'),
                 ('卡酷卡通', '少儿'),
                 ('卡酷少儿', '少儿'),
                 ('宝贝家', '少儿'),
                 ('幼儿教育', '少儿'),
                 ('新动漫', '少儿'),
                 ('新科动漫', '少儿'),
                 ('早期教育', '少儿'),
                 ('炫动卡通', '少儿'),
                 ('金鹰卡通', '少儿'),
                 ('CCTV11', '戏曲'),
                 ('七彩戏剧', '戏曲'),
                 ('中央十一套', '戏曲'),
                 ('梨园频道', '戏曲'),
                 ('CCTV13', '新闻'),
                 ('CCTVNews', '新闻'),
                 ('CCTV新闻', '新闻'),
                 ('CCTV英语', '新闻'),
                 ('东森新闻', '新闻'),
                 ('中天新闻', '新闻'),
                 ('中央十三套', '新闻'),
                 ('中央新闻', '新闻'),
                 ('凤凰资讯', '新闻'),
                 ('江宁新闻', '新闻'),
                 ('镇江新闻', '新闻'),
                 ('雨花新闻', '新闻'),
                 ('旅游897', '旅游'),
                 ('时代出行', '旅游'),
                 ('环球旅游', '旅游'),
                 ('女性时尚', '时尚'),
                 ('江苏靓妆', '时尚'),
                 ('靓妆频道', '时尚'),
                 ('极速汽车', '汽车'),
                 ('汽摩', '汽车'),
                 ('车迷频道', '汽车'),
                 ('CCTV12', '法制'),
                 ('中央十二套', '法制'),
                 ('法治天地', '法制'),
                 ('中国气象', '生活'),
                 ('家政频道', '生活'),
                 ('导视频道', '生活'),
                 ('时代家居', '生活'),
                 ('茶频道', '生活'),
                 ('CCTV6', '电影'),
                 ('CHC动作电影', '电影'),
                 ('CHC家庭影院', '电影'),
                 ('CHC电影', '电影'),
                 ('CHC高清电影', '电影'),
                 ('DOX映画', '电影'),
                 ('DOX院线', '电影'),
                 ('高清电影', '电影'),
                 ('中央六套', '电影'),
                 ('动作影院', '电影'),
                 ('大众影院', '电影'),
                 ('家庭影院', '电影'),
                 ('沙发院线', '电影'),
                 ('CCTV8', '电视剧'),
                 ('DOXTV音像世界', '电视剧'),
                 ('DOX剧场', '电视剧'),
                 ('DOX怡家', '电视剧'),
                 ('DOX新知', '电视剧'),
                 ('DOX英伦', '电视剧'),
                 ('DOX韩流', '电视剧'),
                 ('高清电视剧', '电视剧'),
                 ('中央八套', '电视剧'),
                 ('央视怀旧剧场', '电视剧'),
                 ('怀旧剧场', '电视剧'),
                 ('新视觉剧场', '电视剧'),
                 ('欢笑剧场', '电视剧'),
                 ('第一剧场', '电视剧'),
                 ('都市剧场', '电视剧'),
                 ('风云剧场', '电视剧'),
                 ('CCTV10', '科教'),
                 ('世界地理', '科教'),
                 ('中央十套', '科教'),
                 ('中学生频道', '科教'),
                 ('书画频道', '科教'),
                 ('南通党建引导', '科教'),
                 ('国学频道', '科教'),
                 ('招考频道', '科教'),
                 ('收藏天下', '科教'),
                 ('江苏党校一套', '科教'),
                 ('江苏党校三套', '科教'),
                 ('江苏党校二套', '科教'),
                 ('江苏招考', '科教'),
                 ('环球奇观', '科教'),
                 ('留学世界', '科教'),
                 ('考试在线', '科教'),
                 ('职业指南', '科教'),
                 ('英语辅导', '科教'),
                 ('读书频道', '科教'),
                 ('CCTV9', '纪实'),
                 ('高清纪实', '纪实'),
                 ('上海纪实', '纪实'),
                 ('上视纪实', '纪实'),
                 ('中央九套', '纪实'),
                 ('人物频道', '纪实'),
                 ('先锋纪录', '纪实'),
                 ('全纪实', '纪实'),
                 ('华数求索', '纪实'),
                 ('发现之旅', '纪实'),
                 ('探索发现', '纪实'),
                 ('新视觉纪实', '纪实'),
                 ('求索纪实', '纪实'),
                 ('求索纪录', '纪实'),
                 ('纪实频道', '纪实'),
                 ('老故事', '纪实'),
                 ('金鹰纪实', '纪实'),
                 ('时代风尚', '综艺'),
                 ('中华美食', '美食'),
                 ('时代美食', '美食'),
                 ('CCTV2', '财经'),
                 ('东方财经', '财经'),
                 ('中央二套', '财经'),
                 ('家庭理财', '财经'),
                 ('幸福彩', '财经'),
                 ('彩民在线', '财经'),
                 ('江苏体彩', '财经'),
                 ('江苏彩票', '财经'),
                 ('江苏财经', '财经'),
                 ('第一财经', '财经'),
                 ('证券资讯', '财经'),
                 ('财富天下', '财经'),
                 ('财经频道', '财经'),
                 ('南京信息', '购物'),
                 ('CCTV15', '音乐'),
                 ('CCTV音乐', '音乐'),
                 ('中央十五套', '音乐'),
                 ('中央音乐', '音乐'),
                 ('南京六合音乐', '音乐'),
                 ('句容互动点歌', '音乐'),
                 ('新视觉娱乐', '音乐'),
                 ('江苏经典流行音乐', '音乐'),
                 ('江苏音乐', '音乐'),
                 ('风云音乐', '音乐'),
                 ('魅力音乐', '音乐')])

sports_keywords = \
    '赛事|联赛|锦标赛|巡回赛|挑战赛|小组赛|公开赛|男单|女单|' \
    '奥运会|世锦赛|世界杯|欧洲杯|亚洲杯|足协杯|汤姆斯杯|' \
    '澳网|法网|温网|美网|篮球|足球|NBA|CBA|英超|中超|中甲|意甲|德甲|欧冠|亚冠|' \
    '游泳|田径|斯诺克|羽毛球|乒乓球|网球|排球|台球|棒球|垒球|冰球|'\
    '高尔夫|保龄球|板球|藤球|壁球|手球|曲棍球|橄榄球|围棋|象棋|' \
    '柔道|拳击|跆拳道|空手道|射箭|皮划艇|自行车|马术|击剑|体操|蹦床|' \
    '赛艇|帆船|射击|举重|摔跤|体育舞蹈|现代五项|铁人三项|武术|轮滑|卡巴迪|龙舟'

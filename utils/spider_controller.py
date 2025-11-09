# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
from tqdm import tqdm

from function.search import Search
from function.detail import Detail
from function.review import Review
from function.get_encryption_requests import *
from utils.saver.saver import saver
from utils.spider_config import spider_config


class Controller():
    """
    整个程序的控制器
    用来进行爬取策略选择以及数据汇总存储
    """

    def __init__(self):
        self.s = Search()
        self.d = Detail()
        self.r = Review()
        self.cityMap={
            1: '上海', 2: '北京', 10: '天津', 18: '沈阳', 19: '大连', 21: '青岛', 22: '济南', 23: '海口', 
            24: '石家庄', 25: '唐山', 26: '秦皇岛', 27: '邯郸', 28: '邢台', 29: '保定', 30: '张家口', 
            31: '承德', 32: '沧州', 33: '廊坊', 34: '衡水', 35: '太原', 36: '大同', 37: '阳泉', 38: '长治', 
            39: '晋城', 40: '朔州', 41: '晋中', 42: '运城', 43: '忻州', 44: '临汾', 45: '吕梁', 46: '呼和浩特', 
            47: '包头', 48: '乌海', 49: '赤峰', 50: '通辽', 51: '鄂尔多斯', 52: '呼伦贝尔', 53: '兴安盟', 
            54: '锡林郭勒', 55: '乌兰察布', 56: '巴彦淖尔', 57: '阿拉善', 58: '鞍山', 59: '抚顺', 60: '本溪', 
            61: '丹东', 62: '锦州', 63: '营口', 64: '阜新', 65: '辽阳', 66: '盘锦', 67: '铁岭', 68: '朝阳', 
            69: '葫芦岛', 70: '长春', 71: '吉林', 72: '四平', 73: '辽源', 74: '通化', 75: '白山', 76: '松原', 
            77: '白城', 78: '延边', 79: '哈尔滨', 80: '齐齐哈尔', 81: '鸡西', 82: '鹤岗', 83: '双鸭山', 
            84: '大庆', 85: '伊春', 86: '佳木斯', 87: '七台河', 88: '牡丹江', 89: '黑河', 90: '绥化', 
            91: '大兴安岭', 92: '徐州', 93: '常州', 94: '南通', 95: '连云港', 96: '淮安', 97: '盐城', 
            98: '镇江', 99: '泰州', 100: '宿迁', 101: '温州', 102: '嘉兴', 103: '湖州', 104: '绍兴', 
            105: '金华', 106: '衢州', 107: '舟山', 108: '台州', 109: '丽水', 110: '合肥', 111: '芜湖', 
            112: '蚌埠', 113: '淮南', 114: '马鞍山', 115: '淮北', 116: '铜陵', 117: '安庆', 118: '黄山', 
            119: '滁州', 120: '阜阳', 121: '宿州', 123: '六安', 124: '亳州', 125: '池州', 126: '宣城', 
            127: '莆田', 128: '三明', 129: '泉州', 130: '漳州', 131: '南平', 132: '龙岩', 133: '宁德', 
            134: '南昌', 135: '景德镇', 136: '萍乡', 137: '九江', 138: '新余', 139: '鹰潭', 140: '赣州', 
            141: '吉安', 142: '宜春', 143: '抚州', 144: '上饶', 145: '淄博', 146: '枣庄', 147: '东营', 
            148: '烟台', 149: '潍坊', 150: '济宁', 151: '泰安', 152: '威海', 153: '日照', 155: '临沂', 
            156: '德州', 157: '聊城', 158: '滨州', 159: '菏泽', 160: '郑州', 161: '开封', 162: '洛阳', 
            163: '平顶山', 164: '安阳', 165: '鹤壁', 166: '新乡', 167: '焦作', 168: '濮阳', 169: '许昌', 
            170: '漯河', 171: '三门峡', 172: '南阳', 173: '商丘', 174: '信阳', 175: '周口', 176: '驻马店', 
            177: '黄石', 178: '十堰', 179: '宜昌', 180: '襄阳', 181: '鄂州', 182: '荆门', 183: '孝感', 
            184: '荆州', 185: '黄冈', 186: '咸宁', 187: '随州', 188: '恩施', 189: '仙桃', 190: '潜江', 
            191: '天门', 192: '株洲', 193: '湘潭', 194: '衡阳', 195: '邵阳', 196: '岳阳', 197: '常德', 
            198: '张家界', 199: '益阳', 200: '郴州', 201: '永州', 202: '怀化', 203: '娄底', 204: '湘西', 
            205: '韶关', 206: '珠海', 207: '汕头', 208: '佛山', 209: '江门', 210: '湛江', 211: '茂名', 
            212: '肇庆', 213: '惠州', 214: '梅州', 215: '汕尾', 216: '河源', 217: '阳江', 218: '清远', 
            219: '东莞', 220: '中山', 221: '潮州', 222: '揭阳', 223: '云浮', 224: '南宁', 225: '柳州', 
            226: '桂林', 227: '梧州', 228: '北海', 229: '防城港', 230: '钦州', 231: '贵港', 232: '玉林', 
            233: '百色', 234: '贺州', 235: '河池', 238: '自贡', 239: '攀枝花', 240: '泸州', 241: '德阳', 
            242: '绵阳', 243: '广元', 244: '遂宁', 245: '内江', 246: '乐山', 247: '南充', 248: '眉山', 
            249: '宜宾', 250: '广安', 251: '达州', 252: '雅安', 253: '巴中', 254: '资阳', 255: '阿坝', 
            256: '甘孜州', 257: '凉山', 258: '贵阳', 259: '六盘水', 260: '遵义', 261: '安顺', 262: '铜仁', 
            263: '黔西南', 264: '毕节市', 265: '黔东南', 266: '黔南', 267: '昆明', 268: '曲靖', 269: '玉溪', 
            270: '保山', 271: '昭通', 272: '楚雄州', 273: '红河', 274: '文山州', 275: '普洱', 276: '西双版纳', 
            277: '大理州', 278: '德宏', 279: '丽江', 280: '怒江', 281: '迪庆', 282: '临沧', 283: '拉萨', 
            284: '昌都市', 285: '山南', 286: '日喀则', 287: '那曲', 288: '阿里', 289: '林芝市', 290: '铜川', 
            291: '宝鸡', 292: '咸阳', 293: '渭南', 294: '延安', 295: '汉中', 296: '榆林', 297: '安康', 
            298: '商洛', 299: '兰州', 300: '嘉峪关', 301: '金昌', 302: '白银', 303: '天水', 304: '武威', 
            305: '张掖', 306: '平凉', 307: '酒泉', 308: '庆阳', 309: '定西', 310: '陇南', 311: '临夏州', 
            312: '甘南', 313: '西宁', 314: '海东', 315: '海北', 316: '黄南', 318: '果洛', 319: '玉树', 
            320: '海西', 321: '银川', 322: '石嘴山', 323: '吴忠', 324: '固原', 325: '乌鲁木齐', 326: '克拉玛依', 
            327: '吐鲁番市', 329: '昌吉州', 330: '博尔塔拉', 331: '巴音郭楞', 332: '阿克苏地区', 333: '克孜勒苏', 
            334: '喀什地区', 335: '和田地区', 336: '伊犁', 337: '塔城地区', 338: '阿勒泰地区', 339: '石河子', 
            340: '台湾', 341: '香港', 342: '澳门', 344: '长沙', 345: '三亚', 346: '北屯', 351: '中卫', 
            358: '儋州', 389: '阿拉尔', 390: '白沙', 391: '保亭', 392: '昌江', 393: '澄迈县', 394: '崇左', 
            395: '定安县', 396: '东方', 397: '济源', 398: '来宾', 399: '乐东', 400: '临高县', 401: '陵水', 
            402: '琼海', 403: '琼中', 404: '神农架林区', 405: '图木舒克', 406: '屯昌县', 407: '万宁', 
            408: '文昌', 409: '五家渠', 410: '五指山', 411: '海南州', 2233: '哈密市', 2310: '三沙', 
            4472: '铁门关市', 4488: '双河市', 4489: '昆玉市', 4490: '可克达拉市', 4493: '胡杨河市'
        }

        # 初始化基础URL
        if spider_config.SEARCH_URL == '':
            keyword = spider_config.KEYWORD
            channel_id = spider_config.CHANNEL_ID
            city_id = spider_config.LOCATION_ID
            self.base_url = 'http://www.dianping.com/search/keyword/' + str(city_id) + '/' + str(
                channel_id) + '_' + str(keyword) + '/p'
            print(f"基础搜索URL为：{self.base_url}")
            pass
        else:
            # 末尾加一个任意字符，为了适配两种初始化url切割长度
            self.base_url = spider_config.SEARCH_URL + '1'

    def main(self):
        """
        调度
        @return:
        """
        # Todo  其实这里挺犹豫是爬取完搜索直接详情还是爬一段详情一段
        #       本着稀释同类型访问频率的原则，暂时采用爬一段详情一段
        # 调用搜索
        for page in tqdm(range(1, spider_config.NEED_SEARCH_PAGES + 1), desc='搜索页数'):
            # 拼凑url
            search_url, request_type = self.get_search_url(page)
            """
            {
                '店铺id': -,
                '店铺名': -,
                '评论总数': -,
                '人均价格': -,
                '标签1': -,
                '标签2': -,
                '店铺地址': -,
                '详情链接': -,
                '图片链接': -,
                '店铺均分': -,
                '推荐菜': -,
                '店铺总分': -,
                '店铺分类': -,
                '城市ID': -,
                '城市名称': -,
            }
            """
            search_res = self.s.search(search_url, request_type)
            # search方法如果返回None，代表页面已经没有数据了
            if not search_res:
                break

            if spider_config.NEED_DETAIL is False and spider_config.NEED_REVIEW is False:
                for each_search_res in search_res:
                    each_search_res.update({
                        '店铺电话': '-',
                        '其他信息': '-',
                        '优惠券信息': '-',
                    })
                    self.saver(each_search_res, {})
                continue
            for each_search_res in tqdm(search_res, desc='详细爬取'):
                each_detail_res = {}
                each_review_res = {}
                # 爬取详情
                if spider_config.NEED_DETAIL:
                    shop_id = each_search_res['店铺id']
                    if spider_config.NEED_PHONE_DETAIL:
                        """
                        {
                            '店铺id': -,
                            '店铺名': -,
                            '评论总数': -,
                            '人均价格': -,
                            '店铺地址': -,
                            '店铺电话': -,
                            '其他信息': -
                        }
                        """
                        each_detail_res = self.d.get_detail(shop_id)
                        # 多版本爬取格式适配
                        each_detail_res.update({
                            '店铺总分': '-',
                            '店铺均分': '-',
                            '优惠券信息': '-',
                        })
                    else:
                        """
                        {
                            '店铺id': -,
                            '店铺名': -,
                            '店铺地址': -,
                            '店铺电话': -,
                            '店铺总分': -,
                            '店铺均分': -,
                            '人均价格': -,
                            '评论总数': -,
                        }
                        """
                        hidden_info = get_basic_hidden_info(shop_id)
                        review_and_star = get_review_and_star(shop_id)
                        each_detail_res.update(hidden_info)
                        each_detail_res.update(review_and_star)
                        # 多版本爬取格式适配
                        each_detail_res.update({
                            '其他信息': '-',
                            '优惠券信息': '-'
                        })
                    # 爬取经纬度
                    if spider_config.NEED_LOCATION:
                        """
                        {
                            '店铺id': -,
                            '店铺名': -,
                            '店铺纬度': -,
                            '店铺经度': -,
                        }
                        """
                        shop_id = each_search_res['店铺id']
                        lat_and_lng = get_lat_and_lng(shop_id)
                        each_detail_res.update(lat_and_lng)
                    else:
                        each_detail_res.update({
                            '店铺纬度': '-',
                            '店铺经度': '-'
                        })
                    # 全局整合，将详情以及评论的相关信息拼接到search_res中。
                    each_search_res['店铺地址'] = each_detail_res['店铺地址']
                    each_search_res['店铺电话'] = each_detail_res['店铺电话']
                    each_search_res['店铺总分'] = each_detail_res['店铺总分']
                    if each_search_res['店铺均分'] == '-':
                        each_search_res['店铺均分'] = each_detail_res['店铺均分']
                    each_search_res['人均价格'] = each_detail_res['人均价格']
                    each_search_res['评论总数'] = each_detail_res['评论总数']
                    each_search_res['其他信息'] = each_detail_res['其他信息']
                    each_search_res['优惠券信息'] = each_detail_res['优惠券信息']
                    each_search_res['店铺纬度'] = each_detail_res['店铺纬度']
                    each_search_res['店铺经度'] = each_detail_res['店铺经度']
                    each_search_res['店铺分类'] = str(spider_config.KEYWORD)
                    each_search_res['城市ID'] = spider_config.LOCATION_ID
                    each_search_res['城市名称'] = self.cityMap.get(int(spider_config.LOCATION_ID), '-')
                # 爬取评论
                if spider_config.NEED_REVIEW:
                    shop_id = each_search_res['店铺id']
                    if spider_config.NEED_REVIEW_DETAIL:
                        """
                        {
                            '店铺id': -,
                            '评论摘要': -,
                            '评论总数': -,
                            '好评个数': -,
                            '中评个数': -,
                            '差评个数': -,
                            '带图评论个数': -,
                            '精选评论': -,
                        }
                        """
                        each_review_res = self.r.get_review(shop_id)
                        each_review_res.update({'推荐菜': '-'})
                    else:
                        """
                        {
                            '店铺id': -,
                            '评论摘要': -,
                            '评论总数': -,
                            '好评个数': -,
                            '中评个数': -,
                            '差评个数': -,
                            '带图评论个数': -,
                            '精选评论': -,
                            '推荐菜': -,
                        }
                        """
                        each_review_res = get_basic_review(shop_id)

                        # 全局整合，将详情以及评论的相关信息拼接到search_res中。
                        each_search_res['推荐菜'] = each_review_res['推荐菜']
                        # 对于已经给到search_res中的信息，删除
                        each_review_res.pop('推荐菜')


                self.saver(each_search_res, each_review_res)
            # 如果这一页数据小于15，代表下一页已经没有数据了，直接退出
            if len(search_res) < 15:
                break

    def get_review(self, shop_id, detail=False):
        if detail:
            each_review_res = self.r.get_review(shop_id)
        else:
            each_review_res = get_basic_review(shop_id)
        saver.save_data(each_review_res, 'review')

    def get_detail(self, shop_id, detail=False):
        each_detail_res = {}
        if detail:
            """
            '店铺id': -,
            '店铺名': -,
            '评论总数': -,
            '人均价格': -,
            '店铺地址': -,
            '店铺电话': -,
            '其他信息': -,
            '店铺总分': '-',
            '店铺均分': '-',
            """
            each_detail_res = self.d.get_detail(shop_id)
            # 多版本爬取格式适配
            each_detail_res.update({
                '店铺总分': '-',
                '店铺均分': '-',
            })
        else:
            """
            '店铺id': -,
            '店铺总分': -,
            '店铺均分': -,
            '人均价格': -,
            '评论总数': -,
            '店铺名': -,
            '店铺地址': -,
            '店铺电话': -，
            '其他信息': -,
            """
            hidden_info = get_basic_hidden_info(shop_id)
            review_and_star = get_review_and_star(shop_id)
            each_detail_res.update(hidden_info)
            each_detail_res.update(review_and_star)
            # 多版本爬取格式适配
            each_detail_res.update({
                '其他信息': '-'
            })
        # 获取经纬度
        if spider_config.NEED_LAT_AND_LNG:
            lat_and_lng = get_lat_and_lng(shop_id)
            each_detail_res.update(lat_and_lng)
        saver.save_data(each_detail_res, 'detail')

    def get_search_url(self, cur_page):
        """
        获取搜索链接
        @param cur_page:
        @return:
        """
        if cur_page == 1:
            # return self.base_url[:-2], 'no proxy, no cookie'
            return self.base_url[:-2], 'proxy, cookie'
        else:
            if self.base_url.endswith('p'):
                return self.base_url + str(cur_page), 'proxy, cookie'
            else:
                return self.base_url[:-1] + str(cur_page), 'proxy, cookie'

    def saver(self, each_search_res, each_review_res):
        # save search
        saver.save_data(each_search_res, 'search')
        # save detail
        # if spider_config.NEED_DETAIL:
        #     saver.save_data(each_detail_res, 'detail')

        # save review
        if spider_config.NEED_REVIEW:
            saver.save_data(each_review_res, 'review')


controller = Controller()

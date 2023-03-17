# 用来格式化时间的模块
from datetime import datetime
# 用来通过正则表达式来提取起批量的模块
import re
# 用来传递 item 对象
from graduationProject.items import GraduationprojectItem

class SaveProduct:

    # 到这里，已经是开始存储数据库了，这里爬取第一页至第二十页
    def saveProduct(self,response):
        # 获得第三分类的名字
        third_level_name = response.meta['third_level_name']

        # 全部加 if ，是因为有个别的数据是一个空数组，而此时加 [0]，会导致报数组越界的异常，如果是空数组，则在 else 中进行置空
        # 商品名称
        name=response.xpath('//div[@class="c-ctn"]//div[@class="supply-price-show"]//div[@class="d-t"]/text()').extract()
        if name:
            name=name[0]
        # 商品价格
        price=response.xpath('//div[@class="c-ctn"]//div[@class="supply-price-show"]//div[@class="active-p"]/text()').extract()
        if price:
            price=price[0]
            # 将价格变为 double 类型，xx.xx元或xx.xx-xx.xx元 --> xx.xx
            price=float(price.split('-')[0].split('元')[0])
        # 起批量
        start_batching=response.xpath('//div[@class="c-ctn"]//div[@class="supply-price-show"]//div[@class="line-val"]/text()').extract()
        if start_batching:
            start_batching=start_batching[0]
            # 将起批量变为 int 类型，xx箱起批 --> xx
            start_batching=int(re.findall('\d+',start_batching)[0])
        # 更新时间
        update_time=response.xpath('//div[@class="c-ctn"]//div[@class="supply-price-show"]//div[@class="r-t"]/text()').extract()
        if update_time:
            update_time=update_time[0]
            # 格式化时间，有时分秒的 datetime 格式，更新时间：2023年 03月11日 --> 2023-03-11 00:00:00
            # 数据库不支持这种插入方式，因此需要改变 2023-03-11 00:00:00 --> 20230211
            # update_time=update_time[5:9]+'/'+update_time[11:13]+'/'+update_time[14:16]
            # update_time=datetime.strptime(update_time, '%Y/%m/%d')
            update_time=update_time[5:9]+update_time[11:13]+update_time[14:16]
        # 发货地址
        ship_from_address=response.xpath('//div[@class="c-ctn"]//div[@class="con-bg"]/div[@class="batch-num mar flex-c"][1]//div[@class="line-val"]/text()').extract()
        if ship_from_address:
            ship_from_address=ship_from_address[0]
            # 改发货地址的格式，由吉林省长春市二道区 --> 吉林，依靠前两个字符来确定是哪个省，如果精确到区级，会导致数量太多
            ship_from_address=ship_from_address[0:2]
        # 采购热度
        purchasing_heat=response.xpath('//div[@class="c-ctn"]//div[@class="con-bg"]/div[@class="batch-num mar flex-c"]//div[@class="line-val flex-center"]//img').extract()
        # 根据数组求长度，即为火花的个数
        purchasing_heat=len(purchasing_heat)
        # 询价人数
        inquiry=response.xpath('//div[@class="c-ctn"]//div[@class="con-bg"]/div[@class="batch-num mar flex-c"]//div[@class="line-val"][1]//span/text()').extract()
        if inquiry:
            inquiry=inquiry[0]
            # 此时的询价人数，前后有空格，需要去空格
            inquiry = inquiry.strip()
            # 字符串类型转为 int 类型，6 --> 6
            inquiry=int(inquiry)
        # 成交人数
        traded=response.xpath('//div[@class="c-ctn"]//div[@class="con-bg"]/div[@class="batch-num mar flex-c"]//div[@class="line-val"][2]//span/text()').extract()
        if traded:
            traded=traded[0]
            # 字符串类型转为 int 类型，6 --> 6
            traded=int(traded)
        # 评价人数
        assess=response.xpath('//div[@class="c-ctn"]//div[@class="con-bg"]/div[@class="batch-num mar flex-c"]//div[@class="line-val"][3]//span/text()').extract()
        if assess:
            assess=assess[0]
            # 字符串类型转为 int 类型，6 --> 6
            assess=int(assess)
        # 描述
        desc=response.xpath('//div[@class="com-bg"]//div[@class="detail-desc"]/text()').extract()
        if desc:
            desc=desc[0]
        else:
            desc = response.xpath('//div[@class="con-bg"]//div[@class="supply-price-show"]//div[@class="d-t"]/text()').extract()
            if desc:
                desc=desc[0]
            else:
                desc=None
        # 商铺链接
        shop_url=response.xpath('//div[@class="shop-com"]//a/@href').extract()
        if shop_url:
            shop_url=shop_url[0]

        product=GraduationprojectItem(third_level_name=third_level_name,name=name,
                                      price=price,start_batching=start_batching,
                                      update_time=update_time,ship_from_address=ship_from_address,
                                      purchasing_heat=purchasing_heat,inquiry=inquiry,
                                      traded=traded,assess=assess,desc=desc,shop_url=shop_url)
        yield product

        # print('商品名称')
        # print(name)
        # print('商品价格')
        # print(price)
        # print('起批量')
        # print(start_batching)
        # print('更新时间')
        # print(update_time)
        # print('发货地址')
        # print(ship_from_address)
        # print('采购热度')
        # print(purchasing_heat)
        # print('询价人数')
        # print(inquiry)
        # print('成交人数')
        # print(traded)
        # print('评价人数')
        # print(assess)
        # print('描述')
        # print(desc)
        # print('商铺链接')
        # print(show_url)
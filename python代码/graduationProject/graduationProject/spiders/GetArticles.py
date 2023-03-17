import time
from functools import partial

import scrapy
# 导入管道
from graduationProject.items import GraduationprojectItem
# 导入请求商品列表的函数
from graduationProject.spiders.crawling.GetProductList import getProductList


class GetarticlesSpider(scrapy.Spider):
    name = 'GetArticles'
    allowed_domains = ['cnhnb.com']
    # 起始地址
    start_urls = ['https://www.cnhnb.com/supply/']


    def parse(self, response):

        # 第一级分类和第二级分类的数据较少，因此可直接创建数据库表
        # 第三级分类，也直接建立表，但是查询的时候需要连带第三级的值传入管道，因为需要将商品表与第三极表联系起来
        # 获得页面的所有分类，包括了第二级分类和第三级分类
        all_classifications=response.xpath('//div[@class="cate-cons"]//div[@class="c-c-l"]//div[@class="cate-block"]')
        # 此处的 secondLevel 对应第二级分类，每个循环的当前项包含了第三级分类的数据

# 此处
        for secondLevel in range(0,len(all_classifications)):
            # 获取第三级分类的名字，因为所有商品需要与此分类的名字绑定（该属性在数据库中唯一），此时一个 secondLevel 相当于
            #   第二级分类的一个值，其中包含了大量的第三级分类的数据，此时需要循环
            third_level_names=all_classifications[secondLevel].xpath('./div[@class="cate-block-list"]//a')
            print(third_level_names.extract())
            for third_level in third_level_names:

                # 此时的 thirdLevelName 即为第三级分类的值
                third_level_name=third_level.xpath('./text()').extract()[0]
                # 获取需要跳转的连接，根据第三级分类的值来进行归类
                overview_url=third_level.xpath('./@href').extract()[0]
                overview_url="https://www.cnhnb.com"+overview_url


                # 将 getProductList 函数冻结，使他可以接收到从此传递过去的 response 对象
                # callback = partial(getProductList.getProductList, response=response)
                # 创建一个对象，使这个回调函数能够接收新的 response 对象，使用冻结的会导致 response 对象是旧的
                get_product_list = getProductList()
                # 通过第三级分类表的数据以及所要跳转的链接，开始请求商品总列表
                # yield scrapy.Request(url=overviewUrl, callback=callback,meta={'thirdLevelName':thirdLevelName})
                # time.sleep(0.2)
                yield scrapy.Request(url=overview_url, callback=get_product_list.getProductList,meta={'third_level_name': third_level_name}, dont_filter=True)
#此处




        # for secondLevel in allClassifications:
        #     # 获取第三级分类的名字，因为所有商品需要与此分类的名字绑定（该属性在数据库中唯一），此时一个 secondLevel 相当于
        #     #   第二级分类的一个值，其中包含了大量的第三级分类的数据，此时需要循环
        #     thirdLevelNames=secondLevel.xpath('./div[@class="cate-block-list"]//a')
        #     for thirdLevel in thirdLevelNames:
        #         print(thirdLevel.xpath('./@href'))
        #         print(thirdLevel.xpath('./text()'))
        #         # 此时的 thirdLevelName 即为第三级分类的值
        #         thirdLevelName=thirdLevel.xpath('./text()')[0].extract()
        #         # 获取需要跳转的连接，根据第三级分类的值来进行归类
        #         overviewUrl=thirdLevel.xpath('./@href')[0].extract()
        #         overviewUrl="https://www.cnhnb.com"+overviewUrl
        #
        #         # 通过第三级分类表的数据以及所要跳转的链接，开始请求商品总列表
        #         yield scrapy.Request(url=overviewUrl,callback=getProductList,meta={'thirdLevelName':thirdLevelName})
            pass




































    # https://www.cnhnb.com/p/jiuhuang/ 例如此链接
    # 此时已经到了商品总列表，暂定义，如果页数大于 20 页的，则只爬取 20 页，低于 20 页的，则爬取全部
    def getProductList(self, response):
        # 获取整个商品列表的页数，通过页数的大小来决定调用哪个函数，此处获取分页的最后一个按钮，根据其中的数字来判断
        last_item = response.xpath('//div[@class="l-bg"]//div[@class="pagination-bg"]//a[last()]/text()').extract()[0]
        thirdLevelName=response.meta['thirdLevelName']

        # 判断，此时需要进行强转，不然会报错
        if int(last_item) <= 20:
            # productListLessThan20 = ProductListLessThan20()
            # productListLessThan20.getProductLess(response)
            yield scrapy.Request(url=response.url,callback=self.getProductMoreThan20)
        else:
            # productListMoreThan20 = ProductListMoreThan20(response.url[:-1])
            # productListMoreThan20.getProductMore(response)
            page=1
            # print(type(response.url))
            url=response.url
            url=url[:-1]+'-0-0-0-0-2'
            self.getProductLessThan20(response)
            yield scrapy.Request(url=url,callback=self.getProductMoreThan20)
        pass


    def getProductMoreThan20(self,response):
        print('进来了')
        # 定义基准链接
        base_url = response.url
        # 因为此时的基准链接最后有个 / ，因此不能直接拼接，需要先去除最后一个 / ，然后再与 -0-0-0-0- 进行拼接
        base_url=base_url[:-1]+'-0-0-0-0-'
        for page in range(2,21):
            url = base_url + str(page)
            # print(url)
            yield scrapy.Request(url=url,callback=self.getProduct)
            pass



    def getProductLessThan20(self,response):
        print('中途调用')
        pass

    def getProduct(self,response):
        print('response')
        pass
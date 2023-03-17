import time

import scrapy

from graduationProject.spiders.crawling.SaveProduct import SaveProduct

class ProductListLessThan20:

    def getProduct(self,response):
        # 获得第三分类的名字
        third_level_name=response.meta['third_level_name']
        # 获取一共有多少页，此时是从第二页开始的，并且总页数是低于 20 的，此时的 last_item 是最后的总页数
        last_item = response.xpath('//div[@class="l-bg"]//div[@class="pagination-bg"]//a[last()]/text()').extract()[0]

        # 定义基准链接
        base_url = response.url
        # 因为此时的基准链接最后有个 / ，因此不能直接拼接，需要先去除最后一个 / ，然后再与 -0-0-0-0- 进行拼接
        # 改变了，需要 -2，不然多几个0
        base_url = base_url[:-2]

        # 此后到 for 之前为止，都是爬取第二页的数据
        # 设置爬取具体商品的基准链接
        second_base_url = 'https://www.cnhnb.com'
        # 获取第二页的所有商品的链接
        all_list = response.xpath('//div[@class="supply-list"]//div[@class="supply-item"]//a//@href').extract()
        for item in all_list:
            url = second_base_url + item
            # time.sleep(1)
            save_product=SaveProduct()
            # time.sleep(0.2)
            yield scrapy.Request(url=url, callback=save_product.saveProduct,meta={'third_level_name':third_level_name}, dont_filter=True)

        # 使用 for 循环爬取后面页数的代码，确保大于 3 页
        if int(last_item) >2:
            for page in range(3, int(last_item)+1):
                # 要使用 str() ，python 不能字符串和数字自动转换拼接
                url = base_url + str(page)
                # time.sleep(0.2)
                yield scrapy.Request(url=url, callback=self.getPages,meta={'third_level_name':third_level_name}, dont_filter=True)
        pass

    # 爬取第三页及以后的数据
    def getPages(self, response):
        # 获得第三分类的名字
        third_level_name=response.meta['third_level_name']
        # 设置基准链接
        base_url = 'https://www.cnhnb.com'
        # 获取每页的所有商品的链接
        all_list = response.xpath('//div[@class="supply-list"]//div[@class="supply-item"]//a//@href').extract()
        for item in all_list:
            url = base_url + item
            save_product=SaveProduct()
            # time.sleep(0.2)
            yield scrapy.Request(url=url, callback=save_product.saveProduct,meta={'third_level_name':third_level_name}, dont_filter=True)

    # def getPageProduct(self,response):
    #     # 获得第三分类的名字
    #     third_level_name=response.meta['third_level_name']
    #     print(response)
    #     pass
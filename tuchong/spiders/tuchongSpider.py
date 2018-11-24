import scrapy
import json
from scrapy.spiders import Spider
from tuchong.items import TuchongItem
from scrapy.utils.response import open_in_browser


class TuChongSpider(Spider):
    name = "tuchong"
    # start_urls = ["https://tuchong.com/explore/"]   # 起始网址

    # yield 是一个类似 return 的关键字，只是这个函数返回的是个生成器。
    # yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，
    # Python 解释器会将其视为一个 generator，调用这里的 parse() 不会执行 parse 函数，而是返回一个 iterable 对象！
    # 在 for 循环遍历 parse 时，每次循环都会执行 parse 函数内部的代码，执行到 yield  时，parse 函数就返回一个迭代值，
    # 下次迭代时，代码从 yield 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，
    # 于是函数继续执行，直到再次遇到 yield。

    tag_url = 'https://tuchong.com/rest/tags/%s/posts?page=%d&count=%d&order=weekly'  # 热门
    # tag_url = 'https://tuchong.com/rest/tags/%s/posts?page=%d&count=%d&order=new'   # 最新
    comment_url = 'https://tuchong.com/rest/2/posts/%s/comments?page=%d&count=%d'  # 评论
    # 评论有两种情况
    # 1. 作者主页为 https://xxxx.tuchong.com的
    # 2. 作者主页为 https://tuchong.com/12345678/的
    # 第一种情况可以用 https://xxxx.tuchong.com 前缀或者https://tuchong.com 前缀的评论api
    # 第二种情况zhineny https://tuchong.com 前缀的评论api
    # 综上，直接用https://tuchong.com 前缀

    # 图虫用了ajax，不能直接获得内容
    def start_requests(self):

        # 抓取20个页面，每页20个图集
        # 指定 parse 作为回调函数并返回 Requests 请求对象
        for page in range(1, 21):
            yield scrapy.Request(url=self.tag_url % ('风光', page, 20), callback=self.parse)

    # 直接解析json获取图片内容
    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        for post in body['postList']:
            url2 = post['url']         # 作品地址

            title = post['title']   # 标题
            published_time = post['published_at']  # 发布时间
            favorites = post['favorites']  # 喜欢
            views = post['views']         # 阅读量
            img_count = int(post['image_count'])    # 图片数
            post_id = post['post_id']
            # 从作品地址获取作者首页地址，用于下面拼接出api接口
            author_url = url2.split('/'+post_id)[0]

            # 将 images 处理成 {img_id: img_url} 对象数组
            imgs = []
            for img in post.get('images', ''):
                # 图片地址
                img_url = 'https://photo.tuchong.com/%s/f/%s.jpg' % (
                    post['site_id'], img['img_id'])
                imgs.append(img_url)
            # 处理tags
            tags = []
            for tag in post.get('tags', ''):
                tag_name = tag['tag_name']
                tags.append(tag_name)

            item = TuchongItem()
            item['url'] = url2
            item['title'] = title
            item['img_count'] = img_count
            item['pic_urls'] = imgs
            item['published_time'] = published_time
            item['favorites'] = favorites
            item['views'] = views
            item['tags'] = tags
            item['author_url'] = author_url

            page = 1
            count = 10
            yield scrapy.Request(url=self.comment_url % (post_id, page, count), meta={'item': item}, callback=self.detail_parse)

    # 评论

    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        comments = []
        # 如果评论数为0,请求会被重定向到作者主页，就会解析失败
        try:
            body = json.loads(response.body_as_unicode())
            for post in body['commentlist']:
                comments.append(post['content'])
        finally:
            item['comments'] = comments
        return item

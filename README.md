# 运行环境
> python2.7 windows7
# 使用方法
* python taptap.py
* 参数直接在代码里改,一共三个参数
    * url = 'https://www.taptap.com/app/这里使用你想要查的游戏的ID/review?order=update&page={}#review-list
    * page_range = range(1,结束页)
    * game_name = '用个英文名称吧,中文没试过'
* 几个库要安装一下
    * requests
    * bs4
    * pytagcloud
    * jieba
# 注意事项
* 要设置中文字体. 详见: https://blog.csdn.net/tiffany_li2015/article/details/50219687

# 运行效果图
![](qwq_tag.png)
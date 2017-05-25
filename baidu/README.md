# 百度相关脚本
### BDPandel.py
该脚本是为了删除百度云盘重复的大文件。
思路是：

1. 将百度网盘所有文件的Md5、文件大小、名字和路径信息保存在数据库中
2. 根据文件的MD5来区分是否为重复文件，把路径记录下来
3. 根据文件的路径进行批量删除


详细内容参考[博客](http://fuping.site/2017/05/24/Clean-Duplicate-Files-OF-BaiDu-YunPan/)

下载脚本后将数据库信息和Cookie换成自己的。

>Cookie需要有BDUSS和STOKEN的值即可。
>白名单在Python脚本暂时没有添加，可以参考Java的白名单方式。

使用方法：


```python
python BDPandel.py -m 1 //将文件信息入库
python BDPandel.py -m 2 //找出重复的大文件并删除
```

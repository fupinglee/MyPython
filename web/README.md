# Web相关脚本

主要是一些web测试中使用的脚本。

### RSADemo.py

一个RSA加密的demo，包括验证码的识别。
安装依赖
```python
pytesseract==0.1.7
rsa==3.4.2
requests==2.10.0
Pillow==4.2.1
```
>modulus和exponent用来生成Public key，其值是从页面动态获取的。




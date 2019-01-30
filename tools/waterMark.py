"""
批量给图片添加水印

"""


from PIL import Image,ImageDraw,ImageFont
import os

def is_img(ext):	#是否为图片格式
  ext = ext.lower()
  if ext in ['.jpg', '.png', '.jpeg', '.bmp']:
    return True
  else:
    return False

def doWaterMark(path,text):	#添加水印
	try:
		image = Image.open(path)
		font = ImageFont.truetype("FZSTK.TTF",40)
		layer = image.convert('RGBA')
		text_overlay = Image.new("RGBA",layer.size,(255,255,255,0))
		image_draw = ImageDraw.Draw(text_overlay)
		text_size_x,text_size_y = image_draw.textsize(text,font=font)
		text_xy = (layer.size[0] - text_size_x,layer.size[1]-text_size_y)
		image_draw.text(text_xy,text,font=font,fill=(255,0,0,80))
		after = Image.alpha_composite(layer,text_overlay)
		after.save(path)
	except Exception as e:
		print(path+"\t添加水印失败")
if __name__ == '__main__':
	directory = 'D:\\Images'	#图片路径
	for x in os.listdir(directory):
		 if is_img(os.path.splitext(x)[1]):
		 	path = os.path.join(directory,x)
		 	text = "浮萍'Blog"	#添加的文字
		 	doWaterMark(path,text)
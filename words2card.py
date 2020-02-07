from PIL import Image, ImageDraw, ImageFont
import json, os, random, time, glob, requests
from io import BytesIO

class Img():

	def __init__(self, save_dir=None):
		self.save_dir = save_dir
		self.font_family = 'static/STHeiti_Light.ttc'
		self.font_size = 30 # 字体大小
		self.line_space = 30 # 行间隔大小
		self.share_img_width = 640
		self.padding = 50
		self.song_name_space = 50
		self.banner_space = 60
		self.text_color = '#767676'
		self.netease_banner = u'来自我的摘抄'
		self.netease_banner_color = '#D3D7D9'
		self.netease_banner_size = 20
		self.netease_icon = 'static/netease_icon.png'
		self.icon_width = 25
		if self.save_dir is not None:
			try:
				os.mkdir(self.save_dir)
			except:
				pass
		self.chars_width = {}
		self.chars = [
			'。', '，', '、', '：', '？', '（', '）', '【', '】', '《', '》', '’', '‘', '“', '”', '！', '~', '—', '…', '；',
		 	'.', ',', '\\', ':', '?', '(', ')', '[', ']', '<', '>', '\'', '\"', '!', '-', '_', '+', '-', '*', '/',
		 	'&', '%', '^', '$', '￥', '#', '@', '`', '·', ' '
		]
		for i in range(ord('0'), ord('9') + 1):
			self.chars.append(chr(i))
		for i in range(ord('a'), ord('z') + 1):
			self.chars.append(chr(i))
		for i in range(ord('A'), ord('Z') + 1):
			self.chars.append(chr(i))

		for char in self.chars:
			self.chars_width[char], _ = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(
				char, font=ImageFont.truetype(self.font_family, self.font_size), spacing=self.font_size)

	def save(self, name, lrc, img_url):
		lyric_font = ImageFont.truetype(self.font_family, self.font_size)
		banner_font = ImageFont.truetype(self.font_family, self.netease_banner_size)

		padding = self.padding
		w = self.share_img_width

		album_img = None
		if img_url.startswith('http'):
			raw_img = requests.get(img_url)
			album_img = Image.open(BytesIO(raw_img.content))
		else:
			album_img = Image.open(img_url)
		
		iw, ih = album_img.size
		album_h = ih *  w // iw

		lrc_revised = ""
		for line in lrc.split('\n'):
			line_list = list(line)
			x = k = delta_x = 0
			for index in range(len(line)):
				delta_x = self.chars_width.get(line[index], self.font_size)
				x += delta_x
				if x > w - padding * 2:
					if line[index] in self.chars[:50]:
						continue
					line_list.insert(index + k, '\n')
					x = delta_x
					k += 1
			lrc_revised += ''.join(line_list) + '\n'
		lrc = lrc_revised

		lyric_w, lyric_h = ImageDraw.Draw(Image.new(mode='RGB', size=(1, 1))).textsize(lrc, font=lyric_font, spacing=self.line_space)

		h = album_h + padding + lyric_h + self.song_name_space + \
			self.font_size + self.banner_space + self.netease_banner_size + padding

		resized_album = album_img.resize((w, album_h), resample=3)
		icon = Image.open(self.netease_icon).resize((self.icon_width, self.icon_width), resample=3)

		out_img = Image.new(mode='RGB', size=(w, h), color=(255, 255, 255))
		draw = ImageDraw.Draw(out_img)

		# 添加封面
		out_img.paste(resized_album, (0, 0))
		
		# 添加文字
		draw.text((padding, album_h + padding), lrc, font=lyric_font, fill=self.text_color, spacing=self.line_space)
		
		# Python中字符串类型分为byte string 和 unicode string两种，'——'为中文标点byte string，需转换为unicode string
		y_song_name = album_h + padding + lyric_h + self.song_name_space
		# song_name = unicode('—— 「', "utf-8") + name + unicode('」', "utf-8")
		song_name = u'—— 「' + name + u'」'
		sw, sh = draw.textsize(song_name, font=lyric_font)
		draw.text((w - padding - sw, y_song_name), song_name, font=lyric_font, fill=self.text_color)
		
		# 添加网易标签
		y_netease_banner = h - padding - self.netease_banner_size
		out_img.paste(icon, (padding, y_netease_banner - 2))
		draw.text((padding + self.icon_width + 5, y_netease_banner), self.netease_banner, font=banner_font, fill=self.netease_banner_color)
		
		img_save_path = ''
		if self.save_dir is not None:
			img_save_path = self.save_dir
		out_img.save(img_save_path + '/' + name + str(int(time.time())) + '.png')

def main():
	generater = Img("output")
	images = glob.glob("image/*.jpg") + glob.glob("image/*.png")
	with open('data.txt', 'r', encoding='utf-8') as reader:
		data = json.loads(reader.read())
		for item in data:
			image = random.choice(images)
			if item['image']:
				image = item['image']
				if not item['image'].startswith("http"):
					image = "image/" + image
			author = item['author'] if item['author'] else "无名氏"
			print("Generating %s's words ... " % author, end="")
			generater.save(author, item['quotes'], image)
			print("done!")

if __name__ == '__main__':
	main()
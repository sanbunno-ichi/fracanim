#-----------------------------------------------------------------
# title: Deep Mandelbrot
# author: sanbunnoichi
# desc: Calculating the deep Mandelbrot by perturbation theory
#       （摂動論による深い位置のマンデルブロートを算出する）
# site: none
# license: none
# version: none
#
#更新履歴
#2025.03.20 公開、ただしソース＆アプリで
#2025.03.15 作成開始
#-----------------------------------------------------------------
import pyxel

import numpy as np
from timeit import default_timer as timer
from numba import njit, prange
import math

MAX_X = 512
MAX_Y = 512

width, height = MAX_X,MAX_Y

MENU_YOFS = 512
SCREEN_WIDTH = MAX_X
SCREEN_HEIGHT = MAX_Y + 128

_pix = [0 for tbl in range(width*height)]
_type = 0
_menu = 0

bailout = 4.0

center_real = "0.0"
center_imag = "0.0"
magnification = '1e72'		#倍率
max_iters = 10000			#最大整数

magni_front = ''
magni_number = 0

TYPE_MAX = 11

#------------------------------------------------------------------------------
#draw_image
#------------------------------------------------------------------------------
@njit('void(uint8[:,:], float64[:,:],  float64, int64, float64)', parallel=True)
def draw_image(image,  ref,  pixel_size,  max_iters, bailout):
	height, width = image.shape[0], image.shape[1]
	max_ref_iteration = ref.shape[0]
	for y in prange(height):
		#print(y)
		dc_y = pixel_size * (y - height//2)
		for x in range(width):
			dc_x = pixel_size * (x - width//2)

			dz_x, dz_y = 0,0
			iteration = 0
			ref_iteration =0
			while iteration < max_iters:
				ref_x, ref_y = ref[ref_iteration][0], ref[ref_iteration][1]
				zx, zy = ref_x+dz_x, ref_y+dz_y
				radius2 = zx*zx + zy*zy
				if radius2 > bailout: break

				# Rebasing
				dradius2 = dz_x*dz_x + dz_y*dz_y
				if radius2<dradius2 or ref_iteration==max_ref_iteration-1:
					dz_x,dz_y = zx, zy
					ref_iteration = 0
					ref_x, ref_y = ref[0][0], ref[0][1]

				dz_x_1 = 2*(ref_x*dz_x-ref_y*dz_y) + (dz_x*dz_x - dz_y*dz_y)  + dc_x
				dz_y_1 = 2*(ref_x*dz_y+ref_y*dz_x) + 2*dz_x*dz_y + dc_y
				dz_x, dz_y = dz_x_1, dz_y_1

				iteration += 1
				ref_iteration+=1

			if iteration < max_iters:
				image[height-1-y, x] = 253*((iteration/1000)%1)

	return

#------------------------------------------------------------------------------
#calc_references
#------------------------------------------------------------------------------
from decimal import Decimal, getcontext
def calc_references( center_real, center_imag, magnification, max_iters, bailout, dtype):
	getcontext().prec = int(Decimal(magnification).log10())+5
	Z=[]
	radius2 = 0.0
	iteration = 0
	c_x, c_y = Decimal(center_real), Decimal(center_imag)
	z_x, z_y = 0, 0
	while iteration < max_iters and radius2 <= bailout:
		Z.append((z_x,z_y))
		z_x, z_y = (z_x*z_x-z_y*z_y) + c_x, (2*z_x*z_y) + c_y
		radius2 = (z_x*z_x) + (z_y*z_y)
		iteration += 1
	return np.array(Z,dtype)

#------------------------------------------------------------------------------
#calc_pixel_size
#------------------------------------------------------------------------------
def calc_pixel_size(width, magnification,dtype ):
	return dtype(Decimal(4.0/width) / Decimal(magnification))

#------------------------------------------------------------------------------
#mdraw
#------------------------------------------------------------------------------
def mdraw(width, height, center_real, center_imag, magnification, max_iters, bailout):

	start = timer()
	ref = calc_references( center_real, center_imag, magnification, max_iters, bailout, np.float64)
	pixel_size = calc_pixel_size(width, magnification, np.float64)
	duration = timer() - start
	print( f'calc_references: {ref.shape[0]}/{max_iters} : {duration:.3f} sec.')

	image = np.zeros((height,width), dtype = np.uint8)
	start = timer()
	draw_image(image, ref, pixel_size, max_iters, bailout)
	duration = timer() - start
	print(f"draw_image: {width}x{height} pixels :  {duration:.3f} sec.")
	return image

"""
#-----------------------------------------------------------------
#パレットファイルを作成する
#-----------------------------------------------------------------
@njit('float32[:](float32)')
def get_color(alpha):
    shift = 0.0
    color = np.empty((3,), np.float32)
    color[0] = (np.cos((alpha*2.0-1.0+shift)*np.pi) + 1.0)
    color[1] = (np.cos((alpha*2.0-0.75+shift)*np.pi) + 1.0)
    color[2] = (np.cos((alpha*2.0-0.5+shift)*np.pi) + 1.0)
    return (color*(0.5*255)).astype(np.float32)

#----------------------------
def make_palet():
	with open('./my_resource.pyxpal', mode='w') as f:
		#No.0の色を設定
		f.write( str(0)+'\n' )
		density = 0.35
		for y in range(1,255):
			alpha = y * 0.05 * density
			alpha = math.log(alpha+1)
			col = get_color( alpha )
			c0 = int(col[0])
			c1 = int(col[1])
			c2 = int(col[2])
			if(c0 > 255):
				c0 = 255
			if(c1 > 255):
				c1 = 255
			if(c2 > 255):
				c2 = 255
			coldata = c0*0x10000 + c1*0x100 + c2
			f.write( hex(coldata).removeprefix('0x')+'\n' )

#-----------------------------------------------------------------
#空の.pyxresファイルを作成する
#-----------------------------------------------------------------
resdata = [	0x50,0x4B,0x03,0x04,0x14,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x21,0x00,0x4C,
			0x7D,0xBE,0xCE,0xA1,0x00,0x00,0x00,0x11,0x15,0x00,0x00,0x13,0x00,0x00,0x00,
			0x70,0x79,0x78,0x65,0x6C,0x5F,0x72,0x65,0x73,0x6F,0x75,0x72,0x63,0x65,0x2E,
			0x74,0x6F,0x6D,0x6C,0xED,0xCC,0x4B,0x0E,0x83,0x30,0x0C,0x04,0xD0,0x7D,0x4E,
			0xC1,0x11,0x50,0x7F,0xBB,0x9E,0x24,0x42,0x55,0x44,0x0C,0x58,0x22,0x09,0xC5,
			0x86,0x5E,0xBF,0x41,0x0A,0xDB,0xEE,0x5A,0x55,0x68,0x76,0x1E,0xDB,0xF3,0xBA,
			0x34,0x07,0xA7,0x8F,0x95,0x66,0xE1,0x14,0xAB,0x7B,0x75,0x31,0xC6,0x5A,0x0E,
			0xAE,0x27,0x69,0x1A,0xF3,0x62,0xAF,0x43,0xDE,0x9E,0xAE,0x37,0x33,0x10,0xF7,
			0x83,0x96,0xE0,0x9D,0xBA,0x3C,0x5A,0x5B,0xE7,0xAF,0x1F,0x35,0x94,0x47,0x0A,
			0x6E,0xFA,0xD8,0xE1,0xD0,0xCB,0xDC,0xE6,0x50,0xA3,0x7E,0x94,0xBA,0xA4,0x25,
			0xFA,0xAD,0x1C,0x93,0x92,0x6C,0x97,0xC6,0x68,0x8A,0xFB,0xB8,0xA6,0x71,0x09,
			0x7B,0xA0,0xAE,0xA3,0x56,0x4B,0x90,0x89,0xC8,0xE7,0xF1,0x5C,0x83,0x01,0x03,
			0x06,0x0C,0x18,0x30,0x60,0xC0,0x80,0x01,0x03,0x06,0x0C,0x18,0x30,0x60,0xC0,
			0x80,0xF9,0x22,0x13,0x16,0xE1,0x76,0x63,0x84,0x9E,0xE5,0xE1,0x7F,0xB7,0x6F,
			0x50,0x4B,0x01,0x02,0x14,0x03,0x14,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x21,
			0x00,0x4C,0x7D,0xBE,0xCE,0xA1,0x00,0x00,0x00,0x11,0x15,0x00,0x00,0x13,0x00,
			0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xA4,0x81,0x00,0x00,0x00,
			0x00,0x70,0x79,0x78,0x65,0x6C,0x5F,0x72,0x65,0x73,0x6F,0x75,0x72,0x63,0x65,
			0x2E,0x74,0x6F,0x6D,0x6C,0x50,0x4B,0x05,0x06,0x00,0x00,0x00,0x00,0x01,0x00,
			0x01,0x00,0x41,0x00,0x00,0x00,0xD2,0x00,0x00,0x00,0x00,0x00,0xFFFF]

#-----------------------------------------------------------------
#make_blank_resource
#-----------------------------------------------------------------
def make_blank_resource()
	with open('./my_resource.pyxres', mode='wb') as f:
		_cnt = 0
		while( resdata[_cnt] != 0xFFFF ):
			#16進数の数値をバイナリ書き込みする
			f.write( resdata[_cnt].to_bytes(1,'big') )
			_cnt+=1

#空のリソースファイルを作成する
make_blank_resource()
#パレットファイルを作成する
make_palet()

"""
#-----------------------------------------------------------------
def update():
	global _menu
	global _type
	global center_real
	global center_imag
	global magnification
	global max_iters
	global magni_front
	global magni_number

	if( _menu == 0 ):
		#メニュー選択
		if getTriggerRIGHT():
			_type += 1
			if( _type >= TYPE_MAX ):
				_type = 0
		elif getTriggerLEFT():
			_type -= 1
			if( _type < 0 ):
				_type = TYPE_MAX - 1
		elif getInputA():

			if( _type == 0 ):		#Simple
				center_real = "-1.768610493014677074503175653270226520239677907588665494812359766720721863405719772"
				center_imag = "0.001266613503868717702066411192242601576193940560471409839484404683951701639387836214"
				magnification = '1e72'

				magni_front = '1e'
				magni_number = 72

				max_iters = 10000
			elif( _type == 1 ):		#Escher-stairs(512x512:2.454sec.)
				center_real = "-1.4745288243866597150338529234652814858152366159373595970988244085363882"
				center_imag = "-0.0000003487076826169475459765969213966576732205034932041774261128754135"
				magnification = '0.8e66'

				magni_front = '0.8e'
				magni_number = 66

				max_iters = 20000
			elif( _type == 2 ):		#Rococo (512x512:76.408sec)
				center_real = "-1.76876898442473700261959292619788254139171165927114985522553497969067887761064140098973721320758899999999999999999999999999999999"
				center_imag = "-0.00216191362891550521831725070129922745099952228048611183539348868567470377745415756262974677771899999999999999999999999999999999"
				magnification = '2e93'

				magni_front = '2e'
				magni_number = 93

				max_iters = 500000
			elif( _type == 3 ):		#Candy (512x512:14.081sec)
				center_real = "-0.107180738697829279360340999999999999999999999997"
				center_imag = "-0.649806014915708984056526999999999999999999999999"
				magnification = '2e19'

				magni_front = '2e'
				magni_number = 19

				max_iters = 500000
			elif( _type == 4 ):		#adventurous-forest(512x512:31.175sec)
				center_real = "-1.628592715100065692740246421411065016210781504987224583927645699258855747539445861746810138167371809624579668378714806728142703763366043312636149151639513061534323902579285270919906743915912519756126984904587485990790076952935528135599999999999999999999999"
				center_imag = "-0.0006524211103784457895307800853381638974244378839807054123237905025557452282257388220027559441478826431197456748863451793661782018706487409345062901219527883216368593640715025508705763177296554682299052874598578922327433211773768848999999999999999999999998"
				magnification = '9.85184797544E228'

				magni_front = '9.85184797544E'
				magni_number = 228

				max_iters = 137000
			elif( _type == 5 ):		#heaven(512x512:5.239sec)
				center_real = "-1.76318254341162830553305389344752837380823691545596149081562559836078692832321311234952871865218128541500509084765175112358402403580276150939292881482525799999999999999999999998"
				center_imag = "0.01301112029473539769759042139694254767421706104013814144429240560692646010846970857463228866512042416021073212703100371864075676784733995579950635855431299999999999999999999999"
				magnification = '1E148'

				magni_front = '1E'
				magni_number = 148

				max_iters = 60000
			elif( _type == 6 ):		#magic(512x512:36.692sec)
				center_real = "-0.7564832970066900239012133696820246293286165925657849586799315589448574587578730184201689267365967578772988407695603766576374269642999999999999999999999999999999"
				center_imag = "0.0702230443937935229896215182418165999480670056421801033794136218374406257397315121084295804357309221080306391667640546316930978149999999999999999999999999999999"
				magnification = '1E126'

				magni_front = '1E'
				magni_number = 126

				max_iters = 238000
			elif( _type == 7 ):		#other-worlds-frightening-digital(512x512:28.911sec)
				center_real = "-1.791959621773670199982760290285134234720014667536718700097404243921192099290972859161932776655100830775456601605748473999999999999999999999999999"
				center_imag = "-0.000000023312033691689496911167858499844017387094859770101206660096067118261881158755536315752503308095675592884423099999999999999999999999999999"
				magnification = '3.78980935963E113'

				magni_front = '3.78980935963E'
				magni_number = 113

				max_iters = 200000
			elif( _type == 8 ):		#hapf-gl(512x512:10.375sec)
				center_real = "-1.410364594260745706588176186762972118793213243854338242161867741778304326"
				center_imag = "-0.136711010515164632751932900773139846402453359380892643209313502999999999"
				magnification = '1.6E53'

				magni_front = '1.6E'
				magni_number = 53

				max_iters = 100000
			elif( _type == 9 ):		#virus(512x512:19.105sec)
				center_real = "-1.774753517530837705738940334970370978021828162902719216038748303534382134584563160647011394568650113675549658827810604500977667609956829284361958257166513471697778668136318939485399402191891172433894560723130048888178008597675569999999999999999999999999999"
				center_imag = "-0.0040366328971117870151629896632344127651024000262734874246218684533475356505732900412154414423722454530812535474088861381325545836009907983993458305694191026346909730374104005767039162618554212725836970662531859186462375067048599999999999999999999999999999"
				magnification = '3E224'

				magni_front = '3E'
				magni_number = 224

				max_iters = 100000

			elif( _type == 10 ):	#編集用
				center_real = "0.0"
				center_imag = "0.0"
				magnification = '1e0'

				magni_front = '1e'
				magni_number = 0

				max_iters = 10000

			_menu = 1

	elif( _menu == 2 ):
		if getInputA():
			_menu = 0
		elif getInputB():
			_menu = 3
		elif getInputC():
			_menu = 4

	elif( _menu == 3 ):
		#magnificationの'E'以降を+1して再描画
		magni_front
		magni_number += 1
		magnification = magni_front + str(magni_number)

		print("magnification = ",magnification)

		_menu = 1

	elif( _menu == 4 ):
		#magnificationの'E'以降を-1して再描画
		magni_front
		magni_number -= 1
		magnification = magni_front + str(magni_number)

		print("magnification = ",magnification)

		_menu = 1

#-----------------------------------------------------------------
def draw():
	global _menu
	global _type
	global center_real
	global center_imag
	global magnification
	global max_iters
	global bailout
	global _results

	
	if( _menu == 0 ):
		#画面クリア
		pyxel.cls(0)

		#タイトル
		pyxel.text( SCREEN_WIDTH//2 - ((4*15)//2), MAX_Y + 20, "DEEP MANDELBROT", 254 )
		#バージョン
		pyxel.text( SCREEN_WIDTH//2 - ((4*14)//2), MAX_Y + 30, "VER.2025.03.20", 254 )

		pyxel.text( SCREEN_WIDTH//2 - ((4*37)//2), MAX_Y + 50, "USE THE LEFT AND RIGHT KEYS TO SELECT", 254 )
		pyxel.text( SCREEN_WIDTH//2 - ((4*14)//2), MAX_Y + 60, "RUN WITH Z-KEY", 254 )

		if( _type == 0 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*7)//2), MAX_Y + 90, "SIMPLE", 254 )
		elif( _type == 1 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*13)//2), MAX_Y + 90, "ESCHER-STAIRS", 254 )
		elif( _type == 2 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*6)//2), MAX_Y + 90, "ROBOCO", 254 )
		elif( _type == 3 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*5)//2), MAX_Y + 90, "CANDY", 254 )
		elif( _type == 4 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*18)//2), MAX_Y + 90, "ADVENTUROUS-FOREST", 254 )
		elif( _type == 5 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*6)//2), MAX_Y + 90, "HEAVEN", 254 )
		elif( _type == 6 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*5)//2), MAX_Y + 90, "MAGIC", 254 )
		elif( _type == 7 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*32)//2), MAX_Y + 90, "OTHER-WORLDS-FRIGHTENING-DIGITAL", 254 )
		elif( _type == 8 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*7)//2), MAX_Y + 90, "HAPF-GL", 254 )
		elif( _type == 9 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*5)//2), MAX_Y + 90, "VIRUS", 254 )
		elif( _type == 10 ):
			pyxel.text( SCREEN_WIDTH//2 - ((4*6)//2), MAX_Y + 90, "NORMAL", 254 )

	elif( _menu == 1 ):
		image = mdraw(width, height, center_real,center_imag, magnification, max_iters, bailout)
		_screen_ptr = pyxel.screen.data_ptr()
		for y in range(height):
			_screen_ptr[y*width+0:y*width+width] = image[0:width][y]

		_menu = 2

	elif( _menu == 2 ):
		#消す
		pyxel.text( SCREEN_WIDTH//2 - ((4*37)//2), MAX_Y + 50, "USE THE LEFT AND RIGHT KEYS TO SELECT", 0 )
		pyxel.text( SCREEN_WIDTH//2 - ((4*14)//2), MAX_Y + 60, "RUN WITH Z-KEY", 0 )
		#表示
		pyxel.text( SCREEN_WIDTH//2 - ((4*15)//2), MAX_Y + 50, "MENU WITH Z-KEY", 254 )
		pyxel.text( SCREEN_WIDTH//2 - ((4*35)//2), MAX_Y + 60, "MAGNIFICATION CONTINUE + WITH X-KEY", 254 )
		pyxel.text( SCREEN_WIDTH//2 - ((4*35)//2), MAX_Y + 70, "MAGNIFICATION CONTINUE - WITH C-KEY", 254 )

#-----------------------------------------------------------------
#入力
#-----------------------------------------------------------------
#左
def getTriggerLEFT():
	if pyxel.btnp(pyxel.KEY_LEFT, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold=10, repeat=10):
		return 1
	else:
		return 0
#右
def getTriggerRIGHT():
	if pyxel.btnp(pyxel.KEY_RIGHT, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold=10, repeat=10):
		return 1
	else:
		return 0
#button-A（決定）
def getInputA():
	if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
		return 1
	else:
		return 0
#button-B（キャンセル）
def getInputB():
	if pyxel.btnp(pyxel.KEY_X, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=10, repeat=10):
		return 1
	else:
		return 0

#button-C（キャンセル）
def getInputC():
	if pyxel.btnp(pyxel.KEY_C, hold=10, repeat=10):
		return 1
	else:
		return 0

#----------------------------
#初期化
pyxel.init( SCREEN_WIDTH, SCREEN_HEIGHT,capture_sec=15 )
#リソース読み込み
pyxel.load("my_resource.pyxres")
#テキストカラー設定
pyxel.colors[254] = 0xFFFFFF		#WHITE
#実行
pyxel.run(update, draw)


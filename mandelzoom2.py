#------------------------------------------
# title: mandelzoom2
# author: sanbunnoichi
# desc: Multicolor Mandelbrot drawing
# site: https://github.com/sanbunno-ichi/fracanim#mandelzoom
# license: MIT
# version: 2.0
#
#-----------------------------------------------------------------
#更新履歴
#2024.09.29 アルゴリズム変わったため ver2.0 とする
#2024.09.28 別グラデパターンのWキー追加
#2024.09.28 スムージング処理を追加
#2024.08.30 ver1.0 公開
#-----------------------------------------------------------------
#複数色マンデルブロート描画
#
#操作方法
#	マウスでカーソル位置を変更して
#	マウス右クリックで拡大
#	マウス左クリックで縮小
#
#	Cキーでグラデカラーに切り替え
#	Wキーで別のグラデカラーに切り替え
#	Gキーでグレーカラーに切り替え
#
#	1～9,0キーで深度切り替え
#
#	Rキーで初期画面にもどる
#-----------------------------------------------------------------
import pyxel
import math

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

max_i = 0x100
xmin = -2.0
xmax = 1.2
ymin = -1.2
ymax = 1.2
pix = [0 for tbl in range(SCREEN_WIDTH * SCREEN_HEIGHT)]

#-----------------------------------------------------------------
#計算
def cal_mbrot():
	global max_i
	global xmin
	global xmax
	global ymin
	global ymax
	global pix

	w = SCREEN_WIDTH
	h = SCREEN_HEIGHT
	i = 0
	j = 0
	k = 0
	x = 0.0
	y = 0.0
	z = 0.0
	x0 = 0.0
	y0 = 0.0
	w1 = 1.0 / w
	h1 = 1.0 / h

	bailout=4.0
	LOG2 = math.log(2)

	p = 0
	for j in range( h ):
		y0 = ymin + (ymax - ymin) * j * h1
		for i in range( w ):
			k = 0
			x0 = xmin + (xmax - xmin) * i * w1
			zx = 0.0
			zy = 0.0
			radius2 = 0.0
			iteration = 0
			while iteration < max_i and radius2 <= bailout:
				zx, zy = zx*zx - zy*zy + x0, 2*zx*zy + y0
				radius2 = zx*zx + zy*zy
				iteration += 1

			alpha = 0
			outside = iteration<max_i
			if outside:
				# smoothing
				log_zn = math.log(radius2) / 2
				nu = math.log(log_zn / LOG2) / LOG2
				alpha = iteration + 1 - nu

				alpha *= 0.05
				alpha = (alpha%1)*255

			k = int(alpha)
			k &= 0xff
			if( k >= 255 ):		#255以上は指定できない
				k = 254
			pix[p] = k
			p+=1
			if( p >= (SCREEN_WIDTH * SCREEN_HEIGHT) ):
				return

#-----------------------------------------------------------------
#マウスで任意の位置を選択（拡大縮小）した時の動作
def zoom_set( isZoom ):
	global xmin
	global xmax
	global ymin
	global ymax

	#マウスカーソル位置をセット
	x = pyxel.mouse_x
	y = pyxel.mouse_y

	xc = xmin + (xmax - xmin) * x / SCREEN_WIDTH
	yc = ymin + (ymax - ymin) * y / SCREEN_HEIGHT

	if( isZoom != 0 ):
		xstep = (xmax - xmin) * 2.0 * 0.5
		ystep = (ymax - ymin) * 2.0 * 0.5
	else:
		xstep = (xmax - xmin) * 0.5 * 0.5
		ystep = (ymax - ymin) * 0.5 * 0.5

	xmin = xc - xstep
	xmax = xc + xstep
	ymin = yc - ystep
	ymax = yc + ystep

	cal_mbrot()

#-----------------------------------------------------------------
#マウスボタン入力
#-----------------------------------------------------------------
def getInputML():
	if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
		return 1
	else:
		return 0

def getInputMR():
	if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
		return 1
	else:
		return 0

#-----------------------------------------------------------------
#更新
def update():
	global max_i
	global xmin
	global xmax
	global ymin
	global ymax

	#深度変更：キー1,2,3,4,5,6,7,8,9,0
	if pyxel.btnp( pyxel.KEY_1 ):
		max_i = 1<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_2 ):
		max_i = 2<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_3 ):
		max_i = 3<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_4 ):
		max_i = 4<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_5 ):
		max_i = 5<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_6 ):
		max_i = 6<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_7 ):
		max_i = 7<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_8 ):
		max_i = 8<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_9 ):
		max_i = 9<<8
		cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_0 ):
		max_i = 10<<8
		cal_mbrot()

	#拡大縮小
	if getInputML():
		zoom_set(0)
	elif getInputMR():
		zoom_set(1)

	#C/Gキーでグラデカラー/グレーカラー切り替え
	if pyxel.btnp(pyxel.KEY_C):
		pyxel.load("my_resource.pyxres", excl_images=True, excl_tilemaps=True, excl_sounds=True, excl_musics=True)
		cal_mbrot()
	elif pyxel.btnp(pyxel.KEY_G):
		pyxel.load("glaycolor.pyxres", excl_images=True, excl_tilemaps=True, excl_sounds=True, excl_musics=True)
		cal_mbrot()
	elif pyxel.btnp(pyxel.KEY_W):
		pyxel.load("getcol.pyxres", excl_images=True, excl_tilemaps=True, excl_sounds=True, excl_musics=True)
		cal_mbrot()

	#Rキーで初期画面にもどる
	elif pyxel.btnp(pyxel.KEY_R):
		max_i = 0x100
		xmin = -2.0
		xmax = 1.2
		ymin = -1.2
		ymax = 1.2
		cal_mbrot()

#-----------------------------------------------------------------
#描画
def draw():
	pyxel.cls(0)
	_screen_ptr = pyxel.screen.data_ptr()
	for _i in range(SCREEN_HEIGHT*SCREEN_WIDTH):
		_screen_ptr[_i] = pix[_i]
#-----------------------------------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='mandelzoom')
pyxel.load("getcol.pyxres", excl_images=True, excl_tilemaps=True, excl_sounds=True, excl_musics=True)
#初期画面作成
cal_mbrot()
#マウスカーソル表示
pyxel.mouse( visible = True )
#実行
pyxel.run(update, draw)

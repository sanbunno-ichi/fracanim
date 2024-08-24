#複数色マンデルブロート描画
#
#マウスでカーソル位置を変更して
#MOUSE_BUTTON_RIGHT	Aボタン（Returnキー）で拡大
#MOUSE_BUTTON_LEFT	Bボタン（Spaceキー）で縮小
#Cキーでグラデカラーに切り替え
#Gキーでグレーカラーに切り替え
#1～0キーで深度切り替え

import pyxel

#512x512にしてhtml化してスマホで起動するとOut of memoryといわれた
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

max_i = 256
xmin = -2.0
xmax = 1.2
ymin = -1.2
ymax = 1.2
pix = [0 for tbl in range(SCREEN_WIDTH * SCREEN_HEIGHT)]

_rgbNum = [0 for tbl in range(3)]
_rgbNum = []

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

	p = 0
	for j in range( 0, h, 1 ):
		y0 = ymin + (ymax - ymin) * j * h1
		for i in range( 0, w, 1 ):
			k = 0
			x0 = xmin + (xmax - xmin) * i * w1
			x = x0
			y = y0
			for k in range( 0, max_i, 1 ):
				z = x * y
				x *= x
				y *= y
				if (x + y >= 4.):
					break
				x = x - y + x0
				y = z + z + y0

			k &= 0xff
			k += 16				#デフォルトカラーを指定しない
			if( k >= 255 ):		#255以上は指定できない
				k = 254
			pix[p] = k
			p+=1
			if( p >= (SCREEN_WIDTH * SCREEN_HEIGHT) ):
				return

#-----------------------------------------------------------------
#マウスで任意の位置を選択（拡大）した時の動作
def zoom_set( is_shift ):
	global xmin
	global xmax
	global ymin
	global ymax

	#マウスカーソル位置をセット
	x = pyxel.mouse_x
	y = pyxel.mouse_y

	#SHIFTキー併用で縮小→is_shift：SHIFTキー押下(1)

	xc = xmin + (xmax - xmin) * x / SCREEN_WIDTH
	yc = ymin + (ymax - ymin) * y / SCREEN_HEIGHT

	if( is_shift != 0 ):
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
	isChange = True

#-----------------------------------------------------------------
#入力（キーボード＆ジョイパッド）ON/OFF = 1/0
#-----------------------------------------------------------------

#上
def getInputUP():
	if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
		return 1
	else:
		return 0
#下
def getInputDOWN():
	if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
		return 1
	else:
		return 0
#左
def getInputLEFT():
	if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
		return 1
	else:
		return 0
#右
def getInputRIGHT():
	if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
		return 1
	else:
		return 0
#button-A（決定）
def getInputA():
	if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
		return 1
	else:
		return 0
#button-B（キャンセル）
def getInputB():
	if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
		return 1
	else:
		return 0
##button-X
#def getInputX():
#	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
#		return 1
#	else:
#		return 0
##button-Y
#def getInputY():
#	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
#		return 1
#	else:
#		return 0

#-----------------------------------------------------------------
def update():
	global max_i

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
	if getInputA():
		zoom_set(0)
	elif getInputB():
		zoom_set(1)

	#C/Gキーでグラデカラー/グレーカラー切り替え
	if pyxel.btnp(pyxel.KEY_C):
		pyxel.load("my_resource.pyxres")
		cal_mbrot()
	elif pyxel.btnp(pyxel.KEY_G):
		pyxel.load("glaycolor.pyxres")
		cal_mbrot()

#	#Rキーで拡大縮小リセット
#	elif pyxel.btnp(pyxel.KEY_R):
#		pyxel.mouse_x = SCREEN_WIDTH/2
#		pyxel.mouse_y = SCREEN_HEIGHT/2
#		max_i = 256
#		xmin = -2.0
#		xmax = 1.2
#		ymin = -1.2
#		ymax = 1.2
#		cal_mbrot()

def draw():
	pyxel.cls(0)
	_xp = 0
	_yp = 0
	for _yp in range(SCREEN_HEIGHT):
		for _xp in range(SCREEN_WIDTH):
			pyxel.pset(_xp, _yp, pix[_yp * SCREEN_WIDTH + _xp])

#-----------------------------------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='mandelzoom')
#パレットロード（255色）
pyxel.load("my_resource.pyxres")
#初期画面作成
cal_mbrot()
#マウスカーソル表示
pyxel.mouse( visible = True )
pyxel.run(update, draw)

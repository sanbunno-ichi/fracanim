#239色マンデルブロート描画
#
#マウスでカーソル位置を変更して
#MOUSE_BUTTON_RIGHT	Aボタン（Returnキー）で拡大
#MOUSE_BUTTON_LEFT	Bボタン（Spaceキー）で縮小
#Cキーでグラデカラーに切り替え
#Gキーでグレーカラーに切り替え
#1～0キーで深度切り替え

import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

maxEscapeTime = 36*7
isGraycol = False
isChange = False


_st_a = 0.0
_st_b = 0.0
_st2_a = 0.0
_st2_b = 0.0
_ed_a = 0.0
_ed_b = 0.0
_spd_a = 0
_spd_b = 0
_anim_max = 100
_anim_cnt = 0
_anim_dir = 0

COL_OFS = 16		#デフォルトカラーを指定しない
#グラデーションカラーデータは255色-Pyxelオリジナル16色を抜いて239色とする
MAX_COL = 239
#-----------------------------------------------------------------
#coloring algorithim:
#start with 2 of the 3 red, green and blue values fixed at either 0 or 255,
#then increase the other R, G or B value in a given number of increments
#repeat this for seven cases and you get a maximum of 1792 colors (7*256)
#note that white repeats 3 times, at the end of cases 2, 4 and 6
#the seven case are:
#case 0: [xGx]R=0,   B=0,   increase green from 0 to 255
#case 1: [xgB]R=0    G=255, increase blue  from 0 to 255
#case 2: [Rgb]G=255, B=255, increase red   form 0 to 255
#case 3: [Rxb]G=0,   B=255, increase red   from 0 to 255
#case 4: [rGb]R=255, B=255, increase green from 0 to 255
#case 5: [rGx]R=255, B=0,   increase green from 0 to 255
#case 6: [rgB]R=255, G=255, increase blue  from 0 to 255
#case 7: [RGB]increase all from 0 to 255
#-----------------------------------------------------------------
#色データ作成用
def makeColor( escapeTime ):
	redNum = 0
	greenNum = 0
	blueNum = 0
	rgbIncrements = int(((maxEscapeTime) / 7))
	caseNum = int(escapeTime / rgbIncrements)
	
	#グレーカラー作成
	#if( isGraycol == True ):
	#caseNum = 7
	
	remainNum = escapeTime % rgbIncrements

	if( caseNum == 0 ):
		redNum = 0
		greenNum = int(MAX_COL / rgbIncrements) * remainNum
		blueNum = 0
	elif( caseNum == 1 ):
		redNum = 0
		greenNum = 255
		blueNum = int(MAX_COL / rgbIncrements) * remainNum
	elif( caseNum == 2 ):
		redNum = int(MAX_COL / rgbIncrements) * remainNum
		greenNum = 255
		blueNum = 255
	elif( caseNum == 3 ):
		redNum = int(MAX_COL / rgbIncrements) * remainNum
		greenNum = 0
		blueNum = 255
	elif( caseNum == 4 ):
		redNum = 255
		greenNum = int(MAX_COL / rgbIncrements) * remainNum
		blueNum = 255
	elif( caseNum == 5 ):
		redNum = 255
		greenNum = int(MAX_COL / rgbIncrements) * remainNum
		blueNum = 0
	elif( caseNum == 6 ):
		redNum = 255
		greenNum = 255
		blueNum = int(MAX_COL / rgbIncrements) * remainNum
	elif( caseNum == 7 ):
		redNum = int(MAX_COL / rgbIncrements) * remainNum
		greenNum = int(MAX_COL / rgbIncrements) * remainNum
		blueNum = int(MAX_COL / rgbIncrements) * remainNum

#	print(escapeTime)
#	pyxel.colors[escapeTime] = redNum * 0x10000 + greenNum * 0x100 + blueNum

	print(hex(redNum * 0x10000 + greenNum * 0x100 + blueNum))
#-----------------------------------------------------------------
max_i = 256
xmin = -2.0
xmax = 1.2
ymin = -1.2
ymax = 1.2
pix = [0 for tbl in range(SCREEN_WIDTH * SCREEN_HEIGHT)]

_rgbNum = [0 for tbl in range(3)]
_rgbNum = []

#毎回描画ではなくて、変化あった時のみ描画の方がいいかも
def cal_mbrot(_a, _b):
#def cal_mbrot():
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
				x = x * x
				y = y * y
				if (x + y >= 4.):
					break
				
				#mandelbrot
#				x = x - y + x0		#実部:z^2+Cの計算	_a = a * a - b * b + x
#				y = z + z + y0		#虚部:z^2+Cの計算	_b = 2 * a * b + y

				#juria
#				x = x - y + 0.3		#x0		#実部:z^2+Cの計算	_a = a * a - b * b + x
#				y = z + z + 0.45	#y0		#虚部:z^2+Cの計算	_b = 2 * a * b + y

#				x = x - y - 0.77	#x0		#実部:z^2+Cの計算	_a = a * a - b * b + x
#				y = z + z + 0.11	#y0		#虚部:z^2+Cの計算	_b = 2 * a * b + y


				#a = pyxel.mouse_x
				#a = a - (SCREEN_WIDTH/2)
				#a = a / (SCREEN_WIDTH/4)
				#a = a * 10
				#b = pyxel.mouse_y
				#b = b - (SCREEN_HEIGHT/2)
				#b = b / (SCREEN_HEIGHT/4)
				#b = b * 10
				##print(a, b)
                
				x = x - y + _a		#実部:z^2+Cの計算	_a = a * a - b * b + x
				y = z + z + _b		#虚部:z^2+Cの計算	_b = 2 * a * b + y

			k &= 0xff
			k += COL_OFS
			if( k >= 255 ):		#255以上は指定できない
				k = 254
			pix[p] = k
			p+=1
			if( p >= (SCREEN_WIDTH * SCREEN_HEIGHT) ):
				return

#-----------------------------------------------------------------
#マウスで任意の位置を選択（拡大）した時の動作（updateに取り込む）
#カーソル移動させて選択でも良い
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

	#cal_mbrot()
	isChange = True

#-----------------------------------------------------------------
#キー入力チェック（キー入力あった時に動作）（updateに取り込む）
#def ev_keyboard():
#	replot = 0;
#	#if＜キー0-9判定＞:
#		x = ev.keyCode == 48? 10 : ev.keyCode - 48;
#		max_i = x<<8;
#		replot = 1;
#	#elif＜キーC判定＞:	#カラー切り替え
#		isGraycol ^= 1;
#		replot = 1;
#
#	if( replot != 0 ):
#		cal_mbrot()



#-----------------------------------------------------------------
#入力（キーボード＆ジョイパッド）ON/OFF = 1/0
#-----------------------------------------------------------------
#	#1キー
#	if pyxel.btnp(pyxel.KEY_1):
#	#Cキー
#	if pyxel.btnp(pyxel.KEY_C):



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
#button-X
def getInputX():
	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
		return 1
	else:
		return 0
#button-Y
def getInputY():
	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
		return 1
	else:
		return 0

#-----------------------------------------------------------------
def update():
	global _st_a
	global _st_b
	global _st2_a
	global _st2_b
	global _ed_a
	global _ed_b
	global _spd_a
	global _spd_b
	global _anim_max
	global _anim_cnt
	global _anim_dir
	global max_i
	
	#深度変更：キー1,2,3,4,5,6,7,8,9,0
	if pyxel.btnp( pyxel.KEY_1 ):
		max_i = 1<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_2 ):
		max_i = 2<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_3 ):
		max_i = 3<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_4 ):
		max_i = 4<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_5 ):
		max_i = 5<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_6 ):
		max_i = 6<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_7 ):
		max_i = 7<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_8 ):
		max_i = 8<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_9 ):
		max_i = 9<<8
		#cal_mbrot()
	elif pyxel.btnp( pyxel.KEY_0 ):
		max_i = 10<<8
		#cal_mbrot()

	#Xキーで拡大、Yキーで縮小
	if pyxel.btnp(pyxel.KEY_X):
		zoom_set(0)
	elif pyxel.btnp(pyxel.KEY_Y):
		zoom_set(1)

	#Cキー
	if pyxel.btnp(pyxel.KEY_C):
		pyxel.load("my_resource.pyxres")
		#cal_mbrot()
	elif pyxel.btnp(pyxel.KEY_G):
		pyxel.load("glaycolor.pyxres")
		#cal_mbrot()

	#RIGHT click
	if getInputB():
		#アニメーション開始位置仮設定
		_st2_a = pyxel.mouse_x
		_st2_a = _st2_a - (SCREEN_WIDTH/2)
		_st2_a = _st2_a / (SCREEN_WIDTH/4)
		_st2_b = pyxel.mouse_y
		_st2_b = _st2_b - (SCREEN_HEIGHT/2)
		_st2_b = _st2_b / (SCREEN_HEIGHT/4)

	if getInputA():
		#アニメーション終了位置設定＆アニメ開始
		_st_a = _st2_a
		_st_b = _st2_b
		_ed_a = pyxel.mouse_x
		_ed_a = _ed_a - (SCREEN_WIDTH/2)
		_ed_a = _ed_a / (SCREEN_WIDTH/4)
		_ed_b = pyxel.mouse_y
		_ed_b = _ed_b - (SCREEN_HEIGHT/2)
		_ed_b = _ed_b / (SCREEN_HEIGHT/4)

		print( _st_a, _st_b, _ed_a, _ed_b )

		_anim_cnt = 0
		_anim_dir = 0
		_spd_a = (_ed_a - _st_a)/_anim_max
		_spd_b = (_ed_b - _st_b)/_anim_max

	#アニメーション実施
	if( _anim_dir == 0 ):
		_anim_cnt += 1
		if( _anim_cnt > _anim_max ):
			_anim_dir = 1
	else:
		_anim_cnt -= 1
		if( _anim_cnt < 0 ):
			_anim_cnt = 0
			_anim_dir = 0

	_a = _st_a + (_anim_cnt * _spd_a)
	_b = _st_b + (_anim_cnt * _spd_b)
	
	cal_mbrot(_a,_b)

	#_a = 0
	#_b = 0
	#if getInputA():
	#	_a = pyxel.mouse_x
	#	_a = _a - (SCREEN_WIDTH/2)
	#	_a = _a / (SCREEN_WIDTH/4)
	#		
	#	_b = pyxel.mouse_y
	#	_b = _b - (SCREEN_HEIGHT/2)
	#	_b = _b / (SCREEN_HEIGHT/4)
    #
	#	#_a = pyxel.rndf(-1, 1)
	#	#_b = pyxel.rndf(-1, 1)
	#	##print(_a, _b)
	#	
	#	cal_mbrot(_a,_b)

def draw():
	pyxel.cls(0)
	_xp = 0
	_yp = 0
	for _yp in range(SCREEN_HEIGHT):
		for _xp in range(SCREEN_WIDTH):
			pyxel.pset(_xp, _yp, pix[_yp * SCREEN_WIDTH + _xp])

#-----------------------------------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

#パレットロード（256色）
pyxel.load("my_resource.pyxres")
#pyxel.load("glaycolor.pyxres")

#255色パレットファイル作成用（出力色データから"0x"を削除すること）
#for _cnt in range(MAX_COL):
#	makeColor(_cnt)

#初期画面作成
cal_mbrot(0,0)

#マウスカーソル表示
pyxel.mouse( visible = True )
pyxel.run(update, draw)

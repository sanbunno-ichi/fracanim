import pyxel

DisplayMode = 2
DisplayTable = [[0 for i in range(2)] for j in range(5)]
DisplayTable[0] = [1024, 1024 ]
DisplayTable[1] = [ 512,  512 ]
DisplayTable[2] = [ 256,  256 ]
DisplayTable[3] = [ 128,  128 ]
DisplayTable[4] = [ 64,    64 ]

SCREEN_WIDTH	= DisplayTable[DisplayMode][0]			#[int]画面サイズ横
SCREEN_HEIGHT	= DisplayTable[DisplayMode][1]			#[int]画面サイズ縦
XSIZE			= SCREEN_WIDTH							#[int]縦サイズ
YSIZE 			= SCREEN_HEIGHT							#[int]横サイズ

MODE_MAX		= 2		#[int]
COLOR_MODE_MAX	= 4		#[int]色モード最大値
COLOR_MAX		= 15	#[int]色要素数

offset			= 0
DEEP			= COLOR_MAX*2			#[int]深度
ZOOM			= -1	#[int]立体拡大率（0:平面）

FRAC_TYPE_MAX	= 19	#[int]フラクタルパターン数
MANDEL_TYPE_MAX = 16	#[int]マンデルブロートパターン数

frac_type		= 0		#[int]パターン

FRAC_ANIM_SPEED_R = 0.003	#[float]複素平面アニメスピード：実数値0.0001
FRAC_ANIM_SPEED_I = 0.003	#[float]複素平面アニメスピード：虚数値0.0001

ANIM 			= 1.0	#[float]アニメーション幅絶対値


#[float]フラクタルパターン
fractal_tbl = [[0 for i in range(FRAC_TYPE_MAX)] for j in range(FRAC_TYPE_MAX)]
#     				RS      RE    IS     IE      AR       AI
fractal_tbl[0]  = [ -1.3,   1.3,  -1.3,  1.3,   -0.75,    0.2      ]
fractal_tbl[1]  = [ -0.1,   0.1,  -0.2,  0.0,   -1.767,   0.011005 ]
fractal_tbl[2]  = [  0.3,   0.7,  -0.2,  0.2,    0.26,    0.0      ]
fractal_tbl[3]  = [ -1.0,   1.0,  -1.0,  1.0,   -0.02,    0.795    ]
fractal_tbl[4]  = [ -1.0,   1.0,  -1.0,  1.0,   -0.6945,  0.297    ]
fractal_tbl[5]  = [ -0.5,   0.5,  -0.5,  0.5,   -0.2,    -0.675    ]
fractal_tbl[6]  = [  0.0,   1.0,   0.0,  1.0,    0.3,     0.0      ]
fractal_tbl[7]  = [ -0.3,   0.3,  -0.3,  0.3,   -0.38,   -0.6      ]
fractal_tbl[8]  = [ -0.3,   0.3,  -0.3,  0.3,   -0.72,    0.305    ]
fractal_tbl[9]  = [ -0.5,   0.5,  -0.5,  0.5,    0.36,   -0.095    ]
fractal_tbl[10] = [ -0.3,   0.3,  -0.3,  0.3,   -1.16,   -0.27     ]
fractal_tbl[11] = [ -0.5,   0.5,  -0.5,  0.5,   -0.04,   -0.695    ]
fractal_tbl[12] = [ -1.0,   1.0,  -1.0,  1.0,   -0.58,   -0.45     ]
fractal_tbl[13] = [ -0.5,   0.5,  -0.5,  0.5,   -1.2,    -0.155    ]
fractal_tbl[14] = [ -0.3,   0.3,  -0.3,  0.3,   -1.24,    0.075    ]
fractal_tbl[15] = [ -0.5,   0.5,  -0.5,  0.5,    0.34,   -0.4      ]
fractal_tbl[16] = [ -1.5,   1.5,  -1.5,  1.5,    1.0,     0.0      ]
fractal_tbl[17] = [ -0.5,   0.5,  -0.5,  0.5,   -0.1,    -0.845    ]
fractal_tbl[18] = [ -0.25,  0.15, -0.45, 0.85,  -0.75,    0.2      ]

#計算変数
fi = 0		#[int]
fj = 0		#[int]
fk = 0		#[int]
ksx = 0		#[int]X（実数）側の長さ
ksy = 0		#[int]Y（虚数）側の長さ

_rs = 0.0	#[float]
_re = 0.0	#[float]
_is = 0.0	#[float]
_ie = 0.0	#[float]
_ar = 0.0	#[float]
_ai = 0.0	#[float]
_dr = 0.0	#[float]X（実数差分）
_di = 0.0	#[float]Y（虚数差分）
_zr = 0.0	#[float]
_zi = 0.0	#[float]
_xx = 0.0	#[float]
_yy = 0.0	#[float]
_rr = 0.0	#[float]
_ii = 0.0	#[float]
_dar = 1.0	#[float]アニメーションパラメータ
_dai = 1.0	#[float]アニメーションパラメータ

colnum = 0		#[int]
coltype = 0		#[int]
fdemo_num = 0	#[int]

posbase = [[0 for i in range(2)] for j in range(XSIZE*YSIZE)]
pos = [[0 for i in range(2)] for j in range(XSIZE*YSIZE)]

#初期座標セット
for yp in range(YSIZE):
	for xp in range(XSIZE):
		posbase[yp * XSIZE + xp][0] = xp	#xpos
		posbase[yp * XSIZE + xp][1] = yp	#ypos

		pos[yp * XSIZE + xp][0] = 0		#xpos
		pos[yp * XSIZE + xp][1] = 0		#ypos

#パレット変更（モード別）No.0=BLACK固定
def set_pallet(mode):

	#パレット初期化
	pyxel.pal()

	if mode == 0:
		#GRAY
		pyxel.colors[0]  = 0x000000		#0
		pyxel.colors[1]  = 0x0F0F0F		#15
		pyxel.colors[2]  = 0x1E1E1E		#30
		pyxel.colors[3]  = 0x2D2D2D		#45
		pyxel.colors[4]  = 0x3C3C3C		#60
		pyxel.colors[5]  = 0x4B4B4B		#75
		pyxel.colors[6]  = 0x5A5A5A		#90
		pyxel.colors[7]  = 0x696969		#105
		pyxel.colors[8]  = 0x787878		#120
		pyxel.colors[9]  = 0x878787		#135
		pyxel.colors[10] = 0x969696		#150
		pyxel.colors[11] = 0xA5A5A5		#165
		pyxel.colors[12] = 0xB4B4B4		#180
		pyxel.colors[13] = 0xC3C3C3		#195
		pyxel.colors[14] = 0xD2D2D2		#210
		pyxel.colors[15] = 0xE1E1E1		#225
	elif mode == 1:
		#RED
		pyxel.colors[0]  = 0x000000		#0
		pyxel.colors[1]  = 0x0F0000		#15
		pyxel.colors[2]  = 0x1E0000		#30
		pyxel.colors[3]  = 0x2D0000		#45
		pyxel.colors[4]  = 0x3C0000		#60
		pyxel.colors[5]  = 0x4B0000		#75
		pyxel.colors[6]  = 0x5A0000		#90
		pyxel.colors[7]  = 0x690000		#105
		pyxel.colors[8]  = 0x780000		#120
		pyxel.colors[9]  = 0x870000		#135
		pyxel.colors[10] = 0x960000		#150
		pyxel.colors[11] = 0xA50000		#165
		pyxel.colors[12] = 0xB40000		#180
		pyxel.colors[13] = 0xC30000		#195
		pyxel.colors[14] = 0xD20000		#210
		pyxel.colors[15] = 0xE10000		#225
	elif mode == 2:
		#GREEN
		pyxel.colors[0]  = 0x000000		#0
		pyxel.colors[1]  = 0x000F00		#15
		pyxel.colors[2]  = 0x001E00		#30
		pyxel.colors[3]  = 0x002D00		#45
		pyxel.colors[4]  = 0x003C00		#60
		pyxel.colors[5]  = 0x004B00		#75
		pyxel.colors[6]  = 0x005A00		#90
		pyxel.colors[7]  = 0x006900		#105
		pyxel.colors[8]  = 0x007800		#120
		pyxel.colors[9]  = 0x008700		#135
		pyxel.colors[10] = 0x009600		#150
		pyxel.colors[11] = 0x00A500		#165
		pyxel.colors[12] = 0x00B400		#180
		pyxel.colors[13] = 0x00C300		#195
		pyxel.colors[14] = 0x00D200		#210
		pyxel.colors[15] = 0x00E100		#225
	elif mode == 3:
		#BLUE
		pyxel.colors[0]  = 0x000000		#0
		pyxel.colors[1]  = 0x00000F		#15
		pyxel.colors[2]  = 0x00001E		#30
		pyxel.colors[3]  = 0x00002D		#45
		pyxel.colors[4]  = 0x00003C		#60
		pyxel.colors[5]  = 0x00004B		#75
		pyxel.colors[6]  = 0x00005A		#90
		pyxel.colors[7]  = 0x000069		#105
		pyxel.colors[8]  = 0x000078		#120
		pyxel.colors[9]  = 0x000087		#135
		pyxel.colors[10] = 0x000096		#150
		pyxel.colors[11] = 0x0000A5		#165
		pyxel.colors[12] = 0x0000B4		#180
		pyxel.colors[13] = 0x0000C3		#195
		pyxel.colors[14] = 0x0000D2		#210
		pyxel.colors[15] = 0x0000E1		#225
	else:
		#COLORFUL
		pyxel.colors[0]  = 0x000000		#0
		pyxel.colors[1]  = 0xFF0000		#RED
		pyxel.colors[2]  = 0x00FF00		#GREEN
		pyxel.colors[3]  = 0x0000FF		#BLUE
		pyxel.colors[4]  = 0xFFFF00		#YELLOW
		pyxel.colors[5]  = 0xFF00FF		#PURPLE
		pyxel.colors[6]  = 0x00FFFF		#MIZUIRO
		pyxel.colors[7]  = 0x7FFFFF		#
		pyxel.colors[8]  = 0xFF7FFF		#
		pyxel.colors[9]  = 0xFFFF7F		#
		pyxel.colors[10] = 0x7FFF00		#
		pyxel.colors[11] = 0x007FFF		#
		pyxel.colors[12] = 0xFF007F		#
		pyxel.colors[13] = 0x3F3F3F		#
		pyxel.colors[14] = 0x7F7F7F		#GRAY
		pyxel.colors[15] = 0xFFFFFF		#WHITE



def main_control():
	global fi
	global fj
	global fk
	global ksx
	global ksy
	global _rs
	global _re
	global _is
	global _ie
	global _ar
	global _ai
	global _dr
	global _di
	global _zr
	global _zi
	global _xx
	global _yy
	global _rr
	global _ii
	global colnum
	global coltype
	global fdemo_num
	global posbase
	global pos
	global _dar
	global _dai
	
	BAISU = 10000		#float <-> int

	if ( fdemo_num < 0 ) or ( fdemo_num > (FRAC_TYPE_MAX - 1) ):
		fdemo_num = 0
		coltype = ( coltype + 1 ) % COLOR_MODE_MAX 

	#画面クリア
	pyxel.cls(0)

	#複素平面
	_rs = fractal_tbl[fdemo_num][0]			# + drs;
	_re = fractal_tbl[fdemo_num][1]			# + dre;
	_is = fractal_tbl[fdemo_num][2]			# + dis;
	_ie = fractal_tbl[fdemo_num][3]			# + die;
	_ar = fractal_tbl[fdemo_num][4] + _dar	#初期差分→自動化
	_ai = fractal_tbl[fdemo_num][5] + _dai

	ksx = XSIZE					# X（実数）側の長さ
	ksy = YSIZE					# Y（虚数）側の長さ
	_dr = (_re - _rs) / ksx		# X（実数差分）
	_di = (_ie - _is)  / ksy	# Y（虚数差分）

	fk = 0
	fi = 0
	fj = 0

	i_yy = int( _yy * BAISU )
	i_is = int( _is * BAISU )
	i_ie = int( _ie * BAISU )
	i_di = int( _di * BAISU )
#	for _yy in range(_is, _ie, _di):
	for i_yy in range(i_is, i_ie, i_di):

		_yy = float( i_yy / BAISU )
		_is = float( i_is / BAISU )
		_ie = float( i_ie / BAISU )
		_di = float( i_di / BAISU )

		fi = 0

		i_xx = int( _xx * BAISU )
		i_rs = int( _rs * BAISU )
		i_re = int( _re * BAISU )
		i_dr = int( _dr * BAISU )
#		for _xx in range(_rs, _re, _dr):
		for i_xx in range(i_rs, i_re, i_dr):

			_xx = float( i_xx / BAISU )
			_rs = float( i_rs / BAISU )
			_re = float( i_re / BAISU )
			_dr = float( i_dr / BAISU )

			_zr = _xx
			_zi = _yy

			fk = 0

			while True:
				fk = fk + 1
				if fk > DEEP:		#深度が高くなると処理量多くなるのでカット
					break

				#複素平面
				_rr = (_zr * _zr) - (_zi * _zi) + _ar
				_ii = (2.0 * _zr * _zi) + _ai

				if ((_rr * _rr) + (_ii * _ii)) > 4.0:	 #演算限界値
					break

				_zr = _rr
				_zi = _ii

			colnum = fk % COLOR_MAX

			#描画セット
			offset = fj * XSIZE + fi
			pos[offset][0] = posbase[offset][0]
			pos[offset][1] = posbase[offset][1] + fk
			pyxel.pset(pos[offset][0], pos[offset][1], colnum);

			fi = fi + 1
			if fi >= XSIZE:
			    break		#最大値超えたら終了

		fi0 = fi
		for fi in range(fi0, XSIZE):		#不足サイズ分埋める
			#x方向不足サイズ分描画
			offset = fj * XSIZE + fi
			pos[offset][0] = posbase[offset][0];
			pos[offset][1] = posbase[offset][1] + fk;
			pyxel.pset(pos[offset][0], pos[offset][1], colnum);

		fj = fj + 1
		if fj >= YSIZE:
			break		#最大値超えたら終了

	fj0 = fj
	for fj in range(fj0, YSIZE):		#不足サイズ分埋める
		for fi in range(0, XSIZE):		#y方向不足サイズ描画
			offset = fj * XSIZE + fi;
			pos[offset][0] = posbase[offset][0];
			pos[offset][1] = posbase[offset][1] + fk;
			pyxel.pset(pos[offset][0], pos[offset][1], colnum);

	#アニメ実行
	#アニメーションはマイナス方向へ
	_dar = _dar - FRAC_ANIM_SPEED_R
	_dai = _dai - FRAC_ANIM_SPEED_I

	#アニメ終了判定
	if ( _dar < (-1.0)*ANIM ) or ( _dai < (-1.0)*ANIM ):
		#初期値に戻す
		_dar = ANIM
		_dai = ANIM
		
		fdemo_num = fdemo_num + 1

#==============================================================================================================
class App:
	#初期化
	def __init__(self):
		pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60, quit_key=pyxel.KEY_NONE)
		#初期パレットセット
		set_pallet(coltype)
		pyxel.run(self.update, self.draw)

	#更新
	def update(self):
		self.dummy_flag = 0		#dummy

	#描画
	def draw(self):
		main_control()

App()

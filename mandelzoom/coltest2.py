import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

def draw():
    pass
def update():
    pass

#--------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
#パレットロード（256色）
pyxel.load("my_resource.pyxres")
#16x16のカラーマップ表示
_divy = int(SCREEN_HEIGHT/16)
_divx = int(SCREEN_WIDTH/16)
_col = 0
for _yp in range(0, 16):
	for _xp in range(0, 16):
		for _sy in range(_yp * _divy, (_yp * _divy) + _divy):
			for _sx in range(_xp * _divx, (_xp * _divx) + _divx):
				pyxel.pset( _sx, _sy, _col )
		_col+=1
		if( _col > 254 ):
			_col = 254		#カラーコードは0～254まで：255は指定できない
pyxel.run(update, draw)

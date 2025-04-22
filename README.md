## Goto Pyxel Contents内実験室
[Pyxel Contents](https://sanbunnoichi1962.web.fc2.com/pyxel_contents.html)

# Deep Mandelbrot
タイトル：Calculating the deep Mandelbrot by perturbation theory  
（摂動論による深い位置のマンデルブロートを算出する）  
ファイル名：pyxel_PT_0320.py / pt.pyxapp  

numbaを使用しているのでhtml化はできません。  
  
[Pythonでマンデルブロ集合を美しく描画する(摂動論編)](https://qiita.com/T-STAR/items/2ef76940f181acbc90f8)  
の実験用コードのPerturbation Theory:SimpleをPyxel化。  
numbaを使用しても処理時間かかるパターンもあります。  
  
表示した座標を取得しても小数値は限界があってより深い場所を見ることはできない。  
なので公開されている座標をあらかじめ設定しています。  
Pyxelで見れますというだけのものですが・・・  
  
下記gifアニメはSIMPLEパターンを倍率72から0まで進めたもの。  
SIMPLEパターンなら処理はあまりかからない。  
![GIF](PT_SimpleBack.gif)  
  
[Deep Mandelbrot Gallery](https://sanbunnoichi1962.web.fc2.com/dm/dm_gallery.html)  

# mandelzoom2
タイトル：複数色マンデルブロート描画 ver2.0<BR>
操作方法：<BR>
　　マウスでカーソル位置を変更して<BR>
　　マウスの左クリックで拡大<BR>
　　マウスの右クリックで縮小<BR>
　　Cキーでグラデカラーに切り替え<BR>
　　Wキーでグラデカラーに切り替え<BR>
　　Gキーでグレーカラーに切り替え<BR>
　　1～9,0キーで深度切り替え<BR>
　　Rキーで初期画面にもどる<BR>
更新履歴  
2024.09.29 スムージング処理組み込み  
           グラデーションカラー追加  
![SS](mandelzoom2.png)

# mandelzoom
タイトル：複数色マンデルブロート描画<BR>
操作方法：<BR>
　　マウスでカーソル位置を変更して<BR>
　　マウスの左クリックで拡大<BR>
　　マウスの右クリックで縮小<BR>
　　Cキーでグラデカラーに切り替え<BR>
　　Gキーでグレーカラーに切り替え<BR>
　　1～9,0キーで深度切り替え<BR>
　　Rキーで初期画面にもどる<BR>
更新履歴  
2024.09.20 data_ptrによる高速化対応追加  
<BR>
Title: Multicolor Mandelbrot drawing  
How to operate:  
　Change the cursor position with the mouse  
　Right click mouse to enlarge  
　Zoom out with left mouse click  
　Switch to gradient color with C key  
　Switch to gray color with G key  
　Switch depth with 1-9,0 keys  
　Return to initial screen with R key  

![SS](mandelzoom.gif)

# juriaanim
タイトル：複数色ジュリアアニメーション  
操作方法：<BR>
　マウスでカーソル位置を変更して<BR>
　マウスの右クリック位置で始点仮設定<BR>
　マウスの左クリック位置で終点設定<BR>
　開始地点から終了地点までをループするアニメーション開始<BR>
　Cキーでグラデカラーに切り替え<BR>
　Gキーでグレーカラーに切り替え<BR>
　Xキーで拡大<BR>
　Yキーで縮小<BR>
　1～9,0キーで深度切り替え<BR>
更新履歴  
2024.09.20 data_ptrによる高速化対応追加  
<BR>
計算処理に時間かかるのでマウス以外のキーは触らない方がいいかも<BR>
![GIF](juriaanim.gif)

# fracanim
タイトル：フラクタルアニメーション  
　操作無しの見るだけアニメーション<BR>
![SS](fracanim.gif)

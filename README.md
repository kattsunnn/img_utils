<!-- save_img修正 -->
# img_utils

画像処理ユーティリティ集。

## img_utils.py

コマンドライン引数で指定した画像ファイルまたはフォルダを読み込み、表示や保存、GUIでの点取得などのユーティリティ関数を提供します。簡易的なCLIエントリポイントも含まれます。

> ### prepare_io_path

input_pathとoutput_pathを作成するデコレータ。


> ### load_img_paths_from_dir

指定ディレクトリ内の画像ファイル（jpg, jpeg, png）を検索してソート済みのパスリストを返します。

**引数**

- **dir_path:** 検索対象ディレクトリのパス（文字列）

**戻り値**

- **img_paths:** 画像ファイルパスのリスト（文字列のリスト）

> ### load_imgs

ファイルパスがファイルなら1枚の画像を読み込み、ディレクトリならディレクトリ内の画像をリストとして読み込みます。存在しないパスは例外を投げます。

**引数**

- **path:** 画像ファイルまたはディレクトリのパス（文字列）

**戻り値**

- **img または imgs:** 単一画像は `numpy.ndarray`、複数は `list[numpy.ndarray]` を返します

> ### save_imgs

画像または画像リストを指定ディレクトリに保存します。出力ディレクトリがなければ作成します。

**引数**

- **imgs:** `numpy.ndarray` または画像のリスト
- **output_path:** 保存先ディレクトリのパス（文字列）
- **file_name_pattern:** ファイル名パターン（デフォルト: `img_{}`）
- **expand:** ファイル拡張子（デフォルト: `.jpg`）

**戻り値**

- **なし:** ファイルをディスクに保存します（戻り値はありません）

> ### show_imgs

画像または画像リストをウィンドウで表示します。キー入力で次へ進めます。

**引数**

- **imgs:** `numpy.ndarray` または画像のリスト

**戻り値**

- **なし:** 画面表示のみ行います

> ### get_img_points_with_gui

GUI上で複数の点をマウスで指定できるインタラクティブ関数です。Undo/Redo/クリア操作に対応し、最終的な点群と描画済み画像を返します。

**引数**

- **img:** 入力画像（`numpy.ndarray`）
- **window_scale:** 表示倍率（デフォルト: `1.0`）

**戻り値**

- **(points, drawn_img):** 選択点の配列（`numpy.ndarray`）と点を描画した画像（`numpy.ndarray`）

> ### get_single_point_with_gui

GUI上で単一の点を選択するための関数です。選択した点と描画画像を返します。点を選ばなかった場合は `None` を返します。

**引数**

- **img:** 入力画像（`numpy.ndarray`）
- **window_scale:** 表示倍率（デフォルト: `1.0`）

**戻り値**

- **(point, drawn_img) または None:** 選択した点（`numpy.ndarray`）と描画画像（`numpy.ndarray`）。未選択時は `None`。

> ### load_coodinates_from_txt

テキストファイルから座標を読み込みます。ファイルは各行が `x y` の形式であることを想定します。

**引数**

- **txt_path:** 座標ファイルのパス（文字列）

**戻り値**

- **coordinates:** 整数座標のリスト（例: `[[x1, y1], [x2, y2], ...]`）

> ### draw_points_on_img

与えられた点群を画像上に円で描画して新しい画像を返します。

**引数**

- **img:** 入力画像（`numpy.ndarray`）
- **points:** 描画する点のリスト（`List[Tuple[int, int]]`）
- **color:** 円の色（`Tuple[int,int,int]`, デフォルト `(0,0,255)`）
- **size:** 円の半径（整数, デフォルト `5`）

**戻り値**

- **output_img:** 点を描画した新しい画像（`numpy.ndarray`）

---

`img_utils.py` には簡易的な CLI エントリポイント（`if __name__ == "__main__"`）があり、コマンドラインから入力パスとウィンドウスケールを受け取って画像読み込み→点取得→表示を行います。


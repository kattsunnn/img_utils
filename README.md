# img_utils
OpenCV (`cv2`) と NumPy を使った簡単な画像入出力ユーティリティ集です。画像の読み込み、保存、表示を行う軽量なヘルパー関数を提供します。

## セットアップ
- 仮想環境を作成して依存ライブラリ（`requirements.txt`）をインストールしてください。

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## リファレンス

### `prepare_io_paths()`
- 説明: CLI 風に `-i/--input` と `-o/--output` をパースして、絶対パスを返します。出力ディレクトリを自動作成します。
- 引数: なし
- 戻り値: `(input_path, output_path)` — 両方とも絶対パスの文字列。

例:

```python
from img_utils import prepare_io_paths

input_path, output_path = prepare_io_paths()
print(input_path, output_path)
```

コマンドライン例:

```bash
python your_script.py -i ./images -o ./outputs
```

### `load_img_paths_from_dir(dir_path)`
- 説明: 指定ディレクトリ内の画像ファイルパスを収集します。対応拡張子は `jpg`, `jpeg`, `png`（大文字小文字両対応）。
- 引数:
	- `dir_path` (str): ディレクトリのパス。
- 戻り値: `list[str]` — 見つかった画像ファイルのパスのリスト（順序は `glob` に依存）。

例:
```python
from img_utils import load_img_paths_from_dir

paths = load_img_paths_from_dir('./images')
for p in paths:
		print(p)
```

### `load_imgs(path)`
- 説明: ファイルまたはディレクトリから画像を読み込みます。
- 引数:
	- `path` (str): 画像ファイルのパス、または画像ファイルを含むディレクトリのパス。
- 戻り値:
	- ファイルを渡した場合: `numpy.ndarray`（画像データ）。
	- ディレクトリを渡した場合: `list[numpy.ndarray]`（読み込んだ画像のリスト）。
	- 存在しないパスなら `ValueError` を送出します。
- 注意:
	- `cv2.imread` が失敗すると `None` を返すので、呼び出し側でのチェックを推奨します。

例:

```python
from img_utils import load_imgs

# 単一ファイル
img = load_imgs('./images/sample.jpg')
if img is None:
		raise RuntimeError('読み込みに失敗しました')

# ディレクトリ
imgs = load_imgs('./images')
print(len(imgs), 'images loaded')
```

### `save_imgs(imgs, output_path, file_name_pattern='img_{}', expand='.jpg')`
- 説明: 画像（単体またはリスト）を指定ディレクトリに連番で保存します。
- 引数:
	- `imgs` (numpy.ndarray または list[numpy.ndarray]): 保存する画像。単一 ndarray を渡すと内部でリスト化されます。
	- `output_path` (str): 保存先ディレクトリ。存在しない場合は作成されます。
	- `file_name_pattern` (str): ファイル名フォーマット。`{}` が連番部分に置き換わります（例: `img_{}` → `img_0000.jpg`）。
	- `expand` (str): 拡張子（デフォルトは `.jpg`）。
- 戻り値: なし。保存したファイルパスを標準出力に出します。

例:
```python
from img_utils import save_imgs, load_imgs

imgs = load_imgs('./images')
save_imgs(imgs, './outputs', file_name_pattern='frame_{}', expand='.png')
```

### `show_imgs(imgs)`
- 説明: 画像（単体またはリスト）をウィンドウで表示します。キー入力で次の画像に進みます。
- 引数:
	- `imgs` (numpy.ndarray または list[numpy.ndarray]): 表示する画像。単一 ndarray を渡すと内部でリスト化されます。
- 戻り値: なし。
- 注意:
	- GUI 環境（X サーバなど）が必要です。ヘッドレス環境では動作しません。

例:
```python
from img_utils import show_imgs, load_imgs

img = load_imgs('./images/sample.jpg')
show_imgs(img)
```

## 注意事項
- `cv2.imread` は読み込みに失敗した場合 `None` を返します。読み込んだ画像が `None` ではないことを確認してください。
- 出力ファイル上書きの扱いやフォーマット変換をする場合は、`save_imgs` の `expand` を調整してください。
from typing import List, Tuple
import os
import cv2
import numpy as np
import argparse
import glob

def prepare_io_paths():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="入力ファイルまたはフォルダのパス")
    parser.add_argument("-o", "--output", required=True, default="outputs", help="出力ディレクトリパス")
    args = parser.parse_args()

    # 絶対パスに変換
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    # 出力フォルダ作成
    os.makedirs(output_path, exist_ok=True)

    return input_path, output_path

def load_img_paths_from_dir(dir_path):
    img_paths = []
    exts = ["jpg", "jpeg", "png"]
    for ext in exts:
        img_paths += glob.glob(os.path.join(dir_path, f"*.{ext}"))
        img_paths += glob.glob(os.path.join(dir_path, f"*.{ext.upper()}"))
    img_paths = list(set(img_paths))
    img_paths.sort()
    return img_paths

def load_imgs(path):

    if os.path.isfile(path):
        img = cv2.imread(path)
        return img

    elif os.path.isdir(path):
        img_paths = load_img_paths_from_dir(path)
        imgs = [cv2.imread(img_path) for img_path in img_paths ]
        return imgs
    
    else:
        raise ValueError(f"入力パスが存在しません: {path}")


def save_imgs(imgs, output_path, file_name_pattern=f"img_{{}}", expand=".jpg"):
    os.makedirs(output_path, exist_ok=True)
    if isinstance(imgs, np.ndarray):
        imgs = [imgs]
    for i, img in enumerate(imgs):
        file_name = file_name_pattern.format(f"{i:04d}") + expand
        file_path = os.path.join(output_path, file_name)
        cv2.imwrite(file_path, img)
        print(f"{file_path} を保存しました。")

def show_imgs(imgs):
    if isinstance(imgs, np.ndarray):
        imgs = [imgs]
    for idx, img in enumerate(imgs):
        # ウィンドウ名を画像ごとに付ける
        win_name = f"img_{idx}" if len(imgs) > 1 else "img"
        cv2.imshow(win_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Todo: 点の大きさを調節できる引数を追加
def get_img_points_with_gui(img, window_scale=1.0):
    window_name="get_img_points_with_gui"
    points = []
    redo_stack = []
    scaled_img = cv2.resize(img, None, fx=window_scale, fy=window_scale, interpolation=cv2.INTER_LINEAR)
    drawn_img = img.copy() 

    def redraw():
        nonlocal drawn_img
        drawn_img = scaled_img.copy()
        for i, (x, y) in enumerate(points):
            scaled_x, scaled_y = round(x*window_scale), round(y*window_scale)
            cv2.circle(drawn_img, (scaled_x, scaled_y), 5, (0, 0, 255), -1)
            cv2.putText(
                drawn_img,
                str(i),
                (scaled_x + 6, scaled_y - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA
            )
        cv2.imshow(window_name, drawn_img)

    def mouse_callback(event, scaled_x, scaled_y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x = round(scaled_x / window_scale)
            y = round(scaled_y / window_scale)
            points.append([x, y])
            print(f"add: [{x}, {y}]")
            redraw()

    cv2.imshow(window_name, scaled_img)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("操作方法: 左クリック=追加 / u=Undo / r=Redo / c=全削除 / q=終了")
    while True:
        key = cv2.waitKey(10) & 0xFF
        # 1個前削除
        if key == ord("u"):
            if points:
                p = points.pop()
                redo_stack.append(p)
                print(f"undo: {p}")
                redraw()
                
        elif key == ord("r"):
            if redo_stack:
                p = redo_stack.pop()
                points.append(p)
                print(f"redo: {p}")
                redraw()

        elif key == ord("c"):
            if points:
                redo_stack.clear()
                points.clear()
                print("clear all points")
                redraw()

        elif key == ord("q"):
            break

    cv2.destroyWindow(window_name)
    
    print("\n[Final Points]")
    for i, (x, y) in enumerate(points):
        print(f"{i}: [{x}, {y}]")

    return np.array(points), drawn_img

def get_single_point_with_gui(img, window_scale=1.0):
    window_name="get_single_point_with_gui"
    point = None
    scale_img = cv2.resize(img, None, fx=window_scale, fy=window_scale, interpolation=cv2.INTER_LINEAR)
    drawn_img = img.copy()

    def mouse_callback(event, x, y, flags, param):
        nonlocal point, drawn_img
        if event == cv2.EVENT_LBUTTONDOWN:
            ox = round(x / window_scale)
            oy = round(y / window_scale)
            point = (ox, oy)
            drawn_img = scale_img.copy()
            cv2.circle(drawn_img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow(window_name, drawn_img)

    cv2.imshow(window_name, scale_img)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("左クリック：選択/再選択 / q：終了")

    while True:
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):  
            break

    cv2.destroyWindow(window_name)

    if point is not None:
        print(f"selected point: {point}")
        return np.array(point, dtype=np.float32), drawn_img
    else:
        print("no point selected")
        return None

def load_coodinates_from_txt(txt_path):
    coordinates = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # 空行をスキップ
            x, y = line.split()
            coordinates.append([int(x), int(y)])
    return coordinates

def draw_points_on_img( img: np.array, points: List[Tuple[int, int]],
                        color: Tuple[int, int, int] = (0,0,255), 
                        size: int = 5
                        ) -> np.ndarray:
    output_img = img.copy()
    for point in points:
        cv2.circle(output_img, point, size, color, thickness=-1)
    return output_img

if __name__ == "__main__":
    
    import sys

    input_path = sys.argv[1]
    window_scale = float(sys.argv[2])
    img = load_imgs(input_path)
    points, img = get_img_points_with_gui(img, window_scale)
    print(type(points))
    show_imgs(img) 
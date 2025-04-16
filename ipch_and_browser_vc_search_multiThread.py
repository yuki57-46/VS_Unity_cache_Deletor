"""
Visuals StudioのipchおよびBrowser.VC.db, Solution.VC.dbを削除するプログラム

features:
    - GitHubCopilotのキャッシュファイルを削除する
        - チェックボックスで選択する
    - Unityのプロジェクトフォルダ内をgitignoreの対象物を削除する
"""
# pylint: disable=W0611
# pylint: disable=W0311

from ast import pattern
from asyncio import futures
from importlib.metadata import requires
import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from unittest import result
import custom_message_box as cmb
import concurrent.futures
import measure_time

# 定数
# ファイル名
OUTPUT_FILE_NAME = "output.txt"
TARGET_FILES = ["Browse.VC.db", "Solution.VC.db"]
TARGET_DIRS = ["ipch"]
ADD_DIRS = [".vs"] # visual studioのキャッシュファイルを丸ごと削除する
# Unityのプロジェクトフォルダ内をgitignoreの対象物を削除する
UNITY_IGNORE_DIRS = ["Library", "Temp", "Obj", "Build", "Builds", "Logs", "UserSettings", ".gradle"]
UNITY_IGNORE_FILES = ["*.csproj", "*.sln"]


# ipch,Browser.VC.dbのパスを書き出す
@measure_time.measure_time
def write_file_path_to_text(folder_path, output_file_path, vs_check, unity_check):  # フォルダパス, 出力ファイル名, .vsフォルダを削除するかどうか
    """
    フォルダ内のipchおよびBrowser.VC.dbのパスを指定したテキストファイルに書き出す

    Args:
        folder_path (str): フォルダパス
            (ex: C:/Users/user/Documents/Visual Studio projects)
        output_file_path (str): 出力ファイル名 (ex: output.txt)
        vs_check (bool): .vsフォルダを削除するかどうか
        unity_check (bool): Unityのプロジェクトフォルダ内を一時ファイルを削除するかどうか

    Returns:
        None: テキストファイルを書き出す
    """
    if folder_path != "":  # フォルダパスが空でない場合
        found_paths = []
        # マルチスレッドで実行する
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if vs_check:
                # .vsフォルダを削除する
                futures = [executor.submit(find_vs_folders, folder_path, ADD_DIRS)]
            else:
                # 通常のVSキャッシュファイル検索
                futures = [executor.submit(find_target_files_and_dirs, folder_path, TARGET_FILES, TARGET_DIRS)]

            # Unityのキャッシュファイル検索
            if unity_check:
                futures.append(executor.submit(find_unity_cache_files, folder_path))

        # メッセージボックス
        messagebox.showinfo("完了", f"書き出しました \n 出力先: {output_file_path}")
    else:
        # 何もしない
        pass

# find_vs_folders関数
def find_vs_folders(folder_path, add_dirs):
    results = []
    for root, dirs, _ in os.walk(folder_path):
        for dir_name in dirs:
            if dir_name in add_dirs:
                results.append(os.path.join(root, dir_name))
    return results

# find_target_files_and_dirs関数
def find_target_files_and_dirs(folder_path, target_files, target_dirs):
    results = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name in target_files:
                results.append(os.path.join(root, file_name))
        for dir_name in dirs:
            if dir_name in target_dirs:
                results.append(os.path.join(root, dir_name))
    return results

def is_unity_project(directory_path):
    """ Unityのプロジェクトディレクトリかどうかを判定する """
    # すべてのファイルをチェックする前に、ProjectSettingsフォルダを確認する
    if not os.path.isdir(os.path.join(directory_path, "ProjectSettings")):
        return False

    # 次に必須ファイルを確認する
    required_files = ["ProjectSettings/ProjectVersion.txt", "Packages/manifest.json"]
    return all(os.path.isfile(os.path.join(directory_path, file)) for file in required_files)

def find_unity_cache_files(folder_path):
    results = []
    # Unityプロジェクトかどうかを確認する
    if not is_unity_project(folder_path):
        return results

    # Unityのキャッシュファイルを検索する
    ignore_dirs = set() # 重複を防ぐためにsetを使用
    for root, dirs, files in os.walk(folder_path):
        # Unity/Hubの中身は削除しない
        if "Unity/Hub" in root.replace("\\", "/"):
            continue

        # 一度対象になったディレクトリは再度対象にならないようにする
        if any(ignored in root for ignored in ignore_dirs):
            continue

        for dir_name in dirs:
            if dir_name in UNITY_IGNORE_DIRS:
                # XR/Tempは削除しない XRフォルダを無視する
                if dir_name == "Temp" and "XR" in root:
                    continue

                ignore_dirs.add(os.path.join(root,dir_name))
                results.append(os.path.join(root, dir_name))

        for file_name in files:
            if any(file_name.endswith(pattern.replace('*', '')) for pattern in UNITY_IGNORE_FILES):
                results.append(os.path.join(root, file_name))

    return results

# ipch,Browser.VC.dbを削除する
def delete_file_path_from_list(list_txt_file):
    """
    テキストファイル内のパスを読み込み、ファイルおよびディレクトリを削除する

    Args:
        list_txt_file (str): 書き出されたファイル名 (ex: output.txt)

    Returns:
        None: ファイルおよびディレクトリを削除する
    """
    if os.path.isfile(list_txt_file):  # ファイルが存在する場合
        with open(list_txt_file, mode='r', encoding='utf-8') as file:  # 読み込みモード
            for line in file:
                line = line.rstrip('\n')
                try:
                    if os.path.isfile(line):
                        os.remove(line)
                    elif os.path.isdir(line):
                        shutil.rmtree(line)
                except PermissionError:
                    # メッセージボックス
                    messagebox.showerror("エラー", "以下のファイルが削除できませんでした \n" + line)
        # メッセージボックス
        messagebox.showinfo("完了", "削除しました")
        # txtファイル削除するかの確認
        if messagebox.askyesno("確認", "txtファイルを削除しますか？"):
            os.remove(list_txt_file)
            messagebox.showinfo("完了", "削除しました")
        else:
            messagebox.showinfo("完了", "削除しませんでした")
    else:
        # メッセージボックス
        messagebox.showerror("エラー", "output.txtが存在しません")


# テキストファイルの内容を表示する
def show_text_file(text_file):
    """
    テキストファイルの内容を表示する

    Args:
        text_file (str): テキストファイル名 (ex: output.txt)

    Returns:
        None: テキストファイルの内容を表示する
    """
    # テキストファイルが存在する場合
    if os.path.isfile(text_file):
        with open(text_file, mode='r', encoding='utf-8') as file:
            # 1行ずつ読み込み
            text = file.read()
            # 1行読み込んだら改行する
            text = text.replace("\n", "\n")
            return text



def unity_cache_path_to_text(folder_path, output_file_path):
    """
    フォルダ内のUnityのキャッシュファイルのパスを指定したテキストファイルに書き出す

    Args:
        folder_path (str): フォルダパス
            (ex: C:/Users/user/Documents/Unity projects)
        output_file_path (str): 出力ファイル名 (ex: output.txt)

    Returns:
        None: テキストファイルを書き出す

    Note:
        Unityのキャッシュファイルは.gitignoreを参考にする
        似たような構成を削除させないための防止策が必要であるため
        .unityがプロジェクトフォルダのAssetsフォルダ内の何処かのディレクトリまたは直下にあると仮定する
        .unityファイルが存在するということはUnityのプロジェクトフォルダであると推定できる
        .unityファイルを基準に親ディレクトリに`.csproj`や`.sln`が存在するかを確認する
        これらが存在する場合はUnityのプロジェクトフォルダとして扱う
    """

    if not is_unity_project(folder_path):
        return

    if folder_path != "": # フォルダパスが空でない場合
        ignore_dirs = set() # 重複を防ぐためにsetを使用
        with open(output_file_path, mode='a', encoding='utf-8') as file: # 追記モード
            for _root, dirs, files in os.walk(folder_path):
                # Unity/Hubの中身は削除しない
                if "Unity/Hub" in _root.replace("\\", "/"):
                    continue
                # 一度対象になったディレクトリは再度対象にならないようにする
                if any(ignored in _root for ignored in ignore_dirs):
                    continue
                for dir_name in dirs:
                    if dir_name in UNITY_IGNORE_DIRS:
                        # XR/Tempは削除しない XRフォルダを無視する
                        if dir_name == "Temp" and "XR" in _root:
                            continue

                        ignore_dirs.add(os.path.join(_root, dir_name))

                        file_path = os.path.join(_root, dir_name)
                        file.write(file_path + "\n")
                for file_name in files:
                    if file_name in UNITY_IGNORE_FILES:
                        file_path = os.path.join(_root, file_name)
                        file.write(file_path + "\n")
    else: # 何もしない
        pass

    return

# メイン関数
if __name__ == "__main__":

    # 画面サイズ
    root = tk.Tk()
    # 画面サイズ
    root.geometry("400x300")
    # 画面タイトル
    root.title("ipch,Browser.VC.dbのパスを書き出す")
    # ラベル
    label = tk.Label(root, text="フォルダを選択してください")
    label.pack()

    # チェックボックス
    vs_var = tk.BooleanVar()
    vs_var.set(False)
    vs_check = tk.Checkbutton(root, text=".vsフォルダを削除する",
                           variable=vs_var)
    vs_check.pack()
    # チェックボックス
    # copilot_var = tk.BooleanVar()
    # copilot_var.set(False)
    # check = tk.Checkbutton(root, text="GitHubCopilotのキャッシュファイルを削除する(未実装)",
    #                        variable=copilot_var)
    # check.pack()
    # チェックボックス
    unity_var = tk.BooleanVar()
    unity_var.set(False)
    check = tk.Checkbutton(root, text="Unityのプロジェクトの一時ファイルを削除する",
                           variable=unity_var)
    check.pack()

    # ボタン
    button = tk.Button(root, text="フォルダ選択",
                       command=lambda:
                       write_file_path_to_text(filedialog.askdirectory(), OUTPUT_FILE_NAME,
                       vs_var.get(), unity_var.get()))
    button.pack()
    # ボタン
    button = tk.Button(root, text="出力されたテキストファイルを表示",
                       command=lambda:
                       cmb.custom_message_box("テキストファイルの内容",
                                              show_text_file(OUTPUT_FILE_NAME), "720", "300"))
    button.pack()
    # ボタン
    button = tk.Button(root, text="リストで削除",
                       command=lambda: delete_file_path_from_list(OUTPUT_FILE_NAME))
    button.pack()
    # ボタン
    # 終了 # pylint: disable=W0108
    button = tk.Button(root, text="終了", command=lambda: root.destroy())
    button.pack()
    # メインループ
    root.mainloop()

"""
Visuals StudioのipchおよびBrowser.VC.db, Solution.VC.dbを削除するプログラム

features:
    - GitHubCopilotのキャッシュファイルを削除する
        - チェックボックスで選択する
    - Unityのプロジェクトフォルダ内をgitignoreの対象物を削除する
"""
# pylint: disable=W0611
# pylint: disable=W0311

import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
import custom_message_box as cmb

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
def write_file_path_to_text(folder_path, output_file_path, vs_dir):  # フォルダパス, 出力ファイル名
    """
    フォルダ内のipchおよびBrowser.VC.dbのパスを指定したテキストファイルに書き出す

    Args:
        folder_path (str): フォルダパス
            (ex: C:/Users/user/Documents/Visual Studio projects)
        output_file_path (str): 出力ファイル名 (ex: output.txt)

    Returns:
        None: テキストファイルを書き出す
    """
    if folder_path != "":  # フォルダパスが空でない場合
        with open(output_file_path, mode='w', encoding='utf-8') as file:  # 書き込みモード
            for _root, dirs, files in os.walk(folder_path):  # フォルダ内のファイルを走査
                if vs_dir is False:
                    for file_name in files:  # ファイル名を取得
                        # ディレクトリ名がipch,ファイル名がBrowse.VC.dbの場合
                            if file_name in TARGET_FILES:
                                file_path = os.path.join(_root, file_name)
                                file.write(file_path + "\n")
                    for dir_name in dirs:
                        if dir_name in TARGET_DIRS:
                            file_path = os.path.join(_root, dir_name)
                            file.write(file_path + "\n")
                else:
                    for dir_name in dirs:
                        if dir_name in ADD_DIRS:
                            file_path = os.path.join(_root, dir_name)
                            file.write(file_path + "\n")
        # メッセージボックス
        messagebox.showinfo("完了", f"書き出しました \n 出力先: {output_file_path}")
    else:
        # 何もしない
        pass


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
    copilot_var = tk.BooleanVar()
    copilot_var.set(False)
    check = tk.Checkbutton(root, text="GitHubCopilotのキャッシュファイルを削除する(未実装)",
                           variable=copilot_var)
    check.pack()
    # チェックボックス
    unity_var = tk.BooleanVar()
    unity_var.set(False)
    check = tk.Checkbutton(root, text="Unityのプロジェクトの一時ファイルを削除する(未実装)",
                           variable=unity_var)
    check.pack()

    # ボタン
    button = tk.Button(root, text="フォルダ選択",
                       command=lambda:
                       write_file_path_to_text(filedialog.askdirectory(), OUTPUT_FILE_NAME, vs_var.get()))
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

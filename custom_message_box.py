"""
tkinterでカスタムメッセージボックスを作成する
"""

from textwrap import wrap
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font


def custom_message_box(title, message, width, height):
    """
    カスタムメッセージボックスを作成する

    Args:
        title (str): タイトル
        message (str): メッセージ
        width (int): 幅
        height (int): 高さ

    Returns:
        None: カスタムメッセージボックスを作成する
    """
    window = tk.Tk()
    window.title(title)
    window.geometry(width + "x" + height)

    # フレーム作成
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # スクロール可能なエリアを作成
    text_area = scrolledtext.ScrolledText(
        frame,
        wrap=tk.WORD,  # 単語単位で折り返す
        width=int(width) // 10,  # 幅を指定
        height=int(height) // 20,  # 高さを指定
        font=("noto sans", 10),  # フォントを指定
    )
    text_area.pack(fill=tk.BOTH, expand=True)

    # メッセージを挿入
    text_area.insert(tk.END, message)
    # 編集不可設定
    text_area.configure(state=tk.DISABLED)

    # OKボタンを作成
    button_frame = tk.Frame(window)
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    # ボタンを右側に配置
    button_frame = tk.Button(button_frame, text="OK", width=10, command=window.destroy)
    button_frame.pack(side=tk.RIGHT)

    # ウィンドウをモーダルダイアログにする
    window.transient()
    window.grab_set()
    window.focus_set()

    # ウィンドウを表示
    window.mainloop()

    # # ラベル
    # label = tk.Label(window, text=message, width=width,
    #                  height=height, anchor=tk.NW, justify=tk.LEFT)
    # label.pack()
    # # ボタン
    # button = tk.Button(window, text="OK", command=lambda: window.destroy)
    # button.pack()

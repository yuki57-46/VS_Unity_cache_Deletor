"""
tkinterでカスタムメッセージボックスを作成する
"""

import tkinter as tk


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
    # ラベル
    label = tk.Label(window, text=message, width=width,
                     height=height, anchor=tk.NW, justify=tk.LEFT)
    label.pack()
    # ボタン
    button = tk.Button(window, text="OK", command=lambda: window.destroy)
    button.pack()

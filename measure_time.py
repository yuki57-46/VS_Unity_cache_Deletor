import time


# 処理時間測定用の関数
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} 実行時間: {elapsed_time:.3f} 秒")
        return result
    return wrapper

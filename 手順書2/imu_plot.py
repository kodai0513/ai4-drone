# --- 1. 定数とライブラリのインポート ---
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


SERIAL_PORT = ''  # ⚠️ 使用するCOMポート名を設定してください (例: 'COM4' や '/dev/ttyUSB0')
BAUD_RATE = 115200     # M5StickCPlus2のスケッチと同じボーレート
MAX_POINTS = 100       # グラフに表示するデータ点の最大数 

# --- 2. 初期化 ---
try:
    # シリアルポートを開く
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2) # ポートが開くのを待つ
    ser.flush()
    print(f"シリアルポート {SERIAL_PORT} を開きました。プロットを開始します...")
except serial.SerialException as e:
    print(f"❌ エラー: シリアルポート {SERIAL_PORT} を開けません。ポート名を確認し、Arduino IDEのシリアルモニタを閉じてください。")
    print(f"詳細: {e}")
    exit()

# データリストの初期化 (時系列データとして使用)
data_x = list(range(MAX_POINTS)) 
data_gx, data_gy, data_gz = [0] * MAX_POINTS, [0] * MAX_POINTS, [0] * MAX_POINTS

# --- 3. グラフの初期設定 ---
fig, ax = plt.subplots(figsize=(10, 6))
# ジャイロの3軸 (X, Y, Z) をプロット
line_gx, = ax.plot(data_x, data_gx, label='Gyro X (Roll)')
line_gy, = ax.plot(data_x, data_gy, label='Gyro Y (Pitch)')
line_gz, = ax.plot(data_x, data_gz, label='Gyro Z (Yaw)')
ax.legend(loc='upper right')
ax.set_title("M5StickC Plus2 Gyro Data Real-time Plot") 
ax.set_xlabel("Time Step (Data Points)")               
ax.set_ylabel("Angular Velocity (deg/s)")
ax.grid(True)
# Y軸の範囲を固定 (±300 deg/s程度を想定)
ax.set_ylim(-300, 300) 

# --- 4. リアルタイム更新関数 ---
def update(frame):
    """グラフを一定間隔で更新するたびに呼び出される関数"""
    try:
        # シリアルから1行読み込み、デコードし、前後の空白を削除
        line = ser.readline().decode('utf-8').strip()
        
    except Exception:
        # 読み込みエラーやデコードエラーは無視して、古いデータでプロットを再描画
        return line_gx, line_gy, line_gz 

    if line:
        try:
            all_values = [float(v) for v in line.split(',') if v.strip()]
            
            # 6軸データ全てが揃っているか確認
            if len(all_values) == 6:
                gx = all_values[3] 
                gy = all_values[4]
                gz = all_values[5]
                
                # 古いデータを削除し、新しいデータを追加 (FIFO)
                data_gx.pop(0)
                data_gy.pop(0)
                data_gz.pop(0)
                
                data_gx.append(gx)
                data_gy.append(gy)
                data_gz.append(gz)

                # プロットデータを更新
                line_gx.set_ydata(data_gx)
                line_gy.set_ydata(data_gy)
                line_gz.set_ydata(data_gz)
                
        except ValueError:
            # データの解析に失敗した場合は無視
            pass
            
    # 描画対象のオブジェクトを返す
    return line_gx, line_gy, line_gz

# --- 5. アニメーションの開始と実行 ---
# interval=50 は 50ミリ秒ごとに update 関数を呼び出す (約20FPS)
ani = FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("\n[Ctrl+C] プロットを終了します。")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close() # シリアルポートを閉じる
        print("シリアルポートを閉じました。")
# pip install pyserial matplotlib
 
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
 
# COMポート名
SERIAL_PORT = ''
# M5StickCPlus2のスケッチと同じボーレート
BAUD_RATE = 0
MAX_POINTS = 100

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    ser.flush()
    print(f"シリアルポート {SERIAL_PORT} を開きました。Light Unitのプロットを開始します...")
except serial.SerialException as e:
    print(f"❌ エラー: シリアルポート {SERIAL_PORT} を開けません。ポート名を確認し、Arduino IDEのシリアルモニタを閉じてください。")
    print(f"詳細: {e}")
    exit()
 
data_x = list(range(MAX_POINTS))
data_light = [0] * MAX_POINTS
 
fig, ax = plt.subplots(figsize=(10, 6))
line_light, = ax.plot(data_x, data_light, label='Light Sensor Value (0-4095)', color='orange')
ax.legend(loc='upper right')
ax.set_title("M5Stack Light Unit Real-time Plot") 
ax.set_xlabel("Time Step (Data Points)")
ax.set_ylabel("Analog Value (0-4095)")
ax.grid(True)
ax.set_ylim(-100, 4195)
 
def update(frame):
    """グラフを一定間隔で更新するたびに呼び出される関数"""
    try:
        line = ser.readline().decode('utf-8').strip()
       
    except Exception:
        return line_light,
 
    if line:
        try:
            light_value = int(line)
            data_light.pop(0)
            data_light.append(light_value)
            line_light.set_ydata(data_light)
               
        except ValueError:
            pass
    return line_light,
 
ani = FuncAnimation(fig, update, interval=50, blit=True, cache_frame_data=False)
 
try:
    plt.show()
except KeyboardInterrupt:
    print("\n[Ctrl+C] プロットを終了します。")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close() # シリアルポートを閉じる
        print("シリアルポートを閉じました。")
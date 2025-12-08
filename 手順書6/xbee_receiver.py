import serial
import time

# --------------------------------------------------
# 設定 (自分の環境に合わせて書き換えてください)
# --------------------------------------------------
COM_PORT = 'COM8'  # XBee(親機)がつながっているポート
BAUD_RATE = 9600   # M5StickC側の設定と合わせる

def main():
    print(f"--- XBee Receiver Started on {COM_PORT} ---")
    print("停止するには Ctrl+C を押してください")

    try:
        # シリアルポートを開く
        # timeout=1 は「データが来なくても1秒で一旦待機を解除する」設定
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        
        # 受信ループ
        while True:
            # データが届いているか確認
            if ser.in_waiting > 0:
                # 1行読み込む (バイナリデータとして届く)
                line_bytes = ser.readline()
                
                try:
                    # バイナリ(bytes)を文字列(string)に変換し、余計な改行などを削除
                    # errors='ignore' は、万が一文字化けデータが来ても無視してエラーにしない設定
                    line_str = line_bytes.decode('utf-8', errors='ignore').strip()
                    
                    # 空行でなければ表示
                    if line_str:
                        print(f"受信データ: {line_str}")
                        
                except Exception as e:
                    print(f"データ変換エラー: {e}")

            # CPU負荷を下げるために少しだけ休む
            time.sleep(0.1)

    except serial.SerialException:
        print(f"エラー: {COM_PORT} を開けません。XCTUが開いていないか確認してください。")
    except KeyboardInterrupt:
        print("\n--- プログラムを終了します ---")
    finally:
        # 最後にお行儀よくポートを閉じる
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("ポートを閉じました")

if __name__ == '__main__':
    main()
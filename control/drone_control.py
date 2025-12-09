import serial
import time
import socket
import threading

COM_PORT = 'COM8'
BAUD_RATE = 9600
LADING_THRESHOLD = 2000

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
sock = None

def tello_send_command(command):
    if sock:
        sock.sendto(command.encode(encoding="utf-8"), (TELLO_IP, TELLO_PORT))
    else:
        print("エラー: ソケットが初期化されていません。")

def serial_receiver_thread(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                line_bytes = ser.readline()
                
                try:
                    line_str = line_bytes.decode('utf-8', errors='ignore').strip()
                    value = int(line_str)
                    print(f"受信データ: {value}")
                    
                    if value >= LADING_THRESHOLD:
                        print("閾値超えを検出！離陸コマンドを送信します。")
                        tello_send_command('takeoff')
                        
                except ValueError:
                    pass
                except Exception as e:
                    print(f"シリアル受信処理中の予期せぬエラー: {e}")

            time.sleep(0.05)
            
    except Exception as e:
        print(f"\n致命的なエラーによりシリアル受信スレッドが終了しました: {e}")

def console_input_thread():
    """コンソールからコマンドを読み取り、Telloに送信するスレッド"""
    print("コマンド入力スレッド開始...")
    print("--- Telloにコマンドを送る準備ができました (例: command, takeoff, land, up 50) ---")
    print("--- 終了するには 'quit' または 'exit' と入力してください ---")
    
    try:
        while True:
            command = input("Tello > ")
            command = command.strip()

            if command.lower() in ['quit', 'exit']:
                print("コマンド入力の終了を検出しました。プログラム全体を終了しています...")
                return

            if command:
                tello_send_command(command)
                
    except EOFError:
        print("\nコマンド入力の終了を検出しました。プログラム全体を終了しています...")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n致命的なエラーによりコマンド入力スレッドが終了しました: {e}")

def main():
    global sock
    print(f"--- XBee & Tello コントローラー開始 (COM: {COM_PORT}, Tello IP: {TELLO_IP}) ---")
    print("--- 終了するには 'quit' または 'exit' と入力するか、Ctrl+C を押してください ---")
    
    ser = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', TELLO_PORT))
        print(f"Telloソケット初期化完了 (ポート: {TELLO_PORT})")
    except Exception as e:
        print(f"エラー: Telloソケットの初期化に失敗しました: {e}")
        return

    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print(f"シリアルポート {COM_PORT} を開きました")
        serial_thread = threading.Thread(target=serial_receiver_thread, args=(ser,), daemon=True)
        serial_thread.start()
        console_input_thread()

    except serial.SerialException:
        print(f"エラー: {COM_PORT} を開けません。XCTUが開いていないか、ポート番号を確認してください。")
    except KeyboardInterrupt:
        print("\n--- Ctrl+C を検出。プログラムを終了します ---")
    finally:
        print("\n--- 終了処理開始 ---")
        if sock:
            sock.close()
            print("Telloソケットを閉じました")
        if ser and ser.is_open:
            ser.close()
            print(f"シリアルポート {COM_PORT} を閉じました")
        
        print("--- プログラムを終了しました ---")

if __name__ == '__main__':
    main()
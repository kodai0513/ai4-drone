#include <M5StickCPlus2.h> // M5StickC Plus2ライブラリ
#include <HardwareSerial.h> // UART通信用
 
// --- 定義・設定 ---
#define LIGHT_SENSOR_PIN 33  // 光センサーの接続ピン
HardwareSerial XBeeSerial(1); // UART1を使用
 
void setup() {
  // 1. M5StickC Plus2の初期化
  auto cfg = M5.config();
  M5.begin(cfg);
  
  // 画面の基本設定（文字サイズなど）
  M5.Display.setRotation(1); // 見やすいように横向きにする（お好みで変更可）
  M5.Display.setTextSize(2);
  M5.Display.println("XBee Light Sensor");
 
  // 2. PCデバッグ用シリアル開始
  Serial.begin(115200);
  Serial.println("--- M5StickC Plus2 XBee Light Sensor Start ---");
 
  // 3. XBeeとの通信設定 (UART1)
  // RX: 36, TX: 26, Baud: 9600
  XBeeSerial.begin(9600, SERIAL_8N1, 36, 26);
  Serial.println("XBee Serial initialized.");
  
  // 光センサーピンを入力モードに設定（analogReadだけでも動作しますが念のため）
  pinMode(LIGHT_SENSOR_PIN, INPUT);
}
 
void loop() {
  // M5StickC Plus2の内部状態更新
  M5.update();
 
  // --------------------------------------------------
  // 1. XBeeモジュールからの受信処理 (データが来ている場合)
  // --------------------------------------------------
  if (XBeeSerial.available()) {
    String receivedData = XBeeSerial.readStringUntil('\n');
    
    // PCのシリアルモニタへ表示
    Serial.print("【受信】XBeeから: ");
    Serial.println(receivedData);
    
    // (オプション) 画面にも受信データを表示したい場合は以下を追加
    // M5.Display.println("RX: " + receivedData);
  }
 
  // --------------------------------------------------
  // 2. 光センサーの値を読み取って送信 (1秒ごと)
  // --------------------------------------------------
  static unsigned long lastSendTime = 0;
  if (millis() - lastSendTime >= 1000) {
    
    // A. 光センサーの値を取得
    int lightValue = analogRead(LIGHT_SENSOR_PIN);
 
    // B. 送信するメッセージを作成
    // 例: "Light: 1234" という文字列にする
    String message = "Light: " + String(lightValue);
 
    // C. XBeeへ送信（改行付き）
    XBeeSerial.println(message);
 
    // D. 確認用出力 (PCシリアル & 本体画面)
    Serial.print("【送信】: ");
    Serial.println(message);
 
    // 画面の特定位置を黒で塗りつぶして数値を更新（チラつき防止の簡易策）
    M5.Display.setCursor(0, 40);
    M5.Display.fillRect(0, 40, 240, 30, BLACK);
    M5.Display.printf("Value: %d", lightValue);
 
    // タイマー更新
    lastSendTime = millis();
  }
}
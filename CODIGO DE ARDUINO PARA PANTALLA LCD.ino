#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ArduinoJson.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Dirección I2C del LCD y tamaño (16x2)

void setup() {
  lcd.begin(16, 2);  // Iniciar el LCD con 16 columnas y 2 filas
  lcd.backlight();  // Encender el backlight del LCD
  Serial.begin(9600);  // Iniciar comunicación serial a 9600 baudios
  lcd.print("Esperando Datos");  // Imprimir mensaje inicial
}

void loop() {
  if (Serial.available() > 0) {
    // Limpiar pantalla al recibir un mensaje
    lcd.clear();
    
    String message = Serial.readString();
    
    // Decodificar el mensaje ASCII
    String decoded_message = asciiToString(message);
    
    // Aplicar el código para eliminar caracteres de inicio y fin, y reemplazar caracteres escapados
    decoded_message = decoded_message.substring(1, decoded_message.length() - 1); // Eliminar los caracteres de inicio y fin
    decoded_message.replace("\\\"", "\""); // Reemplazar \" con "
    decoded_message.replace("\\\\", "\\"); // Reemplazar \\ con \
    
    // Convertir el mensaje a un objeto JSON
    StaticJsonDocument<64> doc;
    deserializeJson(doc, decoded_message);
    
    // Leer los valores de temperatura y humedad del objeto JSON
    float temperature = doc["temperatura"];
    float humidity = doc["humedad"];

    // Mostrar los valores en la pantalla LCD
    lcd.setCursor(0, 0);
    lcd.print("Temperatura: ");
    lcd.print(temperature);
    lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("Humedad: ");
    lcd.print(humidity);
    lcd.print("%");
  }
}

String asciiToString(String ascii) {
  String str;
  for (int i = 0; i < ascii.length(); i++) {
    if (ascii.charAt(i) != '\n' && ascii.charAt(i) != '\r') {
      str += ascii.charAt(i);
    }
  }
  return str;
}


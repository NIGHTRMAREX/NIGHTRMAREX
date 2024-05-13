# Escribe tu código aquí :-)
import network
import time
from machine import Pin, UART
import dht
import ujson
from umqtt.simple import MQTTClient
import machine

# Configuración de la conexión WiFi
wifi_config = {"ssid": "UnachWiFi", "password": ""}

# Configuración de pines para la comunicación entre ESP32 y Arduino Uno
ESP32_TX2 = 17  # Pin TX de ESP32
ESP32_RX2 = 16  # Pin RX de ESP32
ARDUINO_RX = 2  # Pin RX de Arduino Uno
ARDUINO_TX = 3  # Pin TX de Arduino Uno

led = machine.Pin(2, machine.Pin.OUT)

# Configurar UART para la comunicación entre ESP32 y Arduino Uno
uart = UART(1, baudrate=9600, tx=ESP32_TX2, rx=ESP32_RX2)

# Inicializar objeto DHT22
sensor = dht.DHT11(Pin(15))

# Función para conectar a WiFi
def connect_to_wifi():
    print("Connecting to WiFi", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_config["ssid"], wifi_config["password"])
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")
    return wlan


# Conectar a WiFi
wifi_interface = connect_to_wifi()

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "clima-weather"

# Conectar al servidor MQTT
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

prev_weather = ""
while True:
    # Medir temperatura y humedad
    sensor.measure()
    message = ujson.dumps(
        {
            "temperatura": sensor.temperature(),
            "humedad": sensor.humidity(),
        }
    )

    # Codificar el mensaje
    encoded_message = message.encode("utf-8")

    # Convertir a ASCII
    ascii_message = encoded_message.decode("ascii")

    if message != prev_weather:
        # Enviar datos al Arduino Uno a través de UART
        uart.write(ascii_message + "\n")

        # Publicar datos en MQTT
        client.publish(MQTT_TOPIC, message)
        prev_weather = message

        # Encender y apagar el LED 4 veces
        for _ in range(4):
            led.on()
            time.sleep_ms(100)
            led.off()
            time.sleep_ms(100)
    time.sleep(1)

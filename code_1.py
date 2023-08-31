import socket
import pyaudio
import threading
import RPi.GPIO as GPIO

# Sender configuration
SENDER_HOST = '0.0.0.0'  # Host IP
SENDER_PORT = 12345     # Port for sender
RECEIVER_IP = '192.168.29.90'  # Receiver's IP address
RECEIVER_PORT = 12346   # Port for receiver
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096  # Maximum size of each packet

GPIO.setmode(GPIO.BCM)
gpio_pin = 17  # Change this to the actual GPIO pin number you're using
GPIO.setup(gpio_pin, GPIO.OUT)


        

# Initialize PyAudio
audio = pyaudio.PyAudio()
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Set up sender and receiver sockets
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))

ptt_active = False



def receive_audio():
    while True:
        data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
        receiver_stream.write(data)

# Start sender and receiver threads
receiver_thread = threading.Thread(target=receive_audio)

receiver_thread.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 12356))  # Change the port if needed
while True:
    data, _ = server_socket.recvfrom(1024)
    if data == b'high':
        GPIO.output(gpio_pin, GPIO.LOW)
    elif data == b'low':
        GPIO.output(gpio_pin, GPIO.HIGH)






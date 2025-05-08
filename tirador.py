#!/usr/bin/env python3
# Script para controlar motor DC con dos botones y LEDs indicadores

import RPi.GPIO as GPIO
import time

# === Definición de pines (modo BCM) ===
IN1 = 17             # Dirección 1 del motor (L293D)
IN2 = 27             # Dirección 2 del motor (L293D)
ENA = 18             # Pin de habilitación con PWM (L293D)
BUTTON_IZQ = 23      # Botón para disparo a la izquierda (LED azul)
BUTTON_DER = 24      # Botón para disparo a la derecha (LED verde)
LED_VERDE = 5        # LED verde → disparo derecho
LED_AZUL = 6         # LED azul → disparo izquierdo

# === Configuración inicial ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pines de salida
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_AZUL, GPIO.OUT)

# Asegurar que todo esté apagado al iniciar
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(LED_VERDE, GPIO.LOW)
GPIO.output(LED_AZUL, GPIO.LOW)

# Pines de entrada (con pull-down física)
GPIO.setup(BUTTON_IZQ, GPIO.IN)
GPIO.setup(BUTTON_DER, GPIO.IN)

# PWM en el pin de habilitación
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)  # Motor completamente apagado

try:
    while True:
        if GPIO.input(BUTTON_DER) == GPIO.HIGH:
            # Disparo derecho: LED verde encendido, motor en dirección A
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            pwm.ChangeDutyCycle(75)
            GPIO.output(LED_VERDE, GPIO.HIGH)
            GPIO.output(LED_AZUL, GPIO.LOW)

        elif GPIO.input(BUTTON_IZQ) == GPIO.HIGH:
            # Disparo izquierdo: LED azul encendido, motor en dirección B
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            pwm.ChangeDutyCycle(75)
            GPIO.output(LED_VERDE, GPIO.LOW)
            GPIO.output(LED_AZUL, GPIO.HIGH)

        else:
            # Si no hay botón presionado, se apaga el motor y ambos LEDs
            pwm.ChangeDutyCycle(0)
            GPIO.output(LED_VERDE, GPIO.LOW)
            GPIO.output(LED_AZUL, GPIO.LOW)

        time.sleep(0.1)  # Antirebote y ahorro de CPU

except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")

finally:
    pwm.stop()
    del pwm
    GPIO.cleanup()
    print("GPIO liberado correctamente.")


#!/usr/bin/env python
# Simulador de penalti: al presionar un botón, el motor DC gira (disparo) y el servo se lanza como portero aleatorio

import RPi.GPIO as GPIO
import time
import random


def registrar_evento(origen, evento, detalle=""):
    # Registra un evento con timestamp en un archivo de bitácora
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("eventos.log", "a") as f:
        f.write(f"{timestamp} - {origen} - {evento} {detalle}\n")

# === PINES MOTOR DC ===
IN1 = 17             # Dirección 1 del motor
IN2 = 27             # Dirección 2 del motor
ENA = 18             # PWM para velocidad
LED_VERDE = 5        # Indica dirección A (disparo derecho)
LED_AZUL = 6         # Indica dirección B (disparo izquierdo)

# === PINES BOTONES ===
BOTON_DERECHO = 23   # Disparo derecho
BOTON_IZQUIERDO = 24 # Disparo izquierdo

# === PIN SERVO (PORTERO) ===
SERVO = 19           # PWM del servo

# === CONFIGURACIÓN GENERAL ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configurar salidas
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_AZUL, GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)

# Configurar entradas con resistencia pull-down
GPIO.setup(BOTON_DERECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOTON_IZQUIERDO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM para motor DC y servo
pwm_motor = GPIO.PWM(ENA, 1000)   # PWM motor a 1 kHz
pwm_servo = GPIO.PWM(SERVO, 50)   # PWM servo a 50 Hz (necesario para SG90)
pwm_motor.start(0)
pwm_servo.start(0)

def mover_servo(grados):
    """
    Mueve el servo a un ángulo específico.
    Convierte los grados al duty cycle correspondiente (2.5% a 12.5%).
    """
    duty = 2.5 + (grados / 18)
    pwm_servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm_servo.ChangeDutyCycle(0)

def disparar(direccion):
    """
    Activa el motor y lanza el portero aleatoriamente.
    :param direccion: 'derecha' o 'izquierda'
    """
    if direccion == 'derecha':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(LED_VERDE, GPIO.HIGH)
        GPIO.output(LED_AZUL, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(LED_VERDE, GPIO.LOW)
        GPIO.output(LED_AZUL, GPIO.HIGH)

    pwm_motor.ChangeDutyCycle(75)  # Velocidad del motor

    # El portero se lanza al azar a 0 o 180
    angulo = random.choice([0, 180])
    mover_servo(angulo)

    time.sleep(1.5)  # Duración del disparo

    # Apagar motor y LEDs
    pwm_motor.ChangeDutyCycle(0)
    GPIO.output(LED_VERDE, GPIO.LOW)
    GPIO.output(LED_AZUL, GPIO.LOW)

    # Regresar servo al centro
    mover_servo(90)

try:
    mover_servo(90)  # Inicializar el portero al centro

    while True:
        if GPIO.input(BOTON_DERECHO) == GPIO.HIGH:
            disparar('derecha')
            time.sleep(0.3)

        elif GPIO.input(BOTON_IZQUIERDO) == GPIO.HIGH:
            disparar('izquierda')
            time.sleep(0.3)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")

finally:
    pwm_motor.stop()
    pwm_servo.stop()
    GPIO.cleanup()
    print("GPIO liberado correctamente.")


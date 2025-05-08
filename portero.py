#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ===== IMPORTACIÓN DE LIBRERÍAS =====
import RPi.GPIO as GPIO      # Librería para manejar los pines GPIO de la Raspberry Pi
import time                  # Para manejar retardos
import random                # Para elegir una dirección aleatoria

# ===== CONFIGURACIÓN DEL PIN PWM PARA EL SERVO SG90 =====
SERVO_PIN = 19  # GPIO19 (pin físico 35), compatible con PWM por hardware

# ===== CONFIGURACIÓN INICIAL DE GPIO =====
GPIO.setmode(GPIO.BCM)          # Usamos numeración BCM
GPIO.setwarnings(False)         # Evitamos advertencias si se reutiliza el pin
GPIO.setup(SERVO_PIN, GPIO.OUT) # Establece el pin del servo como salida

# ===== CONFIGURACIÓN DE PWM =====
# Los servos como el SG90 se controlan con señales PWM.
# La frecuencia debe ser de 50 Hz (es decir, un pulso cada 20 ms).

# ¿Qué significa esto?
# En cada ciclo de 20 ms, el ancho del pulso determina el ángulo del servo:
# Ángulo   | Ancho de pulso | Duty Cycle
# -------- | ---------------|------------
# 0°       | 0.5 ms         | (0.5 / 20) * 100 = 2.5%
# 90°      | 1.5 ms         | (1.5 / 20) * 100 = 7.5%
# 180°     | 2.5 ms         | (2.5 / 20) * 100 = 12.5%

# Es decir:
# - El rango de giro total del servo (0° a 180°) corresponde a un duty cycle de 2.5% a 12.5%
# - Esto da un rango de 10% para 180 grados
# - Por lo tanto, 180 grados / 10% = 18 grados por cada 1% de duty cycle

# Para convertir un ángulo a duty cycle, usamos esta fórmula:
# duty = 2.5 + (grados / 18)

# Esto genera los pulsos exactos que necesita el servo.
pwm = GPIO.PWM(SERVO_PIN, 50)  # Creamos el objeto PWM con 50 Hz
pwm.start(0)  # Inicia con duty 0 para que no se mueva al encender

# ===== FUNCION PARA MOVER EL SERVO A UN ÁNGULO ESPECÍFICO =====
def mover_servo(grados):
    """
    Mueve el servo al ángulo especificado.
    Calcula el ciclo de trabajo necesario según el ángulo
    usando la fórmula explicada arriba.
    """
    duty = 2.5 + (grados / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)        # Espera a que el servo llegue a la posición
    pwm.ChangeDutyCycle(0) # Evita que el servo zumbe manteniendo la señal activa

# ===== PROGRAMA PRINCIPAL =====
try:
    print("Iniciando simulador de portero...")
    print("Posición inicial: Centro (90°)")
    mover_servo(90)  # Posición inicial al centro del arco

    # Simula un disparo del jugador
    input("Presiona ENTER para simular disparo...")

    # El portero elige aleatoriamente hacia qué lado lanzarse
    direccion = random.choice([0, 180])  # 0 = derecha del tirador, 180 = izquierda

    if direccion == 0:
        print("¡Portero se lanza a la DERECHA del tirador! (0°)")
    else:
        print("¡Portero se lanza a la IZQUIERDA del tirador! (180°)")

    mover_servo(direccion)

except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario con Ctrl+C.")

# ===== LIMPIEZA DE RECURSOS =====
finally:
    pwm.stop()         # Detener la señal PWM
    del pwm            # Eliminar el objeto PWM para evitar errores al salir
    GPIO.cleanup()     # Liberar todos los pines usados
    print("GPIO liberado correctamente.")


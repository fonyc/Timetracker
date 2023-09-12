import RPi.GPIO as GPIO
from time import sleep

def Beep(beepNumber, duration):
    GPIO.setmode(GPIO.BCM)
    buzzer=23

    GPIO.setup(buzzer, GPIO.OUT)
    for x in range(0,beepNumber):
        sleep(duration)
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(duration)
        GPIO.output(buzzer, GPIO.LOW)
    GPIO.cleanup(buzzer)

def PositiveSoundFeedback():
    Beep(1, 0.25)

def NegativeSoundFeedback():
    Beep(3, 0.1)

def InitSoundFeedback():
    # Beep(5, 0.05)
    # Define the frequency values for the notes of the song
    A = 600
    B = 800
    C = 600
    D = 900

    # Define the melody of the song with pauses
    melody = [A, B, C, D]

    # Define the duralog ition of each note and pause in seconds
    note_duration = 0.15
    pause_duration = 0.4

    # Set up the GPIO pin and PWM
    buzzer = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    pwm = GPIO.PWM(buzzer, 50)  # Set frequency to 50 Hz

    # Play the melody
    for note in melody:
        sleep(note_duration)  # Play the note for the specified duration
        pwm.stop()  # Stop the PWM output
        pwm.ChangeFrequency(note)  # Set the PWM frequency to the current note
        pwm.start(50)  # Start the PWM output with 50% duty cycle

    sleep(0.7)  # Add a short pause between notes
    # Clean up the GPIO pin and PWM
    GPIO.cleanup(buzzer)
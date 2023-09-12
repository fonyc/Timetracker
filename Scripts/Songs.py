import RPi.GPIO as GPIO
import time

# Define the frequency values for the notes of the song
A = 400
B = 600
C = 900
D = 300

# Define the melody of the song with pauses
melody = [A, B, C, D]

# Define the duralog ition of each note and pause in seconds
note_duration = 0.1
pause_duration = 0.075

# Set up the GPIO pin and PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
pwm = GPIO.PWM(23, 50)  # Set frequency to 50 Hz

# Play the melody
for note in melody:
    if note == 0:  # If the note is a pause, just wait
        time.sleep(pause_duration)
    else:
        pwm.ChangeFrequency(note)  # Set the PWM frequency to the current note
        pwm.start(50)  # Start the PWM output with 50% duty cycle
        time.sleep(note_duration)  # Play the note for the specified duration
        pwm.stop()  # Stop the PWM output
        time.sleep(pause_duration)  # Add a short pause between notes

# Clean up the GPIO pin and PWM
GPIO.cleanup()

"""
This example shows connecting to the PN532 and writing an M1
type RFID tag

Warning: DO NOT write the blocks of 4N+3 (3, 7, 11, ..., 63)
or else you will change the password for blocks 4N ~ 4N+2.

Note: 
1.  The first 6 bytes (KEY A) of the 4N+3 blocks are always shown as 0x00,
since 'KEY A' is unreadable. In contrast, the last 6 bytes (KEY B) of the 
4N+3 blocks are readable.
2.  Block 0 is unwritable. 
"""
import RPi.GPIO as GPIO

import pn532.pn532 as nfc
from LCDLibrary import PrintLCDEvent, PrintLCDLoop
from pn532 import *
from Timetracker import InputTime
from Buzzer import NegativeSoundFeedback, InitSoundFeedback

if __name__ == "__main__":
    GPIO.setwarnings(False)
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    #pn532 = PN532_I2C(debug=False, reset=20, req=16)
    #pn532 = PN532_UART(debug=False, reset=20)

    #Cuidado con esta linea, me ha petado a mi dos veces ejecutando el script como usuario "pi" y root al mismo tiempo, vente y te explico
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))


    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()

    InitSoundFeedback()

    while True:
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            # print('.', end="")
            # Try again if no card is available.
            if uid is not None:
                break
            #There is already a timer inside the reading process, so its not neccesary to add more time
            PrintLCDLoop(uid)
            
        # Write block #6
        block_number = 6
        key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
        data = bytes(block_number.to_bytes(16, 'big'))

        try:
            pn532.mifare_classic_authenticate_block(
                uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            CardId = int.from_bytes(pn532.mifare_classic_read_block(block_number), 'big')
            dataToPrint = InputTime(CardId)
            PrintLCDEvent(dataToPrint[0], dataToPrint[1],2,1)
        except:
            NegativeSoundFeedback()

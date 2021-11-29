import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

class LCDClass():

    def __init__(self):
        lcd_rs = digitalio.DigitalInOut(board.D25)
        lcd_en = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D23)
        lcd_d5 = digitalio.DigitalInOut(board.D17)
        lcd_d6 = digitalio.DigitalInOut(board.D18)
        lcd_d7 = digitalio.DigitalInOut(board.D22)
        lcd_backlight = digitalio.DigitalInOut(board.D4)

        lcd_columns = 16
        lcd_rows = 2


        self.lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
    
    def updateModeOnLcd(self, modeStr):
        self.lcd.cursor_position(0, 0)
        self.lcd.message = modeStr;

    def updateUnitOnLcd(self, unitStr):
        self.lcd.cursor_position(10, 0)
        self.lcd.message = unitStr;

    def updateDistanceOnLcd(self, distanceDots, divisor):
        self.lcd.cursor_position(0, 1)
        
        self.lcd.message = str(round(distanceDots/divisor,2)) + "                "

    def clear(self):
        self.lcd.clear()

    def displayQuestion(self, str):
        self.lcd.clear()
        self.lcd.cursor_position(0, 0)
        self.lcd.message = str
        self.lcd.cursor_position(0, 1)
        self.lcd.message = "Yes       No"

    def displayMessage(self,str):
        self.lcd.clear()
        self.lcd.message = str


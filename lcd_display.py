#!/usr/bin/env python3
"""
Raspberry Pi I2C LCD Display Controller
========================================
Author      : C. P. Ravi
Company     : Aislyn Technologies Pvt. Ltd.
Hardware    : Raspberry Pi + 16x2 I2C LCD (PCF8574 backpack)
Library     : RPLCD, smbus2

Features:
  - Real-time clock display
  - CPU temperature monitor
  - CPU & RAM usage stats
  - Custom scrolling message
  - Clean menu-driven demo
"""

import time
import subprocess
import psutil
from datetime import datetime
from RPLCD.i2c import CharLCD

# ─── Configuration ────────────────────────────────────────────────────────────
I2C_ADDRESS = 0x27   # Change to 0x3F if your module uses that address
I2C_PORT    = 1      # Use 1 for Raspberry Pi (0 for very old models)
LCD_COLS    = 16
LCD_ROWS    = 2
# ──────────────────────────────────────────────────────────────────────────────


def init_lcd():
    """Initialise and return the LCD object."""
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=I2C_ADDRESS,
        port=I2C_PORT,
        cols=LCD_COLS,
        rows=LCD_ROWS,
        dotsize=8
    )
    lcd.clear()
    return lcd


def get_cpu_temp():
    """Return CPU temperature in Celsius (Raspberry Pi only)."""
    try:
        result = subprocess.run(
            ['vcgencmd', 'measure_temp'],
            capture_output=True, text=True
        )
        temp_str = result.stdout.strip()          # e.g. "temp=42.8'C"
        temp = float(temp_str.replace("temp=", "").replace("'C", ""))
        return temp
    except Exception:
        return 0.0


def get_cpu_usage():
    """Return CPU usage percentage."""
    return psutil.cpu_percent(interval=0.5)


def get_ram_usage():
    """Return RAM usage percentage."""
    ram = psutil.virtual_memory()
    return ram.percent


def display_welcome(lcd):
    """Show a welcome splash screen."""
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("  RPi + LCD  ")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("  C. P. Ravi  ")
    time.sleep(2)


def display_clock(lcd, duration=10):
    """Display real-time date and clock for `duration` seconds."""
    print("[MODE] Clock")
    end_time = time.time() + duration
    while time.time() < end_time:
        now = datetime.now()
        line1 = now.strftime("%a %d %b %Y")    # Mon 17 Mar 2026
        line2 = now.strftime("   %H:%M:%S   ") # HH:MM:SS centred

        lcd.cursor_pos = (0, 0)
        lcd.write_string(line1.ljust(16))
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2.ljust(16))
        time.sleep(1)


def display_system_stats(lcd, duration=10):
    """Display CPU temperature, CPU%, and RAM% in rotation."""
    print("[MODE] System Stats")
    end_time = time.time() + duration
    toggle = True
    while time.time() < end_time:
        cpu_temp  = get_cpu_temp()
        cpu_usage = get_cpu_usage()
        ram_usage = get_ram_usage()

        if toggle:
            line1 = f"CPU: {cpu_usage:.1f}%".ljust(16)
            line2 = f"Temp: {cpu_temp:.1f}C".ljust(16)
        else:
            line1 = f"RAM: {ram_usage:.1f}%".ljust(16)
            line2 = f"CPU: {cpu_usage:.1f}%".ljust(16)

        lcd.cursor_pos = (0, 0)
        lcd.write_string(line1)
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2)

        toggle = not toggle
        time.sleep(2)


def display_scroll(lcd, message, row=1, delay=0.3):
    """Scroll a long message across one row of the LCD."""
    print(f"[MODE] Scrolling: {message}")
    padded = (" " * LCD_COLS) + message + (" " * LCD_COLS)
    for i in range(len(padded) - LCD_COLS + 1):
        lcd.cursor_pos = (row, 0)
        lcd.write_string(padded[i:i + LCD_COLS])
        time.sleep(delay)


def display_custom_message(lcd, line1, line2="", duration=3):
    """Show any two-line message on the LCD."""
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1[:16].ljust(16))
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2[:16].ljust(16))
    time.sleep(duration)


def run_demo(lcd):
    """
    Full demo loop:
      1. Welcome screen
      2. Real-time clock (10 s)
      3. System stats  (10 s)
      4. Scrolling message
      5. Repeat
    """
    display_welcome(lcd)

    while True:
        # ── Clock ───────────────────────────────
        display_custom_message(lcd, "  ** CLOCK **", "")
        display_clock(lcd, duration=10)

        # ── System Stats ────────────────────────
        display_custom_message(lcd, "** SYS STATS **", "")
        display_system_stats(lcd, duration=10)

        # ── Scrolling message ───────────────────
        display_custom_message(lcd, "  ** SCROLL **", "")
        lcd.cursor_pos = (0, 0)
        lcd.write_string("  Scroll Demo:  ")
        display_scroll(
            lcd,
            "Hello! I am C. P. Ravi, Embedded Developer at Aislyn Technologies. ",
            row=1
        )

        time.sleep(1)


def main():
    print("=" * 40)
    print("  Raspberry Pi I2C LCD Controller")
    print("   Author: C. P. Ravi")
    print("   Aislyn Technologies Pvt. Ltd.")
    print("=" * 40)

    lcd = init_lcd()

    try:
        run_demo(lcd)

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")

    finally:
        display_custom_message(lcd, "   Goodbye! :)", "  C. P. Ravi", duration=2)
        lcd.clear()
        lcd.close(clear=True)
        print("[INFO] LCD cleared. Exited cleanly.")


if __name__ == "__main__":
    main()

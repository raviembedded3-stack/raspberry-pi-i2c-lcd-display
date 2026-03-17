# 🖥️ Raspberry Pi I2C LCD Display Controller

Control a 16x2 I2C LCD Display using Raspberry Pi with 
real-time clock, system stats and scrolling text!

## 📋 Description
This project interfaces a 16x2 I2C LCD display with 
Raspberry Pi and shows real-time information like clock, 
CPU temperature, CPU usage and RAM usage.

## ✨ Features
- 🕐 Real-time clock display
- 🌡️ CPU temperature monitor
- 📊 CPU & RAM usage stats
- 📜 Custom scrolling message
- 👋 Welcome splash screen

## 🛠️ Hardware Required
- Raspberry Pi
- 16x2 I2C LCD Display (PCF8574 backpack)
- Jumper Wires

## 📌 I2C Configuration
| Parameter | Value |
|-----------|-------|
| I2C Address | 0x27 |
| I2C Port | 1 |
| LCD Columns | 16 |
| LCD Rows | 2 |

## 💻 Libraries Required
```bash
pip install RPLCD smbus2 psutil
```

## ▶️ How to Run
```bash
python3 lcd_display.py
```

## 📺 Display Modes
| Mode | Description |
|------|-------------|
| Clock | Shows real-time date and time |
| System Stats | Shows CPU temp, CPU%, RAM% |
| Scroll | Scrolls custom message |

## 👨‍💻 Author
**C. P. Ravi**
Embedded Developer | Aislyn Technologies Pvt. Ltd.
📧 raviembedded3@gmail.com
🔗 [GitHub](https://github.com/raviembedded3-stack)
🔗 [LinkedIn](https://www.linkedin.com/in/cp-ravi-7716173b2)

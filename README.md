# ⌚ OZIL SECURITY
### Wearable Linux Cybersecurity Computer

OZIL SECURITY is an experimental wearable Linux computer designed to bring Linux system monitoring and network diagnostics to a compact, smartwatch-style interface.

The project combines Python, Linux, networking, and cybersecurity tools in a wrist-mounted computing device with a small touchscreen.

The goal is to build a portable cybersecurity companion that allows users to monitor system information and perform basic network diagnostics directly from their wrist.

---

## 🚀 Project Vision

Traditional cybersecurity tools are usually accessed through laptops or desktop computers.

OZIL SECURITY explores a different approach: a compact, wrist-mounted Linux computer with a dedicated display, wireless connectivity, and a touchscreen interface.

The device is designed to provide quick access to useful Linux and networking functions while maintaining the appearance of a modern smartwatch.

---

## ✨ Features

### ⌚ Smartwatch Interface
- Compact smartwatch-style user interface.
- Digital clock and date display.
- Dark interface with mint-green accents.
- Touch-friendly navigation designed for a small screen.

### 🐧 Linux Integration
- Linux terminal access.
- Execute supported Linux commands.
- View system information.
- Monitor available system and battery information.

### 🌐 Network Diagnostics
- Display network interface information.
- Check network connectivity.
- Perform DNS lookups.
- Check TCP port connectivity.
- Display Wi-Fi status when supported.

### 🔐 Cybersecurity Learning Tools
- Basic network troubleshooting.
- TCP connectivity testing.
- DNS diagnostics.
- Linux command execution.
- Security-focused system monitoring.

> Network testing should only be performed on systems and networks you own or have permission to assess.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main application logic |
| Tkinter | Graphical user interface |
| Linux | Operating system |
| Socket | Network and TCP connectivity checks |
| Subprocess | Execute supported system commands |
| Threading | Run selected tasks without freezing the interface |
| Git & GitHub | Version control and project documentation |

---

## 🏗️ Hardware Concept

OZIL SECURITY is being developed as a wrist-mounted Linux computer.

The planned hardware includes:

- A compact Linux-compatible computing board.
- A small touchscreen display.
- Wi-Fi connectivity.
- A rechargeable battery and suitable power-management circuit.
- A wrist-mounted enclosure.

**Hardware status:** Experimental design. Final components, dimensions, and power requirements are subject to testing.

---

## 📁 Project Structure

```text
OZIL-SECURITY/
├── README.md
├── LICENSE
├── requirements.txt
├── software/
│   ├── main.py
│   ├── security_tools.py
│   ├── ui/
│   ├── tools/
│   ├── services/
│   └── tests/
├── hardware/
│   ├── compute/
│   ├── display/
│   ├── power/
│   ├── connectivity/
│   ├── pcb/
│   └── enclosure/
├── operating-system/
├── security/
├── networking/
├── design/
├── testing/
├── docs/
├── assets/
└── screenshots/

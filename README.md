# ⌚ OZIL SECURITY
### Wearable Linux Cybersecurity Computer

OZIL SECURITY is an experimental wearable Linux computer designed to bring Linux system monitoring and network diagnostics to a compact, smartwatch-style interface.

The project combines Python, Linux, networking, and cybersecurity tools in a wrist-mounted computing device with a small touchscreen.

The goal is to build a portable cybersecurity companion that allows users to monitor system information and perform basic network diagnostics directly from their wrist.

---

## 📑 Table of Contents

- [Project Vision](#-project-vision)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Hardware Concept](#-hardware-concept)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running the Application](#-running-the-application)
- [Troubleshooting](#-troubleshooting)
- [Development Roadmap](#-development-roadmap)
- [Security Considerations](#-security-considerations)
- [Screenshots](#-screenshots)
- [Future Goals](#-future-goals)
- [Author](#-author)
- [Disclaimer](#️-disclaimer)

---

## 🚀 Project Vision

Traditional cybersecurity tools are usually accessed through laptops or desktop computers.

OZIL SECURITY explores a different approach: a compact, wrist-mounted Linux computer with a dedicated display, wireless connectivity, and a touchscreen interface.

The device is designed to provide quick access to useful Linux and networking functions while maintaining the appearance of a modern smartwatch.

### Design Goals

- Create a compact interface suitable for an approximately 320 × 320 pixel display.
- Maintain a premium smartwatch appearance.
- Use a dark interface with mint-green accents.
- Provide touch-friendly navigation.
- Integrate Linux and network diagnostic tools.
- Prioritize usability, security, and low resource consumption.

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

> **Note:** Feature availability depends on the current implementation and target hardware. Some capabilities may still be under development.

Network testing should only be performed on systems and networks you own or have permission to assess.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Main application logic |
| Tkinter | Graphical user interface |
| Linux | Operating system |
| Socket | DNS and TCP connectivity checks |
| Subprocess | Execute supported system commands |
| Threading | Run background tasks without freezing the interface |
| Git | Version control |
| GitHub | Source code hosting and documentation |

---

## 🏗️ Hardware Concept

OZIL SECURITY is being developed as a wrist-mounted Linux computer.

The planned hardware includes:

- A compact Linux-compatible computing board.
- A small touchscreen display.
- Wi-Fi connectivity.
- A rechargeable battery.
- A suitable charging and power-management circuit.
- A custom wrist-mounted enclosure.

### Hardware Status

The hardware design is experimental. Final components, dimensions, power requirements, and display compatibility must be validated before assembly.

The application can initially be developed and tested on a Linux laptop before being integrated into the wearable device.

---

## 📁 Project Structure

The project is organized into separate directories for software, hardware, operating-system configuration, security, networking, testing, and documentation.

```text
OZIL-SECURITY/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── software/
│   ├── main.py
│   ├── security_tools.py
│   ├── ui/
│   │   ├── watch_face.py
│   │   ├── app_menu.py
│   │   ├── cyber_mode.py
│   │   ├── terminal_ui.py
│   │   ├── system_info.py
│   │   └── settings.py
│   ├── tools/
│   │   ├── network_tools.py
│   │   ├── dns_lookup.py
│   │   ├── port_checker.py
│   │   ├── web_security.py
│   │   ├── linux_tools.py
│   │   └── system_monitor.py
│   ├── services/
│   │   ├── battery_service.py
│   │   ├── wifi_service.py
│   │   ├── display_service.py
│   │   └── startup_service.py
│   └── tests/
│
├── hardware/
│   ├── README.md
│   ├── compute/
│   ├── display/
│   ├── power/
│   ├── connectivity/
│   ├── pcb/
│   └── enclosure/
│
├── operating-system/
├── security/
├── networking/
├── design/
├── testing/
├── docs/
├── assets/
│   ├── icons/
│   ├── images/
│   └── fonts/
└── screenshots/
```

*Note: This represents the planned project structure. Your actual repository may differ as development progresses.*

---

## ⚙️ Getting Started

Follow these steps to set up and run OZIL SECURITY on Ubuntu Linux.

### 1. Prerequisites

Make sure you have:

- Ubuntu Linux or another compatible Linux distribution.
- Python 3.
- Tkinter.
- Git.
- An internet connection for downloading the repository and packages.

### 2. Install Required Packages

Update your package list:

```bash
sudo apt update
```

Install Python, pip, Tkinter, Git, and virtual-environment support:

```bash
sudo apt install python3 python3-pip python3-tk python3-venv git -y
```

Verify the installations:

```bash
python3 --version
git --version
```

### 3. Clone the GitHub Repository

Clone the OZIL SECURITY repository:

```bash
git clone https://github.com/sheikaabu11/Ozil-secuirty_wearable-linux.git
```

Navigate into the project directory:

```bash
cd Ozil-secuirty_wearable-linux
```

If you already have the project on your computer, navigate to your existing project directory instead of cloning it again.

### 4. Check the Project Files

List the files in the current directory:

```bash
ls -la
```

If your application files are inside the `software` directory, check them:

```bash
ls -la software
```

The application uses `main.py` as its entry point and may depend on `security_tools.py` for diagnostic functions.

Make sure the required files exist before starting the application.

### 5. Create a Python Virtual Environment

Using a virtual environment helps isolate project dependencies from other Python applications.

Create the environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your terminal should now indicate that the virtual environment is active.

To deactivate it later, run:

```bash
deactivate
```

### 6. Install Python Dependencies

If the repository contains a populated `requirements.txt` file, install its dependencies:

```bash
python -m pip install -r requirements.txt
```

If the file is empty or the application uses only Python's standard library and Tkinter, additional pip packages may not be necessary.

If pip reports an externally managed environment error, activate the virtual environment and retry the installation.

### 7. Run OZIL SECURITY

Run the command that matches your actual project structure.

**If `main.py` is inside the `software` directory:**

```bash
python3 software/main.py
```

**If `main.py` is in the project root:**

```bash
python3 main.py
```

If you activated the virtual environment, you can use `python` instead of `python3`.

The graphical application requires a working graphical desktop environment.

### 8. Verify the Application

After launching the application:

1. Check whether the main smartwatch interface opens.
2. Verify that the clock and navigation work, if implemented.
3. Test the available system information functions.
4. Test DNS and network diagnostics.
5. Verify that the interface remains responsive during background operations.
6. Record any errors for further development.

Not every feature may work on every Linux device.

---

## ▶️ Running the Application

### Development Workflow

A typical development session looks like this:

**1. Open the project directory**

```bash
cd ~/Desktop/OZIL-SECURITY
```

Alternatively, use the location where you actually stored the repository.

**2. Activate the virtual environment**

```bash
source .venv/bin/activate
```

**3. Start the application**

For a project-root `main.py`:

```bash
python3 main.py
```

For `software/main.py`:

```bash
python3 software/main.py
```

**4. Test changes**

Modify the code, restart the application, and verify that the changes work as expected.

**5. Save your work with Git**

```bash
git add .
git commit -m "Update OZIL SECURITY"
git push
```

The push command requires valid GitHub authentication and write permission to the repository.

---

## 🧪 Testing

Testing is important before deploying the application to wearable hardware.

### Software Testing

- Verify that each diagnostic function returns the expected result.
- Test invalid inputs and unavailable network connections.
- Confirm that errors are handled gracefully.
- Ensure background operations do not freeze the graphical interface.
- Verify that terminal commands execute with appropriate restrictions.

If automated tests using Python's `unittest` framework are available, run:

```bash
python3 -m unittest discover
```

### Hardware Testing

Before using the application on a wrist-mounted device, test:

- Display compatibility and resolution.
- Touchscreen responsiveness.
- Wi-Fi connectivity.
- Battery life.
- Charging and power management.
- Temperature under sustained use.
- Performance and stability.

Hardware-specific testing will be required once the final components are selected.

---

## 🛠️ Troubleshooting

### Problem: Tkinter Is Missing

Install Tkinter:

```bash
sudo apt install python3-tk -y
```

### Problem: Python Module Not Found

Verify that you are running the application from the correct directory.

Check the project files:

```bash
pwd
find . -type f -name "main.py"
find . -type f -name "security_tools.py"
```

Also verify that the Python imports match your directory structure.

### Problem: Application Does Not Start

Run the application from a terminal so that you can see error messages:

```bash
python3 main.py
```

Read the traceback and check the reported file and line number.

Avoid running the graphical application with `sudo` unless absolutely necessary.

### Problem: Network Diagnostics Fail

Check the network connection and confirm that the relevant network interface is available.

Some functions may depend on system utilities, permissions, or hardware support.

### Problem: Application Freezes

Long-running network operations should not block Tkinter's main event loop.

Use background threads where appropriate and update the interface safely from the main UI thread.

### Problem: GitHub Push Returns 403

A `403` error generally means GitHub is refusing write access with the credentials being used.

Check that:

- You are authenticated as the correct GitHub account.
- The repository URL is correct.
- Your token has access to the repository and `Contents: Read and write` permission, or your SSH key is configured correctly.
- Your GitHub account has write access to the repository.

You can also authenticate using GitHub CLI or SSH.

Never share GitHub tokens, passwords, or private SSH keys.

---

## 🔒 Security Considerations

OZIL SECURITY is intended for educational use, authorized system administration, and security testing.

The application should follow these security principles:

- Never execute untrusted commands.
- Validate user input before running system commands.
- Avoid unnecessary root privileges.
- Protect SSH keys, passwords, and API tokens.
- Test network services only with appropriate authorization.
- Use timeouts for network operations and subprocess calls.
- Handle invalid inputs and command failures safely.
- Avoid unsafe shell command construction.
- Keep dependencies and the operating system updated.
- Review command permissions carefully.

### Command Execution Safety

A terminal interface can execute powerful Linux commands. Quick-action buttons should be restricted to known, safe commands wherever possible.

Where practical, use argument lists with `subprocess.run()` rather than constructing shell command strings from user input. Avoid `shell=True` unless there is a specific, justified need and the input is controlled safely.

---

## 🎯 Development Roadmap

The following roadmap describes the project's development goals. Items should be marked complete only after implementation and testing.

### Software

- [x] Establish the project concept.
- [x] Begin developing the Python application.
- [x] Define a smartwatch-style visual direction.
- [ ] Complete the core user interface.
- [ ] Verify all diagnostic functions.
- [ ] Improve error handling.
- [ ] Strengthen command execution security.
- [ ] Add automated tests.
- [ ] Improve responsiveness on small displays.

### Hardware

- [ ] Select the computing board.
- [ ] Validate touchscreen compatibility.
- [ ] Finalize the power and battery design.
- [ ] Configure Linux for the target device.
- [ ] Integrate Wi-Fi and touchscreen support.
- [ ] Develop the wrist-mounted enclosure.
- [ ] Test power consumption and battery life.
- [ ] Test temperature and reliability.

### Documentation

- [x] Create the initial README.
- [ ] Document software architecture.
- [ ] Document hardware component selection.
- [ ] Write installation and configuration guides.
- [ ] Add real application screenshots.
- [ ] Document hardware assembly and troubleshooting.

---

## 📸 Screenshots

Screenshots will be added as development progresses.

Planned screenshots include:

- Main smartwatch interface.
- Application menu.
- Cybersecurity tools screen.
- Linux terminal interface.
- System information screen.

When a real screenshot is saved as `screenshots/watch-face.png`, display it in this section with:

```markdown
![OZIL SECURITY Watch Face](screenshots/watch-face.png)
```

Use actual screenshots from the running application rather than empty placeholder files.

---

## 🔮 Future Goals

Future development may include:

- Improved touchscreen navigation.
- A responsive interface for small displays.
- Additional network diagnostic utilities.
- Battery and temperature monitoring.
- Hardware integration.
- Linux startup automation.
- A custom wrist-mounted enclosure.
- Improved power efficiency.
- Expanded testing and documentation.

These are goals for future development and are not guaranteed features of the current implementation.

---

## 👨‍💻 Author

**GitHub:** [@sheikaabu11](https://github.com/sheikaabu11)

**Project Repository:** [OZIL SECURITY — Wearable Linux Cybersecurity Computer](https://github.com/sheikaabu11/Ozil-secuirty_wearable-linux)

---

## ⚠️ Disclaimer

OZIL SECURITY is an experimental wearable-computing project intended for learning, development, and authorized diagnostics.

It is not a substitute for professional security testing equipment or a comprehensive security audit. Features, hardware compatibility, and design decisions may change during development.

Use all network diagnostic and cybersecurity functions responsibly and only on systems you own or have permission to test.

---

## ⭐ Support the Project

If you find OZIL SECURITY interesting, consider starring the repository on GitHub.

Suggestions, constructive feedback, and contributions are welcome.

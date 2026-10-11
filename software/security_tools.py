import os
import platform
import shutil
import socket
import subprocess


# =========================================================
# OZIL SECURITY — CYBERSECURITY UTILITIES
# =========================================================

def run_command(args, timeout=5):
    """Execute a command without invoking a shell."""

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )

        if result.returncode == 0:
            return result.stdout.strip()

        return result.stderr.strip() or result.stdout.strip()

    except FileNotFoundError:
        return f"Command not found: {args[0]}"

    except subprocess.TimeoutExpired:
        return "Command timed out."

    except Exception as error:
        return f"Error: {error}"


# =========================================================
# NETWORK INTERFACES
# =========================================================

def get_network_interfaces():
    """Display available network interfaces."""

    if shutil.which("ip"):
        result = run_command(["ip", "-brief", "address"])

        if result:
            return result

    try:
        hostname = socket.gethostname()
        addresses = socket.getaddrinfo(hostname, None)

        unique_addresses = sorted({
            item[4][0] for item in addresses
        })

        return (
            f"Hostname: {hostname}\n\n"
            + "\n".join(unique_addresses)
        )

    except Exception as error:
        return f"Network error: {error}"


# =========================================================
# DNS LOOKUP
# =========================================================

def dns_lookup(hostname):
    """Resolve a hostname into IP addresses."""

    hostname = hostname.strip()

    if not hostname:
        return "Please enter a hostname."

    try:
        results = socket.getaddrinfo(hostname, None)

        addresses = sorted({
            item[4][0] for item in results
        })

        if not addresses:
            return "No addresses found."

        return (
            f"DNS LOOKUP\n"
            f"Hostname: {hostname}\n\n"
            + "\n".join(addresses)
        )

    except socket.gaierror as error:
        return f"DNS lookup failed:\n{error}"

    except Exception as error:
        return f"Error: {error}"


# =========================================================
# TCP PORT CONNECTIVITY CHECK
# =========================================================

def check_tcp_port(host, port, timeout=3):
    """Check whether a TCP connection can be established."""

    host = str(host).strip()

    try:
        port = int(port)
    except (TypeError, ValueError):
        return "Invalid port number."

    if not host:
        return "Please enter a hostname or IP address."

    if not 1 <= port <= 65535:
        return "Port must be between 1 and 65535."

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout
        ):
            return (
                "TCP CONNECTION SUCCESSFUL\n\n"
                f"Host: {host}\n"
                f"Port: {port}\n"
                "Status: Reachable"
            )

    except socket.timeout:
        return (
            f"Connection timed out.\n"
            f"Host: {host}\nPort: {port}"
        )

    except ConnectionRefusedError:
        return (
            f"Connection refused.\n"
            f"Host: {host}\nPort: {port}"
        )

    except OSError as error:
        return f"Connection failed:\n{error}"


# =========================================================
# SYSTEM INFORMATION
# =========================================================

def system_information():
    """Collect basic Linux system information."""

    info = [
        "SYSTEM INFORMATION",
        "",
        f"OS: {platform.system()}",
        f"Release: {platform.release()}",
        f"Architecture: {platform.machine()}",
        f"Python: {platform.python_version()}",
        f"Hostname: {socket.gethostname()}",
    ]

    if shutil.which("uptime"):
        uptime = run_command(["uptime", "-p"])

        if uptime:
            info.append(f"Uptime: {uptime}")

    if shutil.which("free"):
        memory = run_command(["free", "-h"])

        if memory:
            info.extend(["", "MEMORY", memory])

    if shutil.which("df"):
        disk = run_command(["df", "-h", "/"])

        if disk:
            info.extend(["", "DISK", disk])

    return "\n".join(info)


# =========================================================
# BATTERY STATUS
# =========================================================

def get_battery_status():
    """Read battery information from Linux."""

    power_supply = "/sys/class/power_supply"

    if not os.path.isdir(power_supply):
        return "N/A"

    try:
        for name in os.listdir(power_supply):

            directory = os.path.join(power_supply, name)

            type_path = os.path.join(directory, "type")
            capacity_path = os.path.join(directory, "capacity")
            status_path = os.path.join(directory, "status")

            try:
                with open(type_path, encoding="utf-8") as file:
                    supply_type = file.read().strip().lower()
            except OSError:
                continue

            if supply_type != "battery":
                continue

            try:
                with open(
                    capacity_path,
                    encoding="utf-8"
                ) as file:
                    capacity = file.read().strip()
            except OSError:
                capacity = "?"

            try:
                with open(
                    status_path,
                    encoding="utf-8"
                ) as file:
                    status = file.read().strip()
            except OSError:
                status = "Unknown"

            return f"{capacity}% | {status}"

        return "N/A"

    except Exception:
        return "N/A"


# =========================================================
# WI-FI STATUS
# =========================================================

def get_wifi_status():
    """Check Wi-Fi radio status using NetworkManager."""

    if not shutil.which("nmcli"):
        return "Unknown"

    result = run_command([
        "nmcli",
        "-t",
        "-f",
        "WIFI",
        "radio"
    ])

    if result == "enabled":
        return "Enabled"

    if result == "disabled":
        return "Disabled"

    return "Unknown"
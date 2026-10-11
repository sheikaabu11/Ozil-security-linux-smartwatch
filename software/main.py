import os
import queue
import subprocess
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from security_tools import (
    get_network_interfaces,
    dns_lookup,
    check_tcp_port,
    system_information,
    get_battery_status,
    get_wifi_status,
)

# =========================================================
# OZIL SECURITY — WEARABLE LINUX COMPUTER
# Designed for a compact 320 x 320 display
# =========================================================

WIDTH = 320
HEIGHT = 320

BG = "#080D12"
PANEL = "#101A22"
PANEL_2 = "#172630"
GREEN = "#42F5A1"
GREEN_DARK = "#173D30"
TEXT = "#EAF4F0"
MUTED = "#8DA39B"
RED = "#FF6B6B"

FONT = "DejaVu Sans"


class OzilSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OZIL SECURITY")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(WIDTH, HEIGHT)
        self.root.maxsize(WIDTH, HEIGHT)
        self.root.configure(bg=BG)

        self.working_directory = os.path.expanduser("~")
        self.command_history = []
        self.history_index = 0

        self.output_queue = queue.Queue()

        self.terminal_output = None
        self.terminal_entry = None
        self.terminal_status = None

        self.clock_label = None
        self.date_label = None
        self.battery_label = None
        self.wifi_label = None

        self.interface_text = None
        self.system_info_text = None

        self.show_home()

        self.root.after(100, self.process_output_queue)
        self.root.after(500, self.update_clock)

    # =====================================================
    # UI HELPERS
    # =====================================================

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        page = tk.Frame(self.root, bg=BG)
        page.pack(fill="both", expand=True)

        return page

    def title_bar(self, parent, title, back_command=None):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", padx=8, pady=(7, 4))

        if back_command:
            self.make_button(
                bar,
                "‹",
                back_command,
                font_size=14,
                width=2,
            ).pack(side="left", padx=(0, 7))

        tk.Label(
            bar,
            text=title,
            bg=BG,
            fg=GREEN,
            font=(FONT, 10, "bold"),
        ).pack(side="left")

        tk.Label(
            bar,
            text="● ONLINE",
            bg=BG,
            fg=MUTED,
            font=(FONT, 6, "bold"),
        ).pack(side="right")

    def make_button(
        self,
        parent,
        text,
        command,
        bg=PANEL_2,
        fg=TEXT,
        font_size=8,
        height=1,
        width=None,
    ):
        options = {
            "text": text,
            "command": command,
            "bg": bg,
            "fg": fg,
            "activebackground": GREEN_DARK,
            "activeforeground": TEXT,
            "relief": "flat",
            "bd": 0,
            "font": (FONT, font_size, "bold"),
            "cursor": "hand2",
            "padx": 4,
            "pady": 3,
        }

        if width is not None:
            options["width"] = width

        if height is not None:
            options["height"] = height

        return tk.Button(parent, **options)

    def make_text_box(self, parent, height=7):
        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground="#243842",
            highlightthickness=1,
        )

        text = tk.Text(
            frame,
            bg=PANEL,
            fg=TEXT,
            insertbackground=GREEN,
            selectbackground=GREEN_DARK,
            relief="flat",
            wrap="word",
            font=("DejaVu Sans Mono", 8),
            height=height,
            padx=5,
            pady=4,
        )

        scrollbar = tk.Scrollbar(
            frame,
            command=text.yview,
            width=7,
        )

        text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)

        return frame, text

    @staticmethod
    def one_line(value, limit=60):
        value = " ".join(str(value).split())

        if len(value) <= limit:
            return value

        return value[:limit - 1] + "…"

    # =====================================================
    # HOME — SMARTWATCH FACE
    # =====================================================

    def show_home(self):
        page = self.clear_page()

        header = tk.Frame(page, bg=BG)
        header.pack(fill="x", padx=12, pady=(12, 0))

        tk.Label(
            header,
            text="OZIL",
            bg=BG,
            fg=GREEN,
            font=(FONT, 12, "bold"),
        ).pack(side="left")

        tk.Label(
            header,
            text="SECURITY",
            bg=BG,
            fg=TEXT,
            font=(FONT, 8, "bold"),
        ).pack(side="left", padx=(5, 0), pady=(4, 0))

        tk.Label(
            header,
            text="LINUX WEARABLE",
            bg=BG,
            fg=MUTED,
            font=(FONT, 6),
        ).pack(side="right", pady=(5, 0))

        self.clock_label = tk.Label(
            page,
            text="--:--",
            bg=BG,
            fg=TEXT,
            font=(FONT, 38, "bold"),
        )
        self.clock_label.pack(pady=(16, 0))

        self.date_label = tk.Label(
            page,
            text="",
            bg=BG,
            fg=MUTED,
            font=(FONT, 9),
        )
        self.date_label.pack(pady=(0, 12))

        status = tk.Frame(
            page,
            bg=PANEL,
            padx=8,
            pady=7,
        )
        status.pack(fill="x", padx=12)

        self.wifi_label = tk.Label(
            status,
            text="Wi-Fi: checking...",
            bg=PANEL,
            fg=GREEN,
            font=(FONT, 7),
        )
        self.wifi_label.pack(side="left")

        self.battery_label = tk.Label(
            status,
            text="Battery: checking...",
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 7),
        )
        self.battery_label.pack(side="right")

        self.refresh_status_labels()

        self.make_button(
            page,
            "OPEN MENU  ›",
            self.show_menu,
            bg=GREEN_DARK,
            fg=GREEN,
            font_size=10,
        ).pack(fill="x", padx=12, pady=(17, 7))

        tk.Label(
            page,
            text="SECURE • COMPACT • LINUX",
            bg=BG,
            fg=MUTED,
            font=(FONT, 6),
        ).pack(side="bottom", pady=(0, 8))

    def update_clock(self):
        try:
            now = datetime.now()

            if self.clock_label and self.clock_label.winfo_exists():
                self.clock_label.config(
                    text=now.strftime("%H:%M")
                )

            if self.date_label and self.date_label.winfo_exists():
                self.date_label.config(
                    text=now.strftime("%a, %d %b %Y")
                )

        except tk.TclError:
            pass

        self.root.after(1000, self.update_clock)

    def safe_status_call(self, function):
        try:
            return function()
        except Exception as exc:
            return f"Unavailable: {exc}"

    def refresh_status_labels(self):
        wifi = self.safe_status_call(get_wifi_status)
        battery = self.safe_status_call(get_battery_status)

        if self.wifi_label and self.wifi_label.winfo_exists():
            self.wifi_label.config(
                text=f"Wi-Fi: {self.one_line(wifi, 22)}"
            )

        if self.battery_label and self.battery_label.winfo_exists():
            self.battery_label.config(
                text=f"BAT: {self.one_line(battery, 22)}"
            )

    # =====================================================
    # APP MENU
    # =====================================================

    def show_menu(self):
        page = self.clear_page()

        self.title_bar(page, "APP MENU", self.show_home)

        tk.Label(
            page,
            text="Choose a tool",
            bg=BG,
            fg=MUTED,
            font=(FONT, 8),
        ).pack(anchor="w", padx=12, pady=(0, 7))

        menu_items = [
            (
                "LINUX TERMINAL",
                "Run Linux commands",
                self.show_terminal,
            ),
            (
                "CYBER MODE",
                "DNS, TCP ports, interfaces",
                self.show_cyber_mode,
            ),
            (
                "SYSTEM INFO",
                "Device and OS details",
                self.show_system_info,
            ),
            (
                "ABOUT OZIL",
                "Project information",
                self.show_about,
            ),
        ]

        for label, subtitle, command in menu_items:
            card = tk.Frame(
                page,
                bg=PANEL,
                padx=8,
                pady=6,
            )
            card.pack(fill="x", padx=10, pady=3)

            text_frame = tk.Frame(card, bg=PANEL)
            text_frame.pack(side="left", fill="x", expand=True)

            tk.Label(
                text_frame,
                text=label,
                bg=PANEL,
                fg=GREEN,
                font=(FONT, 8, "bold"),
            ).pack(anchor="w")

            tk.Label(
                text_frame,
                text=subtitle,
                bg=PANEL,
                fg=MUTED,
                font=(FONT, 6),
            ).pack(anchor="w", pady=(2, 0))

            self.make_button(
                card,
                "OPEN ›",
                command,
                font_size=7,
            ).pack(side="right")

    # =====================================================
    # LINUX TERMINAL
    # =====================================================

    def show_terminal(self):
        page = self.clear_page()

        self.title_bar(
            page,
            "LINUX TERMINAL",
            self.show_menu,
        )

        status_row = tk.Frame(page, bg=BG)
        status_row.pack(fill="x", padx=8, pady=(0, 3))

        tk.Label(
            status_row,
            text="USER SHELL",
            bg=BG,
            fg=MUTED,
            font=(FONT, 6, "bold"),
        ).pack(side="left")

        self.terminal_status = tk.Label(
            status_row,
            text=self.one_line(self.working_directory, 30),
            bg=BG,
            fg=GREEN,
            font=(FONT, 6),
        )
        self.terminal_status.pack(side="right")

        output_frame, self.terminal_output = self.make_text_box(
            page,
            height=6,
        )
        output_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 4),
        )

        self.terminal_output.insert(
            "end",
            "OZIL shell ready.\n"
            "Tap a button or enter a command.\n\n"
        )
        self.terminal_output.insert(
            "end",
            f"Directory: {self.working_directory}\n",
        )
        self.terminal_output.configure(state="disabled")

        # Eight touchscreen command buttons.
        button_frame = tk.Frame(page, bg=BG)
        button_frame.pack(fill="x", padx=7, pady=(0, 4))

        quick_commands = [
            ("LS", "ls"),
            ("PWD", "pwd"),
            ("WHOAMI", "whoami"),
            ("IP", "ip addr"),
            ("PING", "ping -c 2 example.com"),
            ("DNS", "getent hosts example.com"),
            ("PORT", "nc -z -w 3 example.com 443"),
            ("CLEAR", "__CLEAR__"),
        ]

        for index, (label, command) in enumerate(quick_commands):
            row, col = divmod(index, 4)

            is_special = label in ("IP", "DNS", "PORT", "CLEAR")

            button = self.make_button(
                button_frame,
                label,
                lambda cmd=command: self.run_terminal_quick_command(cmd),
                bg=GREEN_DARK if label == "CLEAR" else PANEL_2,
                fg=GREEN if is_special else TEXT,
                font_size=7,
                height=1,
            )

            button.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=2,
                pady=2,
            )

            button_frame.grid_columnconfigure(
                col,
                weight=1,
                uniform="quick",
            )

        # Terminal input and RUN button.
        input_row = tk.Frame(page, bg=BG)
        input_row.pack(fill="x", padx=8, pady=(0, 7))

        self.terminal_entry = tk.Entry(
            input_row,
            bg=PANEL,
            fg=TEXT,
            insertbackground=GREEN,
            relief="flat",
            font=("DejaVu Sans Mono", 8),
        )
        self.terminal_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=5,
        )

        self.terminal_entry.bind(
            "<Return>",
            self.run_terminal_command,
        )
        self.terminal_entry.bind(
            "<Up>",
            self.history_up,
        )
        self.terminal_entry.bind(
            "<Down>",
            self.history_down,
        )

        self.make_button(
            input_row,
            "RUN",
            self.run_terminal_command,
            bg=GREEN_DARK,
            fg=GREEN,
            font_size=7,
        ).pack(side="right", padx=(4, 0))

        self.terminal_entry.focus_set()

    def run_terminal_quick_command(self, command):
        if command == "__CLEAR__":
            if self.terminal_output and self.terminal_output.winfo_exists():
                self.terminal_output.configure(state="normal")
                self.terminal_output.delete("1.0", "end")
                self.terminal_output.insert(
                    "end",
                    "OZIL shell cleared.\n",
                )
                self.terminal_output.configure(state="disabled")
            return

        if not self.terminal_entry or not self.terminal_entry.winfo_exists():
            return

        self.terminal_entry.delete(0, "end")
        self.terminal_entry.insert(0, command)

        self.run_terminal_command()

    def append_terminal(self, text):
        if not self.terminal_output:
            return

        try:
            if not self.terminal_output.winfo_exists():
                return

            self.terminal_output.configure(state="normal")
            self.terminal_output.insert("end", str(text))
            self.terminal_output.see("end")
            self.terminal_output.configure(state="disabled")

        except tk.TclError:
            pass

    def run_terminal_command(self, event=None):
        if not self.terminal_entry:
            return "break"

        command = self.terminal_entry.get().strip()

        if not command:
            return "break"

        self.terminal_entry.delete(0, "end")

        self.command_history.append(command)
        self.history_index = len(self.command_history)

        self.append_terminal(f"\n$ {command}\n")

        # Built-in commands.
        if command.lower() in ("clear", "cls"):
            if self.terminal_output:
                self.terminal_output.configure(state="normal")
                self.terminal_output.delete("1.0", "end")
                self.terminal_output.configure(state="disabled")
            return "break"

        if command == "exit":
            self.show_menu()
            return "break"

        if command == "help":
            self.append_terminal(
                "Available commands:\n"
                "ls, pwd, whoami, ip addr, ping,\n"
                "getent, nc, cd, clear, help, exit\n"
            )
            return "break"

        if command == "pwd":
            self.append_terminal(self.working_directory + "\n")
            return "break"

        if command == "cd" or command.startswith("cd "):
            target = command[2:].strip()

            if not target or target == "~":
                target = os.path.expanduser("~")
            elif target == "-":
                target = os.path.expanduser("~")
            elif not os.path.isabs(target):
                target = os.path.join(
                    self.working_directory,
                    target,
                )

            target = os.path.abspath(os.path.expanduser(target))

            if os.path.isdir(target):
                self.working_directory = target
                self.update_terminal_directory()
                self.append_terminal(
                    f"Changed directory to {target}\n"
                )
            else:
                self.append_terminal(
                    f"cd: no such directory: {target}\n"
                )

            return "break"

        # Run commands in the background so the UI stays responsive.
        threading.Thread(
            target=self.execute_terminal_command,
            args=(command,),
            daemon=True,
        ).start()

        return "break"

    def execute_terminal_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )

            output = result.stdout or ""

            if result.stderr:
                output += result.stderr

            if not output.strip():
                output = (
                    f"Command finished with exit code "
                    f"{result.returncode}.\n"
                )
            elif not output.endswith("\n"):
                output += "\n"

            self.output_queue.put(output)

        except subprocess.TimeoutExpired:
            self.output_queue.put(
                "Command timed out after 15 seconds.\n"
            )

        except Exception as exc:
            self.output_queue.put(f"Error: {exc}\n")

    def update_terminal_directory(self):
        if self.terminal_status and self.terminal_status.winfo_exists():
            self.terminal_status.config(
                text=self.one_line(self.working_directory, 30)
            )

    def history_up(self, event=None):
        if self.command_history and self.terminal_entry:
            self.history_index = max(
                0,
                self.history_index - 1,
            )

            self.terminal_entry.delete(0, "end")
            self.terminal_entry.insert(
                0,
                self.command_history[self.history_index],
            )

        return "break"

    def history_down(self, event=None):
        if self.terminal_entry and self.command_history:
            self.history_index = min(
                len(self.command_history),
                self.history_index + 1,
            )

            self.terminal_entry.delete(0, "end")

            if self.history_index < len(self.command_history):
                self.terminal_entry.insert(
                    0,
                    self.command_history[self.history_index],
                )

        return "break"

    # =====================================================
    # CYBER MODE
    # =====================================================

    def show_cyber_mode(self):
        page = self.clear_page()

        self.title_bar(
            page,
            "CYBER MODE",
            self.show_menu,
        )

        tk.Label(
            page,
            text="NETWORK DIAGNOSTICS",
            bg=BG,
            fg=MUTED,
            font=(FONT, 7, "bold"),
        ).pack(anchor="w", padx=10, pady=(0, 5))

        # DNS lookup.
        panel = tk.Frame(
            page,
            bg=PANEL,
            padx=8,
            pady=7,
        )
        panel.pack(fill="x", padx=8, pady=3)

        tk.Label(
            panel,
            text="DNS LOOKUP",
            bg=PANEL,
            fg=GREEN,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w")

        dns_row = tk.Frame(panel, bg=PANEL)
        dns_row.pack(fill="x", pady=(4, 0))

        dns_entry = tk.Entry(
            dns_row,
            bg=BG,
            fg=TEXT,
            insertbackground=GREEN,
            relief="flat",
            font=(FONT, 8),
        )
        dns_entry.insert(0, "example.com")
        dns_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=4,
        )

        self.make_button(
            dns_row,
            "LOOKUP",
            lambda: self.run_cyber_action(
                "DNS lookup",
                lambda: dns_lookup(dns_entry.get().strip()),
            ),
            font_size=6,
        ).pack(side="right", padx=(4, 0))

        # TCP port check.
        panel2 = tk.Frame(
            page,
            bg=PANEL,
            padx=8,
            pady=7,
        )
        panel2.pack(fill="x", padx=8, pady=3)

        tk.Label(
            panel2,
            text="TCP PORT CHECK",
            bg=PANEL,
            fg=GREEN,
            font=(FONT, 8, "bold"),
        ).pack(anchor="w")

        port_row = tk.Frame(panel2, bg=PANEL)
        port_row.pack(fill="x", pady=(4, 0))

        host_entry = tk.Entry(
            port_row,
            bg=BG,
            fg=TEXT,
            insertbackground=GREEN,
            relief="flat",
            font=(FONT, 8),
        )
        host_entry.insert(0, "example.com")
        host_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=4,
        )

        port_entry = tk.Entry(
            port_row,
            bg=BG,
            fg=TEXT,
            insertbackground=GREEN,
            relief="flat",
            width=5,
            font=(FONT, 8),
        )
        port_entry.insert(0, "443")
        port_entry.pack(side="left", padx=(4, 0), ipady=4)

        self.make_button(
            port_row,
            "CHECK",
            lambda: self.check_port_action(
                host_entry.get().strip(),
                port_entry.get().strip(),
            ),
            font_size=6,
        ).pack(side="right", padx=(4, 0))

        self.make_button(
            page,
            "SHOW NETWORK INTERFACES",
            self.show_interfaces,
            font_size=7,
        ).pack(fill="x", padx=8, pady=4)

        self.make_button(
            page,
            "BACK TO MENU",
            self.show_menu,
            bg=GREEN_DARK,
            fg=GREEN,
            font_size=7,
        ).pack(fill="x", padx=8, pady=3)

    def run_cyber_action(self, title, action):
        try:
            result = action()
            messagebox.showinfo(
                title,
                str(result),
                parent=self.root,
            )
        except Exception as exc:
            messagebox.showerror(
                title,
                str(exc),
                parent=self.root,
            )

    def check_port_action(self, host, port_text):
        if not host:
            messagebox.showwarning(
                "TCP port check",
                "Enter a hostname or IP address.",
                parent=self.root,
            )
            return

        try:
            port = int(port_text)

            if not 1 <= port <= 65535:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "TCP port check",
                "Port must be from 1 to 65535.",
                parent=self.root,
            )
            return

        self.run_cyber_action(
            "TCP port check",
            lambda: check_tcp_port(host, port),
        )

    def show_interfaces(self):
        page = self.clear_page()

        self.title_bar(
            page,
            "NETWORK INTERFACES",
            self.show_cyber_mode,
        )

        box_frame, box = self.make_text_box(page, height=15)
        box_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5,
        )

        box.insert("end", "Loading network interfaces...\n")
        box.configure(state="disabled")

        self.interface_text = box

        def worker():
            try:
                result = get_network_interfaces()
            except Exception as exc:
                result = f"Could not read interfaces: {exc}"

            self.output_queue.put(("interfaces", result))

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    def show_system_info(self):
        page = self.clear_page()

        self.title_bar(
            page,
            "SYSTEM INFO",
            self.show_menu,
        )

        box_frame, box = self.make_text_box(page, height=14)
        box_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5,
        )

        box.insert("end", "Collecting system information...\n")
        box.configure(state="disabled")

        self.system_info_text = box

        def worker():
            try:
                info = system_information()
            except Exception as exc:
                info = f"Could not read system information: {exc}"

            try:
                battery = get_battery_status()
            except Exception as exc:
                battery = f"Unavailable: {exc}"

            try:
                wifi = get_wifi_status()
            except Exception as exc:
                wifi = f"Unavailable: {exc}"

            result = (
                f"SYSTEM INFORMATION\n\n{info}\n\n"
                f"BATTERY\n{battery}\n\n"
                f"WI-FI\n{wifi}"
            )

            self.output_queue.put(("system_info", result))

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    # =====================================================
    # ABOUT
    # =====================================================

    def show_about(self):
        page = self.clear_page()

        self.title_bar(
            page,
            "ABOUT OZIL",
            self.show_menu,
        )

        card = tk.Frame(
            page,
            bg=PANEL,
            padx=12,
            pady=12,
        )
        card.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8,
        )

        tk.Label(
            card,
            text="OZIL SECURITY",
            bg=PANEL,
            fg=GREEN,
            font=(FONT, 13, "bold"),
        ).pack(anchor="w", pady=(2, 8))

        description = (
            "A compact Linux wearable concept for system monitoring "
            "and basic network diagnostics.\n\n"
            "Features include a Linux terminal, DNS lookup, TCP port "
            "checks, network interface details, battery status and "
            "Wi-Fi status.\n\n"
            "Only test systems and networks you are authorized to use."
        )

        tk.Label(
            card,
            text=description,
            bg=PANEL,
            fg=TEXT,
            justify="left",
            wraplength=265,
            font=(FONT, 8),
        ).pack(anchor="w")

    # =====================================================
    # OUTPUT QUEUE
    # =====================================================

    def process_output_queue(self):
        try:
            while True:
                item = self.output_queue.get_nowait()

                if isinstance(item, tuple):
                    kind, result = item

                    if kind == "interfaces":
                        widget = self.interface_text
                    elif kind == "system_info":
                        widget = self.system_info_text
                    else:
                        widget = None

                    if widget and widget.winfo_exists():
                        widget.configure(state="normal")
                        widget.delete("1.0", "end")
                        widget.insert("end", str(result))
                        widget.see("1.0")
                        widget.configure(state="disabled")

                else:
                    self.append_terminal(item)

        except queue.Empty:
            pass

        self.root.after(
            100,
            self.process_output_queue,
        )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

def main():
    root = tk.Tk()
    OzilSecurityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
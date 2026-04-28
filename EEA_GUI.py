import ttkbootstrap as ttk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import json
import os

STX = 0xFE
ETX = 0xEF

LANG = {
    "ko": {
        "title": "E220 LoRa 설정 GUI",
        "ready": "⏳ 준비됨",
        "conn": "✅ 포트 연결됨",
        "disconn": "🔌 포트 미연결",
        "sent": "✅ 전송 완료:",
        "error": "❌ 오류:",
        "warning_port": "COM 포트를 선택해주세요.",
        "info_sent": "설정 패킷 전송:\n",
        "config_saved": "설정 저장 완료!",
        "config_loaded": "설정 불러옴",
        "failed_load": "⚠️ 설정파일 없음(최초실행)",

        # UI 텍스트
        "label_port": "COM 포트",
        "label_channel": "채널 (1~80)",
        "label_baud": "보드레이트",
        "label_air": "에어레이트",
        "label_addh": "ADDH (상위 주소)",
        "label_addl": "ADDL (하위 주소)",
        "btn_connect": "포트 연결",
        "btn_disconnect": "포트 해제",
        "btn_send": "설정 전송",
        "btn_save": "설정 저장",
        "btn_load": "설정 불러오기",
        "log_title": "전송 로그 / Log",
        "menu_option": "옵션",
        "menu_theme": "🌗 테마 전환(Theme)",
        "menu_language": "언어(Language)",
        "menu_ko": "한국어",
        "menu_en": "English",
    },
    "en": {
        "title": "E220 LoRa Configurator",
        "ready": "⏳ Ready",
        "conn": "✅ Port connected",
        "disconn": "🔌 Port not connected",
        "sent": "✅ Sent:",
        "error": "❌ Error:",
        "warning_port": "Please choose a COM port.",
        "info_sent": "Packet sent:\n",
        "config_saved": "Config saved!",
        "config_loaded": "Config loaded",
        "failed_load": "⚠️ No config file",

        # UI texts
        "label_port": "COM Port",
        "label_channel": "Channel (1~80)",
        "label_baud": "Baud Rate",
        "label_air": "Air Rate",
        "label_addh": "ADDH (High Addr.)",
        "label_addl": "ADDL (Low Addr.)",
        "btn_connect": "Connect Port",
        "btn_disconnect": "Disconnect Port",
        "btn_send": "Send Config",
        "btn_save": "Save Config",
        "btn_load": "Load Config",
        "log_title": "Send Log / Log",
        "menu_option": "Options",
        "menu_theme": "🌗 Toggle Theme",
        "menu_language": "Language",
        "menu_ko": "Korean",
        "menu_en": "English",
    }
}

CONFIG_FILE = "config.json"

class E220Configurator(ttk.Window):
    def __init__(self):
        self.lang = "ko"
        self.strings = LANG[self.lang]
        self.current_theme = "darkly"
        super().__init__(title=self.strings["title"], themename=self.current_theme, size=(520, 620))
        self.resizable(True, True)

        self.ser = None

        self.channel_var = ttk.IntVar(value=1)
        self.selected_port = ttk.StringVar()
        self.baud_rates = [4800, 9600, 19200, 38400, 57600, 115200]
        self.air_rates = [
            "0.3 kbps", "1.2 kbps", "2.4 kbps", "4.8 kbps",
            "9.6 kbps", "19.2 kbps", "38.4 kbps", "62.5 kbps"
        ]
        self.selected_baud = ttk.StringVar(value=str(self.baud_rates[1]))
        self.selected_air = ttk.StringVar(value=self.air_rates[4])
        self.selected_addh = ttk.StringVar(value="00")
        self.selected_addl = ttk.StringVar(value="01")

        self.create_menu()
        self.create_widgets()
        self.load_config()
        self.refresh_ports()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if self.selected_port.get():
            self.connect_port()

    def create_menu(self):
        menubar = ttk.Menu(self)
        option_menu = ttk.Menu(menubar, tearoff=0)
        option_menu.add_command(label=self.strings["menu_theme"], command=self.toggle_theme)
        lang_menu = ttk.Menu(option_menu, tearoff=0)
        lang_menu.add_command(label=self.strings["menu_ko"], command=lambda: self.set_language("ko"))
        lang_menu.add_command(label=self.strings["menu_en"], command=lambda: self.set_language("en"))
        option_menu.add_cascade(label=self.strings["menu_language"], menu=lang_menu)
        menubar.add_cascade(label=self.strings["menu_option"], menu=option_menu)
        self.config(menu=menubar)
        self.menubar = menubar
        self.option_menu = option_menu
        self.lang_menu = lang_menu

    def create_widgets(self):
        padding = {"padx": 10, "pady": 6}

        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew", columnspan=4)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ttk.Label(main_frame, text=self.strings["title"], font=("Malgun Gothic", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=3, pady=3)

        param_frame = ttk.Labelframe(main_frame, text="설정", padding=8, bootstyle="primary")
        param_frame.grid(row=1, column=0, sticky="ew", columnspan=4, pady=(5, 0))

        self.label_port = ttk.Label(param_frame, text=self.strings["label_port"])
        self.label_port.grid(row=0, column=0, sticky="w", **padding)
        self.port_menu = ttk.Combobox(param_frame, textvariable=self.selected_port, bootstyle="dark", width=18)
        self.port_menu.grid(row=0, column=1, sticky="ew", **padding)
        self.btn_refresh_ports = ttk.Button(param_frame, text="새로고침", command=self.refresh_ports, bootstyle="secondary")
        self.btn_refresh_ports.grid(row=0, column=2, **padding)

        self.label_channel = ttk.Label(param_frame, text=self.strings["label_channel"])
        self.label_channel.grid(row=1, column=0, sticky="w", **padding)
        self.channel_spin = ttk.Spinbox(param_frame, from_=1, to=80, textvariable=self.channel_var,
                                        width=10, bootstyle="dark")
        self.channel_spin.grid(row=1, column=1, sticky="w", **padding)

        self.label_baud = ttk.Label(param_frame, text=self.strings["label_baud"])
        self.label_baud.grid(row=2, column=0, sticky="w", **padding)
        self.baud_menu = ttk.Combobox(param_frame, textvariable=self.selected_baud, values=[str(b) for b in self.baud_rates],
                                     bootstyle="dark", width=18)
        self.baud_menu.grid(row=2, column=1, sticky="ew", **padding)

        self.label_air = ttk.Label(param_frame, text=self.strings["label_air"])
        self.label_air.grid(row=3, column=0, sticky="w", **padding)
        self.air_menu = ttk.Combobox(param_frame, textvariable=self.selected_air, values=self.air_rates,
                                    bootstyle="dark", width=18)
        self.air_menu.grid(row=3, column=1, sticky="ew", **padding)

        self.label_addh = ttk.Label(param_frame, text=self.strings["label_addh"])
        self.label_addh.grid(row=4, column=0, sticky="w", **padding)
        address_values = [f"{i:02X}" for i in range(256)]
        self.addh_menu = ttk.Combobox(param_frame, textvariable=self.selected_addh, values=address_values,
                                     bootstyle="dark", width=18)
        self.addh_menu.grid(row=4, column=1, sticky="ew", **padding)

        self.label_addl = ttk.Label(param_frame, text=self.strings["label_addl"])
        self.label_addl.grid(row=5, column=0, sticky="w", **padding)
        self.addl_menu = ttk.Combobox(param_frame, textvariable=self.selected_addl, values=address_values,
                                     bootstyle="dark", width=18)
        self.addl_menu.grid(row=5, column=1, sticky="ew", **padding)

        btn_frame = ttk.Frame(param_frame)
        btn_frame.grid(row=6, column=0, columnspan=4, pady=(8, 0))
        self.connect_btn = ttk.Button(btn_frame, text=self.strings["btn_connect"], command=self.connect_port, bootstyle="success")
        self.connect_btn.grid(row=0, column=0, padx=5)
        self.disconnect_btn = ttk.Button(btn_frame, text=self.strings["btn_disconnect"], command=self.disconnect_port, bootstyle="danger")
        self.disconnect_btn.grid(row=0, column=1, padx=5)

        ttk.Separator(main_frame, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky="ew", pady=8)

        cmd_frame = ttk.Frame(main_frame)
        cmd_frame.grid(row=3, column=0, columnspan=4, sticky="ew")

        self.send_btn = ttk.Button(cmd_frame, text=self.strings["btn_send"], command=self.send_packet, bootstyle="success")
        self.send_btn.grid(row=0, column=0, pady=8, ipadx=10, ipady=4)
        self.save_btn = ttk.Button(cmd_frame, text=self.strings["btn_save"], command=self.save_config, bootstyle="info")
        self.save_btn.grid(row=0, column=1, padx=8, ipadx=5)
        self.load_btn = ttk.Button(cmd_frame, text=self.strings["btn_load"], command=self.load_config, bootstyle="warning")
        self.load_btn.grid(row=0, column=2, ipadx=5)

        self.log_label = ttk.Label(main_frame, text=self.strings["log_title"])
        self.log_label.grid(row=4, column=0, sticky="w", pady=(10, 0))

        self.log_box = ttk.Text(main_frame, height=12, width=62, font=("Consolas", 10), wrap="none")
        self.log_box.grid(row=5, column=0, columnspan=3, padx=4, pady=3, sticky="nsew")
        self.log_box.config(state="disabled")

        self.log_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_box.yview)
        self.log_scrollbar.grid(row=5, column=3, sticky="ns", pady=3)
        self.log_box.config(yscrollcommand=self.log_scrollbar.set)

        self.status_var = ttk.StringVar(value=self.strings["ready"])
        self.status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w", bootstyle="secondary")
        self.status_bar.grid(row=9, column=0, columnspan=4, sticky="ew")

    def set_language(self, lang):
        self.lang = lang
        self.strings = LANG[self.lang]
        self.title(self.strings["title"])
        self.status_var.set(self.strings["ready"])

        # 메뉴 텍스트 변경
        self.option_menu.entryconfig(0, label=self.strings["menu_theme"])
        self.option_menu.entryconfig(1, label=self.strings["menu_language"])
        self.lang_menu.entryconfig(0, label=self.strings["menu_ko"])
        self.lang_menu.entryconfig(1, label=self.strings["menu_en"])

        # UI 텍스트 변경
        self.title_label.config(text=self.strings["title"])
        self.label_port.config(text=self.strings["label_port"])
        self.label_channel.config(text=self.strings["label_channel"])
        self.label_baud.config(text=self.strings["label_baud"])
        self.label_air.config(text=self.strings["label_air"])
        self.label_addh.config(text=self.strings["label_addh"])
        self.label_addl.config(text=self.strings["label_addl"])
        self.connect_btn.config(text=self.strings["btn_connect"])
        self.disconnect_btn.config(text=self.strings["btn_disconnect"])
        self.send_btn.config(text=self.strings["btn_send"])
        self.save_btn.config(text=self.strings["btn_save"])
        self.load_btn.config(text=self.strings["btn_load"])
        self.log_label.config(text=self.strings["log_title"])

    def toggle_theme(self):
        if self.current_theme == "darkly":
            self.current_theme = "flatly"
        else:
            self.current_theme = "darkly"

        self.style.theme_use(self.current_theme)
        style = "dark" if self.current_theme == "darkly" else "secondary"
        self.port_menu.config(bootstyle=style)
        self.baud_menu.config(bootstyle=style)
        self.air_menu.config(bootstyle=style)
        self.channel_spin.config(bootstyle=style)
        self.addh_menu.config(bootstyle=style)
        self.addl_menu.config(bootstyle=style)
        self.connect_btn.config(bootstyle="success")
        self.disconnect_btn.config(bootstyle="danger")
        self.send_btn.config(bootstyle="success")
        self.save_btn.config(bootstyle="info")
        self.load_btn.config(bootstyle="warning")

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports] or []
        self.port_menu['values'] = port_list
        if port_list:
            if not self.selected_port.get() or self.selected_port.get() not in port_list:
                self.selected_port.set(port_list[0])
            if self.ser and self.ser.is_open:
                self.status_var.set(self.strings["conn"])
            else:
                self.status_var.set(self.strings["disconn"])
        else:
            self.selected_port.set("")
            self.status_var.set(self.strings["disconn"])

    def log_message(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def make_packet(self):
        try:
            addh = int(self.selected_addh.get(), 16)
        except Exception:
            addh = 0x00
        try:
            addl = int(self.selected_addl.get(), 16)
        except Exception:
            addl = 0x01
        channel = max(1, min(80, self.channel_var.get()))

        fixed_mode_prefix = [addh, addl, channel]
        try:
            src = int(self.selected_addh.get(), 16)
        except Exception:
            src = 0x00
        dst = addl
        blk = 0x01
        cmd = 0x10
        air_rate_idx = self.air_rates.index(self.selected_air.get()) & 0x07
        data = [air_rate_idx, channel]
        length = len(data)

        packet_body = [STX, src, dst, blk, cmd, length] + data
        checksum = sum(packet_body) & 0xFF
        packet = fixed_mode_prefix + packet_body + [checksum, ETX]
        return packet

    def connect_port(self):
        port = self.selected_port.get()
        if not port:
            messagebox.showwarning(self.strings["warning_port"], self.strings["warning_port"])
            self.status_var.set(self.strings["disconn"])
            return

        baud = self.selected_baud.get()
        try:
            if self.ser:
                if self.ser.is_open:
                    self.ser.close()
                self.ser = None

            self.ser = serial.Serial(port, baudrate=int(baud), timeout=1)
            self.status_var.set(self.strings["conn"])
            self.log_message(f"🔌 {self.strings['conn']}: {port} @ {baud}bps")

        except Exception as e:
            self.ser = None
            self.status_var.set(self.strings["disconn"])
            self.log_message(f"{self.strings['error']} {e}")
            messagebox.showerror(self.strings["error"], str(e))

    def disconnect_port(self):
        if self.ser:
            try:
                self.ser.close()
                self.log_message(f"🔌 {self.strings['disconn']}: {self.ser.port}")
            except Exception as e:
                self.log_message(f"{self.strings['error']} 포트 해제 오류: {e}")
            finally:
                self.ser = None
                self.status_var.set(self.strings["disconn"])

    def send_packet(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning(self.strings["warning_port"], self.strings["disconn"])
            self.status_var.set(self.strings["disconn"])
            return

        try:
            packet = self.make_packet()
            self.ser.write(bytearray(packet))
            hex_str = " ".join(f"{b:02X}" for b in packet)
            self.log_message(f"{self.strings['sent']} {hex_str}")
            self.status_var.set(self.strings["sent"])
            messagebox.showinfo(self.strings["sent"], f"{self.strings['info_sent']}{hex_str}")

        except serial.SerialException as e:
            self.status_var.set(self.strings["disconn"])
            self.log_message(f"{self.strings['error']} {e}")
            messagebox.showerror(self.strings["error"], f"Serial Error: {e}")
        except Exception as e:
            self.status_var.set(f"{self.strings['error']} {e}")
            self.log_message(f"{self.strings['error']} {e}")
            messagebox.showerror(self.strings["error"], f"Error: {e}")

    def save_config(self):
        config = {
            "port": self.selected_port.get(),
            "baud": self.selected_baud.get(),
            "channel": self.channel_var.get(),
            "air": self.selected_air.get(),
            "addh": self.selected_addh.get(),
            "addl": self.selected_addl.get(),
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f)
            messagebox.showinfo(self.strings["config_saved"], self.strings["config_saved"])
            self.log_message("⚡ 설정 저장: " + str(config))
        except Exception as e:
            messagebox.showerror(self.strings["error"], str(e))
            self.log_message(f"❌ 저장 오류: {e}")

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.status_var.set(self.strings["failed_load"])
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                self.selected_port.set(cfg.get("port", ""))
                self.selected_baud.set(str(cfg.get("baud", "9600")))
                self.channel_var.set(cfg.get("channel", 1))
                self.selected_air.set(cfg.get("air", self.air_rates[4]))
                self.selected_addh.set(cfg.get("addh", "00"))
                self.selected_addl.set(cfg.get("addl", "01"))
            self.status_var.set(self.strings["config_loaded"])
            self.log_message("✅ 설정 불러오기 완료")
        except Exception as e:
            messagebox.showerror(self.strings["error"], str(e))
            self.log_message(f"❌ 불러오기 오류: {e}")

    def on_closing(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except:
                pass
            self.ser = None
        self.destroy()

if __name__ == "__main__":
    app = E220Configurator()
    app.mainloop()
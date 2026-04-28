import customtkinter as ctk
from deep_translator import GoogleTranslator
import threading

# 테마 설정
ctk.set_appearance_mode("dark")  # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "dark-blue", "green"

class ModernTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 Google 번역기")
        self.root.geometry("700x750")
        self.root.resizable(True, True)
        self.root.minsize(600, 600)
        
        # 메인 프레임
        main_frame = ctk.CTkFrame(root, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 제목
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌍 Google 번역기",
            font=("Segoe UI", 24, "bold"),
            text_color=("#0066CC", "#00CCFF")
        )
        title_label.pack(pady=(0, 20))
        
        # 부제목
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="한국어 ↔ 영어 자동 감지 번역",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # 입력 섹션
        input_label = ctk.CTkLabel(
            main_frame,
            text="원문 입력",
            font=("Segoe UI", 14, "bold")
        )
        input_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.txt_input = ctk.CTkTextbox(
            main_frame,
            height=120,
            corner_radius=8,
            border_width=2,
            border_color="#0066CC",
            font=("Segoe UI", 11)
        )
        self.txt_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 버튼 프레임
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=10)
        
        # 한 -> 영
        btn_ko_en = ctk.CTkButton(
            btn_frame,
            text="🇰🇷 한국어 → 🇺🇸 영어",
            command=lambda: self.translate_async("en"),
            font=("Segoe UI", 12, "bold"),
            height=40,
            corner_radius=8
        )
        btn_ko_en.pack(side="left", fill="x", expand=True, padx=5)
        
        # 영 -> 한
        btn_en_ko = ctk.CTkButton(
            btn_frame,
            text="🇺🇸 영어 → 🇰🇷 한국어",
            command=lambda: self.translate_async("ko"),
            font=("Segoe UI", 12, "bold"),
            height=40,
            corner_radius=8,
            fg_color="#28a745"
        )
        btn_en_ko.pack(side="left", fill="x", expand=True, padx=5)
        
        # 결과 섹션
        output_label = ctk.CTkLabel(
            main_frame,
            text="번역 결과",
            font=("Segoe UI", 14, "bold")
        )
        output_label.pack(anchor="w", padx=10, pady=(15, 5))
        
        self.txt_output = ctk.CTkTextbox(
            main_frame,
            height=120,
            corner_radius=8,
            border_width=2,
            border_color="#28a745",
            font=("Segoe UI", 11)
        )
        self.txt_output.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 상태 레이블
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="준비 완료",
            font=("Segoe UI", 10),
            text_color="gray"
        )
        self.status_label.pack(pady=10)
        
        # 복사 버튼 프레임
        copy_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        copy_frame.pack(pady=10, fill="x", padx=10)
        
        copy_btn = ctk.CTkButton(
            copy_frame,
            text="📋 결과 복사",
            command=self.copy_result,
            font=("Segoe UI", 11, "bold"),
            width=150,
            height=35,
            corner_radius=8,
            fg_color="#555555"
        )
        copy_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            copy_frame,
            text="🗑️ 초기화",
            command=self.clear_all,
            font=("Segoe UI", 11, "bold"),
            width=150,
            height=35,
            corner_radius=8,
            fg_color="#555555"
        )
        clear_btn.pack(side="left", padx=5)
    
    def translate_async(self, target_lang):
        """비동기로 번역 실행"""
        self.status_label.configure(text="번역 중... ⏳")
        self.root.update()
        
        thread = threading.Thread(target=self.translate, args=(target_lang,))
        thread.daemon = True
        thread.start()
    
    def translate(self, target_lang):
        """번역 실행"""
        source_text = self.txt_input.get("1.0", "end").strip()
        
        if not source_text:
            self.status_label.configure(text="❌ 번역할 내용을 입력해주세요.")
            return
        
        try:
            self.status_label.configure(text="번역 중... ⏳")
            translator = GoogleTranslator(source_language='auto', target_language=target_lang)
            translated = translator.translate(source_text)
            
            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", translated)
            self.status_label.configure(text="✅ 번역 완료")
        except Exception as e:
            error_msg = f"❌ 번역 실패: {str(e)}\n(인터넷 연결을 확인하세요)"
            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", error_msg)
            self.status_label.configure(text="❌ 오류 발생")
    
    def copy_result(self):
        """결과 복사"""
        result = self.txt_output.get("1.0", "end").strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_label.configure(text="✅ 클립보드에 복사됨")
        else:
            self.status_label.configure(text="❌ 복사할 내용이 없습니다.")
    
    def clear_all(self):
        """입력/결과 초기화"""
        self.txt_input.delete("1.0", "end")
        self.txt_output.delete("1.0", "end")
        self.status_label.configure(text="준비 완료")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernTranslator(root)
    root.mainloop()

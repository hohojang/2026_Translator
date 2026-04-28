import customtkinter as ctk
import threading
import requests

def translate_text(text, target_lang):
    """Google Translate API를 사용한 번역 함수"""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': 'auto',
        'tl': target_lang,
        'dt': 't',
        'q': text
    }
    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    data = response.json()
    translated = data[0][0][0]
    return translated

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
        
        # 언어 설정
        self.lang_dict = {
            "자동 감지": "auto",
            "한국어": "ko",
            "영어": "en",
            "중국어 (간체)": "zh-CN",
            "일본어": "ja",
            "베트남어": "vi"
        }
        self.lang_options = list(self.lang_dict.keys())
        
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
            text="다국어 자동 감지 번역",
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
        
        # 언어 선택 프레임
        lang_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        lang_frame.pack(pady=15, fill="x", padx=10)
        
        # 소스 언어
        source_label = ctk.CTkLabel(lang_frame, text="원문 언어:", font=("Segoe UI", 12, "bold"))
        source_label.pack(side="left", padx=5)
        
        self.source_combo = ctk.CTkComboBox(
            lang_frame,
            values=self.lang_options,
            width=150,
            font=("Segoe UI", 11)
        )
        self.source_combo.pack(side="left", padx=5)
        self.source_combo.set("자동 감지")
        
        # 화살표
        arrow_label = ctk.CTkLabel(lang_frame, text="→", font=("Segoe UI", 16, "bold"))
        arrow_label.pack(side="left", padx=10)
        
        # 타겟 언어
        target_label = ctk.CTkLabel(lang_frame, text="번역 언어:", font=("Segoe UI", 12, "bold"))
        target_label.pack(side="left", padx=5)
        
        self.target_combo = ctk.CTkComboBox(
            lang_frame,
            values=self.lang_options,
            width=150,
            font=("Segoe UI", 11)
        )
        self.target_combo.pack(side="left", padx=5)
        self.target_combo.set("영어")
        
        # 버튼 프레임
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=10)
        
        # 번역 버튼
        translate_btn = ctk.CTkButton(
            btn_frame,
            text="🌍 번역하기",
            command=self.translate_async,
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=8,
            fg_color="#0066CC"
        )
        translate_btn.pack(fill="x", expand=True)
        
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
    
    def translate_async(self):
        """비동기로 번역 실행"""
        source_key = self.source_combo.get()
        target_key = self.target_combo.get()
        
        if source_key == target_key:
            self.status_label.configure(text="❌ 동일한 언어로는 번역할 수 없습니다.")
            return
        
        source_lang = self.lang_dict[source_key]
        target_lang = self.lang_dict[target_key]
        
        self.status_label.configure(text="번역 중... ⏳")
        self.root.update()
        
        thread = threading.Thread(target=self.translate, args=(source_lang, target_lang))
        thread.daemon = True
        thread.start()
    
    def translate(self, source_lang, target_lang):
        """번역 실행"""
        source_text = self.txt_input.get("1.0", "end").strip()
        
        if not source_text:
            self.status_label.configure(text="❌ 번역할 내용을 입력해주세요.")
            return
        
        try:
            self.status_label.configure(text="번역 중... ⏳")
            translated = translate_text(source_text, target_lang)
            
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
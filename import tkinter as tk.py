import tkinter as tk
from tkinter import messagebox
from deep_translator import GoogleTranslator

class SimpleTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("개인용 무료 번역기 박 장 호")
        self.root.geometry("1000x500")

        # 1. 상단 안내
        tk.Label(root, text="번역기 (한국어 <-> 영어 자동 감지)", font=("Arial", 10, "bold")).pack(pady=10)

        # 2. 입력창
        tk.Label(root, text="원문 입력:").pack()
        self.txt_input = tk.Text(root, height=8, width=60)
        self.txt_input.pack(padx=20, pady=5)

        # 3. 언어 선택 버튼들
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.btn_ko_en = tk.Button(btn_frame, text="한 -> 영 번역", command=lambda: self.translate("en"), 
                                   width=15, bg="#4285F4", fg="white")
        self.btn_ko_en.pack(side=tk.LEFT, padx=5)

        self.btn_en_ko = tk.Button(btn_frame, text="영 -> 한 번역", command=lambda: self.translate("ko"), 
                                   width=15, bg="#34A853", fg="white")
        self.btn_en_ko.pack(side=tk.LEFT, padx=5)

        # 4. 결과창
        tk.Label(root, text="번역 결과:").pack(pady=5)
        self.txt_output = tk.Text(root, height=8, width=60, bg="#f9f9f9")
        self.txt_output.pack(padx=20, pady=5)

    def translate(self, target_lang):
        # 입력된 텍스트 가져오기
        source_text = self.txt_input.get("1.0", tk.END).strip()
        
        if not source_text:
            messagebox.showwarning("알림", "번역할 내용을 입력해주세요.")
            return

        try:
            # 번역 실행
            # target_lang: 'ko'는 한국어, 'en'은 영어
            translator = GoogleTranslator(source_language='auto', target_language=target_lang)
            translated = translator.translate(source_text)

            # 결과창 업데이트
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert(tk.END, translated)
        except Exception as e:
            messagebox.showerror("오류", f"번역 실패: {e}\n(인터넷 연결을 확인하세요)")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTranslator(root)
    root.mainloop()
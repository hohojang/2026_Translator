# 🌍 Google 번역기 (Google Translator)

Python과 customtkinter로 만든 현대적인 GUI 번역 프로그램입니다.
한국어와 영어를 자동으로 감지하여 실시간 번역을 제공합니다.

## ✨ 기능

- 🎨 **현대적 UI**: customtkinter를 사용한 깔끔한 다크 모드 인터페이스
- 🔄 **자동 언어 감지**: 입력 언어를 자동으로 인식
- ⚡ **빠른 번역**: Google 번역 API 기반 고품질 번역
- 📋 **복사 기능**: 번역 결과를 한 번의 클릭으로 복사
- 🗑️ **초기화 기능**: 입력/결과 영역을 쉽게 초기화

## 🚀 설치 방법

### 소스 코드에서 실행

1. **저장소 클론**
```bash
git clone https://github.com/yourusername/google-translator.git
cd google-translator
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **프로그램 실행**
```bash
python translator.py
```

### EXE 파일로 실행 (Windows)

[Release 페이지](https://github.com/yourusername/google-translator/releases)에서 `translator.exe`를 다운로드하여 실행하면 됩니다.

## 📋 요구사항

- Python 3.10 이상
- Windows / macOS / Linux

## 📦 주요 라이브러리

- **customtkinter** - 현대적 GUI
- **deep-translator** - Google 번역 API
- **requests** - HTTP 요청
- **beautifulsoup4** - HTML 파싱

## 🎯 사용 방법

1. **원문 입력**: 상단 입력 창에 번역할 텍스트를 입력합니다.
2. **언어 선택**: 
   - "한국어 → 영어" 또는 "영어 → 한국어" 버튼을 클릭합니다.
   - 또는 둘 다 클릭하여 교차 검증할 수 있습니다.
3. **결과 확인**: 하단 결과 창에서 번역 결과를 확인합니다.
4. **복사**: "📋 결과 복사" 버튼으로 결과를 클립보드에 복사합니다.

## ⚙️ 시스템 요구사항

- **OS**: Windows 10 이상 (EXE 실행 시)
- **인터넷**: Google 번역 API 사용으로 필수
- **메모리**: 최소 200MB

## 🔧 개발 정보

- 언어: Python 3.13
- GUI 프레임워크: customtkinter
- 번역 라이브러리: deep-translator
- 멀티스레딩: 번역 중 UI 프리징 방지

## 📝 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request는 언제든 환영합니다!

## 📧 연락

문제가 있으시면 GitHub Issues를 통해 연락 주세요.

---
**마지막 업데이트**: 2026년 4월 28일

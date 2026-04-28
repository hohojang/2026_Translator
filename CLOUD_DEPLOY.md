# 🚀 클라우드 배포 가이드

## Railway 배포 (권장)

### 1. Railway 가입
- https://railway.app 에서 GitHub 계정으로 가입

### 2. 프로젝트 생성
- "New Project" → "Deploy from GitHub repo"
- 저장소 선택: `hohojang/2026_Translator`

### 3. 자동 배포
- Railway가 자동으로 `requirements.txt` 읽어서 설치
- `Procfile`에 따라 `gunicorn`으로 실행
- 배포 완료까지 5-10분 소요

### 4. 도메인 확인
- 배포 완료 후 자동으로 HTTPS 도메인 제공
- 예: `https://translator-production-1234.up.railway.app`

### 5. 아이폰에서 사용
- PC 꺼져도 24/7 실행
- 브라우저로 도메인 접속

## 📱 모바일 최적화 완료
- 반응형 디자인 적용
- 터치 인터페이스 지원
- 모바일 브라우저 완벽 호환

## 💰 Railway 무료 플랜
- 월 512MB RAM, 1GB 디스크
- 월 100시간 무료 실행
- 초과 시 자동 중지 (다음 달에 재시작)

---
**배포 준비 완료!** 🎉
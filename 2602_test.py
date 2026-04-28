import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import struct

# --- 설정 (필요 시 수정) ---
PC_IP = '0.0.0.0'      # PC의 모든 네트워크 카드에서 수신 대기
PORT = 31               # 보드 코드의 DEST_PORT와 일치해야 함
MAX_POINTS = 100       # 그래프에 표시할 데이터 개수

# 데이터 저장용 리스트
x_data = []
y_data = []

# 1. TCP 서버 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((PC_IP, PORT))
server_socket.listen(1)
print(f"서버가 시작되었습니다. 보드(192.168.0.200)의 연결을 기다리는 중... (포트: {PORT})")

conn, addr = server_socket.accept()
print(f"보드 연결 성공! 연결된 주소: {addr}")

# 2. 그래프 초기 설정
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Sensor Value')
ax.set_ylim(0, 5)  # ADC 전압 기준 (0V ~ 3.3V/5V) - 센서에 맞게 조절
ax.set_xlim(0, MAX_POINTS)
ax.set_xlabel('Time (Samples)')
ax.set_ylabel('Value')
ax.set_title('Real-time Sensor Data from STM32')
ax.legend()

def update(frame):
    try:
        # 보드에서 보낸 데이터 수신 (1024바이트)
        raw_data = conn.recv(1024)
        if not raw_data:
            return line,

        # 데이터 해석 (보드가 문자열 "2.55" 형태의 데이터를 보낸다고 가정)
        # 만약 바이너리(struct) 형태라면 구조에 맞게 수정이 필요합니다.
        decoded_str = raw_data.decode('utf-8').strip()
        
        # 첫 번째 숫자만 추출 (여러 데이터가 섞여 올 경우 대비)
        val = float(decoded_str.split(',')[0]) 

        y_data.append(val)
        if len(y_data) > MAX_POINTS:
            y_data.pop(0)

        line.set_data(range(len(y_data)), y_data)
        
    except Exception as e:
        print(f"데이터 수신 오류: {e}")
        
    return line,

# 3. 애니메이션 시작
ani = FuncAnimation(fig, update, interval=1000) # 1초마다 업데이트
plt.show()

# 종료 시 소켓 닫기
conn.close()
server_socket.close()

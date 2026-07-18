import rclpy
from rclpy.node import Node
import os
import time

VOICE_PATH = "/root/Voice2.mp3"


class VoiceNode(Node):

    def __init__(self):
        super().__init__("voice_node")

        # 2초마다 상태 확인
        self.timer = self.create_timer(2.0, self.check)

        # ===== 테스트용 변수 =====
        # 나중에 YOLO가 이 값을 바꿔줄 예정
        self.person_detected = True
        self.helmet_detected = False

        # 마지막 음성 출력 시간
        self.last_voice_time = 0

    def play_voice(self):
        self.get_logger().info("⚠ 안전모 미착용! 음성 안내 출력")
        os.system(f"ffplay -nodisp -autoexit {VOICE_PATH}")

    def check(self):

        # -----------------------
        # 사람이 없으면 상태 초기화
        # -----------------------
        if not self.person_detected:
            self.get_logger().info("사람 없음")

            self.last_voice_time = 0
            return

        # -----------------------
        # 안전모를 착용한 경우
        # -----------------------
        if self.helmet_detected:

            self.get_logger().info("✔ 안전모 착용")

            self.last_voice_time = 0
            return

        # -----------------------
        # 안전모 미착용
        # -----------------------
        now = time.time()

        if now - self.last_voice_time >= 5:

            self.play_voice()

            self.last_voice_time = now

        else:

            remain = round(5 - (now - self.last_voice_time), 1)

            self.get_logger().info(
                f"안전모 미착용 (다음 안내까지 {remain}초)"
            )


def main(args=None):

    rclpy.init(args=args)

    node = VoiceNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
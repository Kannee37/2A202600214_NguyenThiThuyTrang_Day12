class MockLLM:
    def invoke(self, messages):
        user_message = messages[-1]["content"].lower()

        if "xin chào" in user_message or "hello" in user_message:
            answer = "Chào bạn! Mình là TravelBuddy mock bot, hiện đang chạy ở chế độ demo."
        elif "đà nẵng" in user_message:
            answer = (
                "Mock response: Mình gợi ý bạn đi Đà Nẵng.\n"
                "- Chuyến bay: khoảng 1.000.000 VND\n"
                "- Khách sạn: khoảng 500.000 VND/đêm\n"
                "- Tổng chi phí ước tính: khoảng 2.000.000 VND"
            )
        elif "phú quốc" in user_message:
            answer = (
                "Mock response: Phú Quốc phù hợp nếu bạn thích biển và nghỉ dưỡng.\n"
                "Ngân sách nên từ 3 đến 5 triệu cho chuyến ngắn ngày."
            )
        else:
            answer = (
                "Mock response: Đây là phản hồi demo từ MockLLM. "
                "Hiện hệ thống chưa gọi model thật."
            )

        return {
            "answer": answer,
            "messages": messages,
        }
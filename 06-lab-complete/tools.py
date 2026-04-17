from langchain_core.tools import tool

# ================================================================
# MOCK DATA - dữ liệu giả lập hệ thống du lịch
# ================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Rivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina’s Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6},
    ]
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    """
    flights = FLIGHTS_DB.get((origin, destination))

    if not flights:
        reverse_flights = FLIGHTS_DB.get((destination, origin))
        if reverse_flights:
            return (
                f"Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                f"Nhưng có dữ liệu chiều ngược lại từ {destination} đến {origin}."
            )
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    results = []
    for flight in flights:
        results.append(
            f"{flight['airline']} | "
            f"{flight['departure']} - {flight['arrival']} | "
            f"{flight['class']} | "
            f"{flight['price']:,} VND"
        )
    return "\n".join(results)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu về khách sạn tại thành phố {city}"

    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    if not filtered:
        return f"Không tìm thấy khách sạn phù hợp tại {city} với giá dưới {max_price_per_night:,} VND/đêm."

    filtered.sort(key=lambda x: x["rating"], reverse=True)

    results = []
    for h in filtered:
        results.append(
            f"{h['name']} | {h['stars']} sao | {h['price_per_night']:,} VND | {h['area']} | rating {h['rating']}"
        )
    return "\n".join(results)


def format_vnd(price: int) -> str:
    return f"{price:,}".replace(",", ".") + "đ"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    """
    if not expenses:
        return "Không có khoản chi nào được cung cấp."

    expense_dict = {}
    total_expense = 0

    try:
        items = expenses.split(",")
        for item in items:
            name, value = item.split(":")
            name = name.strip()
            value = int(value.strip())
            expense_dict[name] = value
            total_expense += value
    except Exception:
        return "Format expenses không hợp lệ. Dùng dạng 'tên:số, tên:số'"

    remaining = total_budget - total_expense

    lines = []
    lines.append("Bảng chi phí:")
    for name, value in expense_dict.items():
        lines.append(f"- {name}: {format_vnd(value)}")

    lines.append("--------")
    lines.append(f"Tổng chi: {format_vnd(total_expense)}")
    lines.append(f"Ngân sách: {format_vnd(total_budget)}")

    if remaining >= 0:
        lines.append(f"Còn lại: {format_vnd(remaining)}")
    else:
        lines.append(f"Vượt ngân sách: {format_vnd(-remaining)}")

    return "\n".join(lines)
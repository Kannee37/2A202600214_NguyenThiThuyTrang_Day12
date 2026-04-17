# ============================================================
# ADVANCED Dockerfile — Multi-stage build for Railway
#
# Mục tiêu:
# - image gọn
# - chạy non-root
# - tương thích Railway
# - không lỗi uvicorn / $PORT
# ============================================================

# ──────────────────────────────────────────────────────────
# STAGE 1: Builder
# Cài dependencies vào /root/.local
# ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements từ project
COPY 02-docker/production/requirements.txt ./requirements.txt

# Cài package vào user site của root: /root/.local
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir --user -r requirements.txt


# ──────────────────────────────────────────────────────────
# STAGE 2: Runtime
# Chỉ giữ phần cần để chạy app
# ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Tạo non-root user với HOME rõ ràng
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

WORKDIR /app

# Copy packages từ builder sang đúng home của appuser
COPY --from=builder /root/.local /home/appuser/.local

# Copy source code cần thiết
COPY 02-docker/production/main.py /app/main.py
COPY utils/mock_llm.py /app/utils/mock_llm.py

# Nếu main.py còn import thêm file khác thì copy thêm ở đây
# Ví dụ:
# COPY app/ /app/app/
# COPY system_prompt.txt /app/system_prompt.txt

# Set quyền
RUN chown -R appuser:appuser /app /home/appuser

USER appuser

# Quan trọng: HOME phải khớp với nơi chứa .local
ENV HOME=/home/appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:' + ('8000') + '/health')" || exit 1

# Dùng sh -c để expand biến PORT của Railway
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
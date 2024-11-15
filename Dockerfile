FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils\
    curl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV VIRTUAL_ENV="/app/.venv" \
    PATH="$VIRTUAL_ENV/bin:/root/.local/bin:$PATH"

WORKDIR /app

COPY . .


RUN python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/python -m pip install --upgrade pip && \
    uv sync --frozen
EXPOSE 8501

CMD ["uv","run","streamlit", "run", "app.py"]
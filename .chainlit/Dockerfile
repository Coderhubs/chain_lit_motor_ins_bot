# Use Python 3.10 for better compatibility
FROM python:3.10

# Create non-root user for HF Spaces
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY --chown=user . .

# Start Chainlit on HF Spaces-compatible host/port
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "7860", "-h"]

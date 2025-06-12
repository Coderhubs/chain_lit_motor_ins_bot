# Use an official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port provided by Render
ENV PORT=10000
EXPOSE ${PORT}

# Start Chainlit app on the correct port
CMD ["sh", "-c", "chainlit run main.py --port $PORT"]

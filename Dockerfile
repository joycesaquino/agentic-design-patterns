FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .chainlit directories if they don't exist
RUN mkdir -p /app/.chainlit /app/ai_chat/.chainlit

# Expose Chainlit default port
EXPOSE 8001

# Set working directory for Chainlit app
WORKDIR /app/ai_chat

# Run Chainlit
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8001"]


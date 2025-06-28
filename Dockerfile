# Dockerfile

FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose ports for both FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start both FastAPI and Streamlit using a script
CMD ["bash", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run visualize/visualize.py --server.port 8501 --server.headless true"]

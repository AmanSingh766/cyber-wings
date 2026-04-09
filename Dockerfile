# Python base image
FROM python:3.11

# working directory
WORKDIR /app

# copy all files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt


ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# expose streamlit port
EXPOSE 8501

# run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
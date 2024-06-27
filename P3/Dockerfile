# Use a lightweight version of python
FROM python:3.8-slim

# Disable output buffering (Show outputs in terminal)
ENV PYTHONUNBUFFERED=1
# Set the working directory
WORKDIR /app
# Copy current file into working dir
COPY simpleServer.py /app/
# Expose the port to the outside of container
EXPOSE 8000
# Run the server
CMD ["python", "simpleServer.py"]


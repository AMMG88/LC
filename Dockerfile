# syntax=docker/dockerfile:1.2
FROM python:3.9
# put you docker configuration here 

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Instala distutils y actualiza pip, luego instala los requisitos
RUN pip install -r /app/requirements.txt

# Expose the port that the application will run on
EXPOSE 8080

# Command to run the application using Uvicorn
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
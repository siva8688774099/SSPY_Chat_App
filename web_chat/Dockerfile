FROM python:3.11

# Set the timezone
RUN apt-get update && apt-get install -y tzdata && \
	ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
	echo "Asia/Kolkata" > /etc/timezone

# Upgrade pip
RUN pip install --upgrade pip --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
RUN pip install --upgrade awscli --trusted-host=pypi.org --trusted-host=files.pythonhosted.org

# Install Python dependencies
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --trusted-host=pypi.org --trusted-host=files.pythonhosted.org

# Copy application files
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the necessary port
EXPOSE 8000

# Set the entry point for the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
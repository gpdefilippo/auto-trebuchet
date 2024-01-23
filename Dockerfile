# Use an official Python runtime as a parent image
FROM python:3.12.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
Run pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code into the container at /usr/src/app
COPY . .

# Run your tests
CMD ["python", "-m", "unittest", "discover", "tests"]


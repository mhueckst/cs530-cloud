# Use Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
MAINTAINER Your Name "mhueck2@pdx.edu"

# Copy the contents of the current directory into the container directory /final
COPY . /final

# Set the working directory of the container to /app
WORKDIR /final

# Install the Python packages specified by requirements.txt into the container
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

#CMD ["main.py"]

# Set the parameters to the program
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app


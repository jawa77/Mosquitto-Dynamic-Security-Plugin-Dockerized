# Use Ubuntu as the base image
FROM ubuntu:latest

# Avoid prompts from apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install software properties common to manage repositories
RUN apt-get update && apt-get install -y software-properties-common

# Add the Mosquitto repository
RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa

# Update the package list after adding Mosquitto repository
RUN apt-get update

# Install the latest Mosquitto broker and clients
RUN apt-get install -y mosquitto mosquitto-clients

# Optional: Install expect and vim for scripting and editing inside the container
RUN apt-get install -y expect vim nano jq

# Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Create directory structure for Mosquitto configuration and data
RUN mkdir -p /mosquitto/config /mosquitto/data /mosquitto/log

# Copy configuration files from your host to the container
COPY config/mosquitto.conf /mosquitto/config/mosquitto.conf
COPY config/dynamic-security.json /mosquitto/config/dynamic-security.json

# Set the working directory for the CMD instruction
WORKDIR /mosquitto

# Expose the default Mosquitto port
EXPOSE 1883

# Start Mosquitto broker using the custom configuration file
CMD ["mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]

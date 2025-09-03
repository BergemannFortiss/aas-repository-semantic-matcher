# Use the official Alpine Linux as the base image
FROM python:3.11-alpine

# Update packages
RUN apk update

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY ./aas_repository_semantic_matcher ./aas_repository_semantic_matcher
COPY ./pyproject.toml ./pyproject.toml
COPY ./LICENSE ./LICENSE
COPY ./README.md ./README.md
COPY ./requirements.txt ./requirements.txt

# Install Python dependencies using pip, from pyproject.toml
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to the app directory
ENV PYTHONPATH=/app

# Command to run the FastAPI server
CMD python aas_repository_semantic_matcher/matcher.py "$REPOSITORY_ENDPOINT"

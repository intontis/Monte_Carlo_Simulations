
# 1. Choose the base Python image
FROM docker.io/library/python:3.14-slim
LABEL org.opencontainers.image.source="https://github.com/intontis/Monte_Carlo_Simulations"

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/matplotlib \
    HOME=/tmp

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy dependency files first
COPY requirements.txt requirements-notebooks.txt ./

# 5. Install Python dependencies
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir \
    -r requirements.txt \
    -r requirements-notebooks.txt

# 6. Copy the project files
COPY --chown=10001:0 . .

# 7. Prepare directories for OpenShift-compatible permissions
RUN mkdir -p /app/results \
    && chgrp -R 0 /app \
    && chmod -R g=u /app

# 8. Run as a non-root user
USER 10001:0

# 9. Default command: execute the test suite
CMD ["python", "-m", "pytest", "-v"]

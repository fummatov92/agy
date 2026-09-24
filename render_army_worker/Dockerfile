# ========================================================
# JarvisOS Distributed Army Worker Dockerfile for Render
# ========================================================
FROM node:20-slim

WORKDIR /app

# Install basic networking tools & git
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node dependencies
COPY package*.json ./
RUN npm install --production

# Copy application files
COPY . .

# Environment Defaults
ENV PORT=10000
ENV NODE_ENV=production

EXPOSE 10000

CMD ["node", "server.js"]

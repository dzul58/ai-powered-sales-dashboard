# Build stage
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy seluruh kode aplikasi
COPY . .

# Build aplikasi
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy built assets dari builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/styles ./styles
COPY --from=builder /app/pages ./pages

# Expose port
EXPOSE 3000

# Command untuk menjalankan aplikasi
CMD ["npm", "start"] 
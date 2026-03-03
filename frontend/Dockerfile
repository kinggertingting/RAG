# ========= Build stage =========
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files trước để tận dụng cache
COPY package.json package-lock.json* ./

RUN npm install

# Copy toàn bộ source
COPY . .

# Build production
RUN npm run build


# ========= Production stage =========
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

# Chỉ copy những gì cần để chạy
COPY --from=builder /app/package.json ./
COPY --from=builder /app/package-lock.json* ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
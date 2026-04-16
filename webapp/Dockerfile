# Multi-stage build for Next.js application

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package files from webapp directory
COPY webapp/package.json webapp/package-lock.json* ./
RUN npm ci

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
# Copy webapp source files
COPY webapp/ ./

# Build the Next.js app
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create a non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Create directory for database
RUN mkdir -p /app/data && chown nextjs:nodejs /app/data

# Copy database from project root (build context is project root)
COPY --chown=nextjs:nodejs data/questions.db /app/data/questions.db

# Copy necessary files from builder
# Public folder
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
# Standalone server
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
# Static assets
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV DB_PATH=/app/data/questions.db

CMD ["node", "server.js"]

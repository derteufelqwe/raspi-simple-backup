FROM node:22-slim as builder

WORKDIR /app

COPY package*.json .
COPY pnpm-lock.yaml .

# Install dependencies
RUN npm i -g pnpm
RUN pnpm install

COPY . .

RUN pnpm run build


FROM node:22-slim as deployer
LABEL Author=derteufelqwe@gmail.com

ENV NODE_ENV=production
ENV TZ=Europe/Berlin

EXPOSE 3000

WORKDIR /app

COPY --from=builder /app/build build/
COPY --from=builder /app/package.json .

# Install dependencies (ci not implemented in pnpm yet)
RUN npm i -g pnpm \
    && pnpm install \
    && pnpm prune --prod \
    && npm uninstall -g pnpm

CMD [ "node", "build" ]
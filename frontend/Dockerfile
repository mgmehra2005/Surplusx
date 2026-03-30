FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
# Using the flags we learned to avoid SSL issues on Fedora
RUN npm install --legacy-peer-deps --no-audit
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
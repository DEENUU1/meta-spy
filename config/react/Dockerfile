# Use a base image with Node.js
FROM node:16 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY facebookspy/src/server/frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY facebookspy/src/server/frontend/ ./

# Build the frontend
RUN npm run build

# Use a lightweight web server to serve the built frontend
FROM nginx:alpine

# Copy the built frontend to the NGINX web server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Command to start NGINX
CMD ["nginx", "-g", "daemon off;"]

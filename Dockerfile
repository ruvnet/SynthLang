FROM nginx:alpine

# Copy the built static files to nginx's serve directory
COPY dist /usr/share/nginx/html

# Copy a custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 as required by Fly.io
EXPOSE 8080

# Update nginx config to listen on port 8080
RUN sed -i 's/listen\(.*\)80;/listen 8080;/' /etc/nginx/conf.d/default.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

# Use the latest Nginx Alpine image
FROM nginx:alpine

# Install curl for healthcheck
RUN apk --no-cache add curl

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Copy the HTML file to Nginx's html directory
COPY index.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
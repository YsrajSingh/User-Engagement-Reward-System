# Coming Soon

docker build -t user-engagement-system:prod .

docker run --env-file .env -p 8000:8000 user-engagement-system:prod

docker run -d --env-file .env -p 8000:8000 user-engagement-system:prod
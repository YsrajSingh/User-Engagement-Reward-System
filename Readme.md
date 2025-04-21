# Coming Soon

docker buildx create --use

docker build -t user-engagement-system:prod .

docker run --env-file .env -p 8000:8000 user-engagement-system:prod

docker run -d --env-file .env -p 8000:8000 user-engagement-system:prod

echo "<github token>" | docker login ghcr.io -u ysrajsingh --password-stdin


docker buildx build \
  --platform linux/amd64 \
  -t ghcr.io/ysrajsingh/user-engagement-reward-system:latest \
  --push .

## Below are depricated (use above command)

docker build -t ghcr.io/ysrajsingh/user-engagement-reward-system:latest .


docker push ghcr.io/ysrajsingh/user-engagement-reward-system:latest

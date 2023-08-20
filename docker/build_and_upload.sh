export https_proxy=...
export http_proxy=...
export all_proxy=...
docker_user=...
tag=$(date +%Y%m%d)

docker build --network host --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy --build-arg all_proxy=$all_proxy -t pixiu:$tag -f DOCKERFILE .
docker tag pixiu:$tag $docker_user/pixiu:$tag
docker push $docker_user/pixiu:$tag
docker tag pixiu:$tag $docker_user/pixiu:latest
docker push $docker_user/pixiu:latest

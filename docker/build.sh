#!/bin/bash

function usage() {
  echo "build.sh [OPTIONS] -n <name>"
  echo "    -h                    도움말 출력"
  echo "    -v version            빌드 버전 (default: v0.1.0)"
  echo "    -r                    RC 버전을 빌드 (default: false)"
  echo "    -o order              RC 버전을 빌드 할 때 오늘 몇 번째 빌드인지 정수(int) 입력 (default: 0)"
  echo "    -d                    dev 버전 빌드 (default: false)"
  exit 0
}

version=v0.1.0
rc=false
orderRC=0
dev=false

while getopts "hv:ro:d" opt
do
  case $opt in
    v) version=$OPTARG ;;
    r) rc=true ;;
    o) orderRC=$OPTARG ;;
    d) dev=true ;;
    h) usage ;;
    ?) usage ;;
  esac
done

function get_img_name() {
  if $dev; then
    echo "db-copy-cron-job"
  else
    echo "db-copy-cron-job"
  fi
}

##############################
########## prepare  ##########
##############################
echo "===== Start setting for image ====="
# check working directory
basePath=$(dirname $0)/..
cd $basePath
basePath=$(pwd)

# Make image tag
today=$(date +%Y%m%d)
headHash=$(git rev-parse --short=7 HEAD)
if $rc
then
  imgTag=${version}-RC${today}.${orderRC}-${headHash}
else
  imgTag=${version}-${headHash}
fi

# Get image name
imgName=$(get_img_name)
echo "===== End setting for image ====="
echo ""

##############################
##########  build   ##########
##############################
echo "===== Start to build docker image ====="

# Build image
DOCKER_BUILDKIT=1 docker build \
  --target app-image \
  --build-arg project_version=${version} \
  -f docker/Dockerfile \
  -t $imgName:$imgTag $basePath

echo "===== Complete to build docker image: [ $imgName:$imgTag ] ====="
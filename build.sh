#!/bin/bash

set -e
set -x

REQUIREMENT_TXT=keep
RELEASE_SUFFIX=""
if [[ "$1" == "release" ]]
then
	REQUIREMENT_TXT=refresh
	RELEASE_SUFFIX="-release"
fi

TAG="$(git describe --long --dirty)${RELEASE_SUFFIX}"
IMAGE=localhost/www-migrate
IMAGE_TAG="$IMAGE:$TAG"
OUTDIR="$PWD/out"

podman build \
	--build-arg REQUIREMENT_TXT="$REQUIREMENT_TXT" \
	-t "$IMAGE_TAG" \
	.

copy_from_image() {
	project="$1"
	shift

	for file in "$@"
	do
		file="$2"
		podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" \
cp "/build/$project/$file" "/out/$project-$file"
		cp -- "out/$project-$file" "$project/$file"
	done
}

if [[ "$REQUIREMENT_TXT" == "refresh" ]]
then
	mkdir -p -- "$OUTDIR"

	copy_from_image links2md requirements.txt requirements.lock
	copy_from_image rss requirements.txt requirements.lock
	copy_from_image tagger requirements.txt requirements.lock
	copy_from_image wordpress requirements.txt requirements.lock
fi

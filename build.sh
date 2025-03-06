#!/bin/sh

set -e
set -x

REQUIREMENT_TXT=keep
RELEASE_SUFFIX=""
if [ "$1" = "release" ]
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

if [ "$REQUIREMENT_TXT" = "refresh" ]
then
	mkdir -p -- "$OUTDIR"

	podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" \
		cp /build/rss/requirements.txt \
		/out/rss-requirements.txt
	podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" \
		cp /build/tagger/requirements.txt \
		/out/tagger-requirements.txt
	podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" \
		cp /build/wordpress/requirements.txt \
		/out/wordpress-requirements.txt

	cp -- "$OUTDIR/rss-requirements.txt" rss/requirements.txt
	cp -- "$OUTDIR/tagger-requirements.txt" tagger/requirements.txt
	cp -- "$OUTDIR/wordpress-requirements.txt" wordpress/requirements.txt
fi

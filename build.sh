#!/bin/sh

set -x
set -e

TAG="$(git describe --long --dirty)"
IMAGE=localhost/www-migrate
IMAGE_TAG="$IMAGE:$TAG"
OUTDIR="$PWD/out"

podman build . -t "$IMAGE_TAG"

mkdir -p -- "$OUTDIR"

podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" cp /build/rss/requirements.txt /out/rss-requirements.txt
podman run --rm -v "$OUTDIR":/out:rw "$IMAGE_TAG" cp /build/wordpress/requirements.txt /out/wordpress-requirements.txt

cp -- "$OUTDIR/rss-requirements.txt" rss/requirements.txt
cp -- "$OUTDIR/wordpress-requirements.txt" wordpress/requirements.txt

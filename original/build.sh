#!/bin/sh
# Build the gold binary of jo 1.9.
# Usage: build.sh <source-dir> <output-path>     (extra flags via CFLAGS / LDFLAGS)
# The source dir is a checkout of https://github.com/jpmens/jo at the commit in task.yaml.
set -e
SRC="$1"; OUT="$2"
${CC:-cc} ${CFLAGS:--O2} -std=gnu99 \
  -DPACKAGE_VERSION='"1.9"' -DHAVE_SNPRINTF=1 -DHAVE_ERR=1 -DHAVE_ERRX=1 \
  -DHAVE_STRCHR=1 -DHAVE_STRRCHR=1 -DHAVE_STRLCPY=0 -DHAVE_STRLCAT=0 -DHAVE_PLEDGE=0 \
  -o "$OUT" "$SRC/jo.c" "$SRC/json.c" "$SRC/base64.c" ${LDFLAGS} -lm

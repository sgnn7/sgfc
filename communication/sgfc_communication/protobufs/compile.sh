#!/bin/bash -e

CURRENT_DIR=$(readlink -f $(dirname $0))
echo "$CURRENT_DIR"

protoc -I="${CURRENT_DIR}" \
       --python_out="${CURRENT_DIR}" \
       "${CURRENT_DIR}/sgfc.proto"

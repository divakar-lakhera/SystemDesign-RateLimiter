#!/bin/bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"uid":"abcd"}' \
    http://127.0.0.1:5000/request/
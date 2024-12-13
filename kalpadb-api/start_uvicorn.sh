#!/bin/bash
xvfb-run --server-args="-screen 0 1024x768x24" uvicorn app.kalpadb-api-main:app --host 0.0.0.0 --port 8088 --log-level debug

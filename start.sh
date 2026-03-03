#!/bin/bash
# 確保使用 bash，並給予執行權限
uvicorn main:app --host 0.0.0.0 --port $PORT
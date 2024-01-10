#!/bin/bash
docker run -d -p 5000:5000 -v "$(pwd)/static/updates:/khs-backend/static/updates" --name khs-server-container khs-server-img

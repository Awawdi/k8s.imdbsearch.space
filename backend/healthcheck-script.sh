#!/bin/bash

EXIT_CODE=0
echo "Checking if web service is up..."
if ! curl -f http://localhost:8000/health >/dev/null; then
  echo "Web service is not reachable"
  EXIT_CODE=1
else
  echo "Web service is up"
fi


if [ $EXIT_CODE -eq 0 ]; then
  echo "All health checks passed."
else
  echo "Some health checks failed."
fi

exit $EXIT_CODE
while true; do
  echo "data: $(date +%s)" | curl -X POST --data-binary @- http://161.0.0.1:5002/stream
  sleep 1
done

for cgnum in $(seq 110 114); do

  echo "Collecting $cgnum"
  echo "----------------------"
  sleep 2
  rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
        govtrack.us::govtrackdata/congress/$cgnum ./wrangle/corral/fetched/congress
done

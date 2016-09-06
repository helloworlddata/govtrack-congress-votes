#!/usr/bin/env sh
for cgnum in $(seq 98 114); do

  srcpath=govtrack.us::govtrackdata/congress/$cgnum/votes
  destpath=./wrangle/corral/fetched/congress/$cgnum
  echo "Syncing with:      $srcpath"
  echo "Saving locally to: $destpath"
  echo "------------------"
  mkdir -p $destpath
  sleep 2

  rsync -avz --delete --delete-excluded \
        --exclude **/text-versions/ \
        $srcpath \
        $destpath
done

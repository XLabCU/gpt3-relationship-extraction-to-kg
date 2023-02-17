#!/bin/bash

# iterate over all files in the current directory
for file in *
do
  # check if file size is greater than 6 KB
  if [[ -f "$file" && $(stat -f%z "$file") -gt 6144 ]]; then
    echo "Splitting file $file"
    # split the file into smaller chunks of 6 KB or less
    split -b 6k -d -a 4 "$file" "$file.part"
    # check if the smallest part is at least 6 KB
    smallest_part=$(ls -S "$file".part* | head -n 1)
    if [[ -f "$smallest_part" && $(stat -f%z "$smallest_part") -lt 6144 ]]; then
      echo "Smallest part is less than 6 KB, deleting split files"
      rm "$file".part*
    else
      # remove the original file if it has been split into smaller parts
      rm "$file"
    fi
  fi
done

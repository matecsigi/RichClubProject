#!/bin/sh

echo "Start run"

python hyperbolicModelRichClubExact.py 10000 18.5
wait
echo "Done"

python hyperbolicModelRichClubExact.py 10000 18.75
wait
echo "Done"

python hyperbolicModelRichClubExact.py 10000 19
wait
echo "Done"

python hyperbolicModelRichClubExact.py 10000 19.25
wait
echo "Done"

#!/bin/bash
lftp -e "mirror --parallel=5 --use-pget-n=5 / $PWD; quit" $1
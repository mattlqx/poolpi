#!/bin/bash

if [ -z "$1" ]; then
  seconds=300
else
  seconds=$((60 * $1))
fi

RRD_PATH=$(realpath $(dirname $BASH_SOURCE)/..)
rrdtool fetch $RRD_PATH/temperature.rrd AVERAGE -s now-${seconds}s -e now

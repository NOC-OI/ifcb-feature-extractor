#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
cd ..
mkdir -p testdata
cd testdata
SHAOUT=($(cat *.adc *.hdr *.roi *.csv | sha256sum -b))
SHAOUT=${SHAOUT[0]}
if [ "$SHAOUT" = "9b7d515f61a3ddc6905ec57abd737e2d3a7c923c3beb01730424abcd23a1a900" ]; then
    echo "Test data OK, skipping download"
else
    echo "Test data hash ($SHAOUT) did not match expected output, redownloading data"
    rm *.adc *.hdr *.roi *.csv
    ROOT_URI="https://ifcb-data.whoi.edu/mvco/D20191211T034109_IFCB010"
    wget ${ROOT_URI}.adc
    wget ${ROOT_URI}.hdr
    wget ${ROOT_URI}.roi
    wget ${ROOT_URI}_features.csv
# src = https://ifcb-data.whoi.edu/timeline?dataset=IFCB14_dock_WHOI&bin=D20160106T195140_IFCB014
fi

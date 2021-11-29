#! /bin/bash
pat='(..:..:..:..:..:..)'
bluetoothctl -- devices | while read line ;
do
  [[ $line =~ $pat ]]
  echo "${BASH_REMATCH[0]}"
  if [[ ${BASH_REMATCH[0]} != "F4:73:35:0F:CE:06" ]]; then
    bluetoothctl -- remove "${BASH_REMATCH[0]}"
  fi
done

bluetoothctl -- discoverable on

numDevices=`bluetoothctl -- devices | wc -l`

while [ $numDevices -le 1 ]
do
    sleep 1
    numDevices=`bluetoothctl -- devices | wc -l`
done

bluetoothctl -- discoverable off

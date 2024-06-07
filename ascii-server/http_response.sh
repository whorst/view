#!/bin/bash
#
# This program is used in conjuction with `tcpserver` from the `ucspi-tcp` package.
#
# Usage:
#  $ tcpserver _host_ _port_ ./http_response.sh

set -euo pipefail

chars="abcdefghijklmnopqrstuvwxyz"
if [ "true" == "${NUMBERS_ONLY:-false}" ]; then
  chars="0123456789"
fi

length=$(( RANDOM % ${#chars} ))
if [ "${length}" -lt 1 ]; then length=1; fi

response=""
for (( i = 0; i < "$length"; i++ ))
do
  response+="${chars:$(( RANDOM % ${#chars} )):1}"
done

echo -e "HTTP/1.1 200 OK\nContent-Length: ${length}\nContent-Type: text/plain; charset=us-ascii\n\n${response}"

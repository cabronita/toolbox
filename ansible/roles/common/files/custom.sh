#!/bin/bash

if (( $UID == 0 )); then
    PS1='\h # '
else
    PS1='\u@\h $ '
fi

set -o vi

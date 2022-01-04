#!/bin/bash

#################################################################################
#                    **-- Subdomain Takeover Check --**                         #
#                                                                               #
# checks for dangling DNS CNAMEs among a list of subdomains                     #
# ex: ./subdom-tko.sh wordlist.txt example.com                                  #
#                                                                               #
# Copyright (c) 2018 Andrew Trube  <https://github.com/AndrewTrube>             #
#                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining a copy  #
# of this software and associated documentation files (the "Software"), to deal #
# in the Software without restriction, including without limitation the rights  #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
# copies of the Software, and to permit persons to whom the Software is         #
# furnished to do so, subject to the following conditions:                      #
#                                                                               #
# The above copyright notice and this permission notice shall be included in all#
# copies or substantial portions of the Software.                               #
#                                                                               #                                              
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################

if [ $# -le 1 ]; then
    echo "Usage: subdomain-takeover.sh HOST-LIST TARGET"
    exit 0
else
    while read subdoms 
       do
           if host $subdoms >/dev/null; then
               echo "$subdoms" >> "live-hosts-tko-$2.txt"
           fi
       done < $1
   
    for HOSTS in `cat "live-hosts-tko-$2.txt"`; do 
        $( dig $HOSTS | grep CNAME ) >> "subdom-tko-targets-$2.txt" 
    done
fi


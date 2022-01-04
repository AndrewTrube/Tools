#!/bin/bash

#################################################################################
#                       **-- Recon Workflow --**                                #
#                                                                               #
# Extracts the subdomains from securitytrails.com (API KEY required) and crt.sh # 
# combines them with any newline seperated list of subdomains (such as from     #
# DNS brute force scan), checks if host is live and then feeds them to nmap.    #
# ex: ./recon_workflow.sh amass-results-yahoo.txt yahoo.com                     #
#                                                                               #
# Copyright (c) 2019 Andrew Trube  <https://github.com/AndrewTrube>             #
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


if [[ $# != 3 ]] ; then
  echo "Usage: ./program [Security Trails APIKEY] [line seperated list of subdomains] [domain.tld]"
  exit
fi


#extract subdomains
temp_fd=`mktemp -u`

echo -e 'Getting subdomains from Security Trails\n'
curl "https://api.securitytrails.com/v1/domain/$3/subdomains" -H "apikey: $1" | sed -E -n '/["\S\.]/p' | cut -d'"' -f2 | sed '$d;1d' | sed "s/$/.$3/" | sort -u > $temp_fd

echo -e "Getting subdomains from Crt.sh\n"
curl "https://crt.sh/?q=$3?output=json" | json_pp -f json -t dumper | grep name_value | cut -f2 -d'"' | sed -e 's/\\n/,/g' | tr ',' '\n' | sed "/*/d" | sort -u >> $temp_fd

echo -e "Combining subdomains into a single list\n"
cat $2 | cut -f1 -d',' | sort -u >> $temp_fd
sort -u $temp_fd > $PWD/subdomains-combined-$3.txt && 
rm $temp_fd 


#get live hosts
echo -e "Running DNS scans to check for live hosts...\n"
while read subdom; 
  do 
    ip=$(host "$subdom" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}') 
    if [[ `echo "$ip" | wc -c` -ge 2 ]]; then      
      echo "$subdom,$ip" >> live-hosts-$3.txt; 
    fi
  done < subdomains-combined-$3.txt &&


#run defualt nmap scan of top 100 ports to check for webhosts
echo -e 'Feeding to Nmap...\n'
nmap_list=`mktemp -u`
mkdir "$3-nmap" 
cut -f2 -d',' live-hosts-$3.txt | sort -u > $nmap_list
nmap --top-ports 100 -sV --version-light -oA "./$3-nmap/nmap-top100-$3" -v -iL $nmap_list -T3 &&  
rm $nmap_list


#extract webhosts with typical http/s ports
for x in `grep "80/open|443/open|8080/open|8443/open" "./$3-nmap/nmap-top100-$3.gnmap" | cut -f2 -d' ' | sort -u`; 
  do 
    sed -n "/$x/p" "live-hosts-$3.txt"; 
  done | cut -f1 -d',' | awk "/^[a-zA-Z]/ {print}" | sort -u | sed -E '/^\*/d;s/[^a-zA-Z0-9._-]//g' > webhosts-$3.txt
  
echo "Done!!"

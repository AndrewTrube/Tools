#!/usr/bin/env python3

#################################################################################
#                    **--BRUTEFORCE BACKUP FILES--**                            #
# Use a wordlist to bruteforce many types of backup file extensions.            #            
# ex: bakbruter.py mywordlist.txt http://www.example.com/path/filename 8080     #  
#                                                                               #
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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################


import sys,socket,re,time

array_backup_ext = [ '.wjf', '.quickenbackup', '.pdb', '.caa', '.tdb', '.sns', '.asvx', '.qsf', '.nbs', '.inprogress', '.pbj', '.wbx', '.dup0', '.icbu', '.ati', '.icf', '.ghs', '.bak3', '.blend2', '.$db', '.qbb', '.nwbak', '.llx', '.jps', '.sis', '.bbb', '.gho', '.wbk', '.mbf', '.gb1', '.pbb', '.bpa', '.ptb', '.__b', '.qbmd', '.fhf', '.exml', '.orig', '.pvhd', '.backup1', '.diy', '.fwbackup', '.lcb', '.qbm', '.arc', '.vbm', '.sav', '.nco', '.bkc', '.bkp', '.bmk', '.ba6', '.cenon~', '.aba', '.fbc', '.ftmb', '.mpb', '.fpsx', '.ab', '.nps', '.sdc', '.ccctask', '.afi', '.ibk', '.jbk', '.pbx5script', '.bif', '.vbk', '.ba7', '.mddata', '.dpb', '.nfb', '.sps', '.win', '.yrcbck', '.pqb-backup', '.$$$', '.oeb', '.rbk', '.bpn', '.kmnb', '.asv', '.nba', '.pbd', '.mbw', '.noy', '.sbb', '.ttbk', '.bps', '.cbu', '.bff', '.bm3', '.bpb', '.abbu', '.abu1', '.abu', '.73b', '.mdinfo', '.blend1', '.flkb', '.vpcbackup', '.dbk', '.acr', '.sbs', '.nbk', '.tibx', '.jdc', '.adi', '.nb7', '.fbw', '.msim', '.mv_', '.bkz', '.dsb', '.~cw', '.safenotebackup', '.vpb', '.sv$', '.aea', '.wx', '.csm', '.bup', '.ful', '.nbak', '.sqb', '.backup', '.bkf', '.mabk', '.bifx', '.ba0', '.nrs', '.psa', '.ashbak', '.snmm', '.tibkp', '.sna', '.acp', '.gb2', '.imazing', '.tis', '.bkup', '.uci', '.xbk', '.001', '.mig', '.bak~', '.bak2', '.nbf', '.sv2i', '.wbb', '.nbd', '.nfc', '.pdu', '.pbxscript', '.pbf', '.bckp', '.bk1', '.tmr', '.113', '.ebabackup', '.abf', '.jpa', '.rbf', '.spf', '.bck', '.wspak', '.nbi', '.old', '.mem', '.kb2', '.lbf', '.pba', '.qbk', '.sbu', '.003', '.spg', '.vrb', '.ldabak', '.abk', '.w01', '.fza', '.asd', '.mbk', '.onepkg', '.__a', '.nda', '.dss', '.cbk', '.pvc', '.qbmb', '.sall', '.wpb', '.srr', '.cmf', '.tmp', '.bdb', '.abex', '.iv2i', '.nrbak', '.qic', '.dba', '.gs-bck', '.fbf', '.dov', '.trn', '.sme', '.rdb', '.bak', '.mdbackup', '.rmbak', '.ba9', '.wbcat', '.pfi', '.fbk', '.rmgb', '.obk', '.walletx', '.prv', '.stg', '.mynotesbackup', '.ori', '.flka', '.tini', '.tig', '.quicken2015backup', '.oyx', '.ck9', '.zbfx', '.ate', '.yoti', '.fzb', '.npf', '.csd', '.gbp', '.quicken2017backup', '.bpm', '.dna', '.quicken2016backup', '.ba8', '.bcm', '.paq', '.rbc', '.qba.tlg', '.bbz', '.qbx', '.tlg', '.sim', '.bac', '.bookexport', '.cbs', '.qualsoftcode', '.vbox-prev', '.002', '.bakx', '.dim', '.nbu', '.ipd', '.sn1', '.as4', '.backupdb', '.da0', '.rbs', '.tbk', '.spi', '.v2i', '.crds', '.dash', '.sn2', '.pqb', '.xlk', '.aqz', '.fbu', '.fh', '.j01', '.rrr', '.qv~', '.imazingapp', '.skb','~']

def con():
    context = ssl.create_default_context()
    host = (sys.argv[2], int(sys.argv[3])
    try:
        sock = socket.create_connection(host)
        ssock = context.wrap_socket(sock, server_hostname=host[0]) 
        return ssock
    except:
        host = (sys.argv[2], int(sys.argv[3])        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(host)
        return sock 
        
def brute():
    with open(sys.argv[1]) as fd:
        wlist = fd.readlines()
        soc = con()
        for x in wlist:
            for y in array_backup_ext:
                payload = "HEAD %s/%s.%s HTTP/1.1\r\nConnection: keep-alive\r\nHost: %s\r\n\r\n" \
                % (sys.argv[2], re.sub(r"\s+","_",x), y, sys.argv[2]) 
                soc.send(payload)
                data = soc.recv(1024)
                result = re.search("(200 OK|302 Found)", data)
            if result:
                print(result.group(0), x)
    soc.close()
                       
def main():
    if len(sys.argv) != 4:
        print("Usage: bakbruter.py WORDLIST URL PORT")
        exit(0)
    brute()
    
if __name__ == "__main__":
    main()

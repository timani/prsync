#!/usr/bin/python

# The MIT License (MIT)
# Copyright (c) <year> <copyright holders>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, merge, # publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
import argparse, os, subprocess, string
 
def process_req(app):     
    results = app.parse_args()  
    print 'Validating local directory...'
    valid = validate_ldir(results.ldir)
    values = {'ldir' : results.ldir, 'env': results.env, 'uuid' : results.uuid, 'rdir': results.rdir}
    if results.op == 'up' and valid:
        print "Starting upload..."          
        c = string.Template("rsync -rlvz --ipv4 --progress -e 'ssh -p 2222' $ldir $env.$uuid@appserver.$env.$uuid.drush.in:$rdir").substitute(values) 
        p = subprocess.Popen([c], shell=True, stdout=subprocess.PIPE) 
    elif results.op == 'dl' and valid:
        print "Starting download..."
        c = string.Template("rsync -rlvz --ipv4 --progress -e 'ssh -p 2222' $env.$uuid@appserver.$env.$uuid.drush.in:$rdir  $ldir").substitute(values)  
        p = subprocess.Popen([c], shell=True, stdout=subprocess.PIPE)
               
    if valid: 
        for line in p.stdout:
        #the real code does filtering here
            print line.strip()        
        
def validate_ldir(ldir):        
    if os.path.exists(ldir): 
        return True
    else:
        #file or directory not found 
        print 'ERROR: The file or directory was not found: ', ldir 
        return False
    
def main():
    parser = argparse.ArgumentParser(  
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''Pantheon RSYNC Tool\n-------------------------------------------------\nUpload, Download and Transfer files between\ndifferent locations.\n
For additional help with a command use the -h flag:\nup -h\r
up sites/default/files* dev 23098rncu3-8-38-12y89ef-8-08wr7 sites/default/\r
up ./ dev 23098rncu3-8-38-12y89ef-8-08wr7 ./ # Entire Drupal Dir\r
\dl sites/default/ dev 23098rncu3-8-38-12y89ef-8-08wr7 sites/default/files/\r 
''',
        version=1.0, 
        )
    
    subparsers = parser.add_subparsers(dest="op")

    # create the parser for the "up" command
    parser_upload = subparsers.add_parser('up',help='Upload files to Pantheon')
    up_group = parser_upload.add_argument_group('Upload options (Required)')
    up_group.add_argument('ldir',  help='Local directory', metavar='./files*') 
    up_group.add_argument('env',  help='Environment', choices=['dev','live','test']) 
    up_group.add_argument('uuid',  help='UUID') 
    up_group.add_argument('rdir', help='Remote directory', metavar='sites/default/files/')  

    # create the parser for the "dl" command
    parser_download = subparsers.add_parser('dl',help='Download files from Pantheon')
    dl_group = parser_download.add_argument_group('Download options (Required)')
    dl_group.add_argument('ldir', help='Local directory', metavar='./files*') 
    dl_group.add_argument('env',  help='Environment',  choices=['dev','live','test']) 
    dl_group.add_argument('uuid',  help='UUID') 
    dl_group.add_argument('rdir', help='Remote directory', metavar='sites/default/files/') 

    process_req(parser)
 
if __name__ == '__main__':
    main()


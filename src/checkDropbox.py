#!/usr/bin/env python
###############################################################################################
#  Author: 
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
_name = 'checkDropbox'
# Descrip: 
_description = '''Check if there are errors or inconsistencies in dropbox folder'''
# Version: 
_version = '0.0.1'
#    Date:
_date = '20101104'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 0.0.1 (20101104)
#            -Initial release
###############################################################################################

# Imports
import logging
import sys
import doctest
import datetime, time
import os
import subprocess
import optparse
import inspect
import glob

# Parameters, Globals n' Constants
TEMP_FILE = "/tmp/checkDropbox.tmp"
gmail_user="enteryours"
gmail_pwd="enteryours"
callingDirectory = os.getcwd()
scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)

# User-libs imports (This is the correct way to do this)
LIB_PATH = scriptDir + os.path.sep + '..' + os.path.sep + 'lib'
for infile in glob.glob(os.path.join(LIB_PATH, '*.*')):
    sys.path.insert(0, infile)
    
import shellutils
import generalutils

# Usage function, logs, utils and check input
def checkInput():
    '''This function is for treat the user command line parameters.
    '''

    #Create instance of OptionParser Module, included in Standard Library
    p = optparse.OptionParser(description=_description,
                              prog=_name,
                              version=_version,
                              usage='''%prog <DropboxPath> <eMail>''') 
    
    #Parse the commandline
    options, arguments = p.parse_args()

    #Decide what to do
    if len(arguments) != 2 :
        p.print_help()
        sys.exit(-1)
        
    else:
        return arguments

# Helper functions
def thereAreErrors(dropboxPath):
    '''This procedure checks the whole dropbox tree looking for errors 
    '''
    code, output, error = shellutils.run(["find", dropboxPath])
    return shellutils.grep("Case Conflict", output)
    
# Main function
def main(dropboxPath, email):
    '''This is the main procedure
    '''
    line = "* * * * * " + scriptPath + " " + dropboxPath + " " + email
    
    if not generalutils.isInCron(line):
        generalutils.setCron(line)
       
    errors = thereAreErrors(dropboxPath) 
    if errors != None:
        print errors
        generalutils.mail(gmail_user, gmail_pwd, email, _name + " report", str(errors))

# Entry point
if __name__ == '__main__':
    parameters = checkInput()
    main(dropboxPath=parameters[0], email=parameters[1])

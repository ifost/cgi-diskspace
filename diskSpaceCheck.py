#!/usr/bin/env python


background = 'white'
criticalColour = 'orange'
warningColour = 'blue'
normalColour = 'lightgreen'
freeColour = 'gray'

criticalLevel = 90
warningLevel = 80

print "Content-type: text/html"
print

import os
import string
#import getopts
import sys
import re

mount_output = os.popen('mount').readlines()

hostname = os.uname()[1]
dict = {'hostname': hostname,
        'background' : background
        }

heading = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
 <title>Disk Space Free on %(hostname)s</title>
</head>

  <body bgcolor="white">
    <h1>Disk Space Free on %(hostname)s</h1>
""" % dict

print heading

maximum_filesystem = 0
for m in mount_output:
    sp = string.split(m)[2]
    (blocksize, frsize,blocks, bfree, bavail, files, ffree, favail, flag, namemax) = os.statvfs(sp)
    blocks = blocks * 4
    if blocks > maximum_filesystem: maximum_filesystem = blocks
    


filesystems = []
for m in mount_output:
    sp = string.split(m)[2]
    (blocksize, frsize,blocks, bfree, bavail, files, ffree, favail, flag, namemax) = os.statvfs(sp)
    if blocks == 0: continue  # e.g. /proc
    # some magic numbers,  don't know why they're necessary
    blocks = blocks * 4
    bfree = bfree * 2
    bavail = bavail * 2
    used = blocks - bfree
    # now,  we've used up 10% of the width,  so our multiplier is 90 not 100
    free_percentage = (bfree *1.0 / blocks) * 90
    used_percentage = (used * 1.0 / blocks) * 90
    if used_percentage >= criticalLevel:
        colour = criticalColour
    elif used_percentage >= warningLevel:
        colour = warningColour
    else:
        colour = normalColour
    dict = {'background' : background,
            'usedcolour': colour,
            'usedwidth' : used_percentage,
            'used' : used,
            'freecolour' : freeColour,
            'freewidth' : free_percentage,
            'free' : bfree,
            'fs' : sp}
    

    body = """
    <table width="95%%">
    <tr> <td bgcolor="%(background)s" width="10%%"><b>%(fs)s</b></td>
    <td bgcolor="%(usedcolour)s" width="%(usedwidth)d%%">%(used)d Mb used</td>
    <td bgcolor="%(freecolour)s" width="%(freewidth)d%%">%(free)d Mb free</td>
    <!--	<td bgcolor="white" width="10%%">&nbsp;</td> -->
    </tr>
    </table>
    """ % dict

    print body

trailer = """	
  </<body>
</html>
"""

print trailer


    

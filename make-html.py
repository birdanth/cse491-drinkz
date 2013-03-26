#! /usr/bin/env python

import os

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

try:
    os.mkdir('html/subdir')
except OSError:
    # already exists
    pass

###

fp = open('html/index.html', 'w')
print >>fp, "Hello, world.<p><a href='link.html'>this is a relative link</a>"

print >>fp, """
<p>
<a href='subdir/table.html'>Here is a link</a> to a file in subdir/:
"""

fp.close()

###

fp = open('html/subdir/table.html', 'w')

print >>fp, """
<ul>
<li> Unordered
<li> list
</ul>
<p>
<ol>
<li> Ordered
<li list
</ol>
<p>
A table:
<table>
 <tr>
  <td>Row 1, col 1</td>
  <td>Row 1, col 2</td>
 </tr>
 <tr>
  <td>Row 2, col 1</td>
  <td>Row 2, col 2</td>
 </tr>
 <tr><td colspan=1>Note, you can nest <a href='table.html'>things like links</a> in tables</td></tr>
</table>
"""

fp.close()

###

fp = open('html/catastrophe.html', 'w')

print >>fp, """
<tr><td> <h3>This <width="25%" align="left"></td></tr><tr><td> <h3>is <width="25%" align="left"></td></tr><tr><td> <h3>an <width="25%" align="left"></td></tr><tr><td> <h3>ascending <width="25%" align="left"></td></tr><tr><td> <h3>catastrophe <width="25%" align="left"></td></tr><tr><td> <h3>QUICK! <width="25%" align="left"></td></tr><tr><td> <h3>close <width="25%" align="left"></td></tr><tr><td> <h3>the <width="25%" align="left"></td></tr><tr><td> <h3>h3 <width="25%" align="left"></td></tr><tr><td> <h3>tags! <width="25%" align="left"></td></tr>
"""

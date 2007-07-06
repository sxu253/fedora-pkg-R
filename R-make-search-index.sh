#!/bin/bash

# Figure out what RHOME is set to
TMP_R_HOME=`R RHOME`

# Write out all the contents in arch and noarch library locations
cat $TMP_R_HOME/library/*/CONTENTS > $TMP_R_HOME/doc/html/search/index.txt 2>/dev/null
cat /usr/share/R/library/*/CONTENTS >> $TMP_R_HOME/doc/html/search/index.txt 2>/dev/null

exit 0


#!/bin/bash

# Figure out what RHOME is set to
TMP_R_HOME=`R RHOME`

# Figure out what R_DOC_DIR is set to
# Ideally, we could ask R just like we do for RHOME, but we can't yet.
TMP_R_DOC_DIR=`grep "R_DOC_DIR=" /usr/bin/R | cut -d "=" -f 2`

# Write out all the contents in arch and noarch library locations
cat $TMP_R_HOME/library/*/CONTENTS > $TMP_R_DOC_DIR/html/search/index.txt 2>/dev/null
cat /usr/share/R/library/*/CONTENTS >> $TMP_R_DOC_DIR/html/search/index.txt 2>/dev/null

exit 0


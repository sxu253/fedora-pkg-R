#!/bin/bash

# Figure out what RHOME is set to
TMP_R_HOME=`R RHOME`

# Figure out what R_DOC_DIR is set to
# Ideally, we could ask R just like we do for RHOME, but we can't yet.
TMP_R_DOC_DIR=`grep "R_DOC_DIR=" /usr/bin/R | cut -d "=" -f 2`

# Write out all the contents in arch library locations
cat $TMP_R_HOME/library/*/CONTENTS > $TMP_R_DOC_DIR/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute TMP_R_HOME
sed -i "s!../../..!$TMP_R_HOME!g" $TMP_R_DOC_DIR/html/search/index.txt

# Write out all the contents in noarch library locations
cat /usr/share/R/library/*/CONTENTS >> $TMP_R_DOC_DIR/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute /usr/share/R
sed -i "s!../../..!/usr/share/R!g" $TMP_R_DOC_DIR/html/search/index.txt

exit 0


# Some R modules are not smart enough to ask R for the value of RHOME
# and instead depend on the R_HOME environment variable.
set RHOME = `R RHOME`
setenv R_HOME $RHOME

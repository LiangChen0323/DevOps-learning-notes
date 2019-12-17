Shell Variables
set Shows shell variables for the current instance of the running shell Set your own shell variables: EXAMPLE=VAR ; echo $EXAMPLE
Creates the shell variable EXAMPLE and sets the value to VAR , then prints the variable's value Remove shell variables: unset EXAMPLE ; echo $EXAMPLE
Removes the shell variable EXAMPLE ; echo will show no display since \$EXAMPLE is no longer set to any value

Environment Variables
env Shows all environment variables
env | grep EXAMPLE Prints current environment variables and then greps the result for the term EXAMPLE export EXAMPLE=VAR Exports shell variable EXAMPLE to the environment variables
EXAMPLE=VAR ; export EXAMPLE Exports a previously-defined shell variable to the environment variables
After you log off, the environment variables you set will restore to default. To permanently set an environment variable, you must either edit the user configuration files or global configuration files for Bash.
Add to .bashrc (for user): ABC="123"; export ABC
Add to /etc/.bash.bashrc (for system): ABC="123"; export ABC

Common Environment Variables
DISPLAY X display name
EDITOR Name of default text editor
HISTCONTROL History command control options
HOME Path to home directory
HOSTNAME Current hostname
MAIL Holds the location of the user mail spools
LD_LIBRARY_PATH Directories to look for when searching for shared libraries PATH Executable search path
PS1 Current shell prompt
PWD Path to current working directory
SHELL Path to login shell
TERM Login terminal type
USER / USERNAME Current user's username
VISUAL Name of visual editor

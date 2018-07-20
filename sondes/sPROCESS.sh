# Nombre de processus
ps -A | wc -l

# Nombre de processus root
ps -aux | cut -d" " -f1 | grep 'root' | wc -l

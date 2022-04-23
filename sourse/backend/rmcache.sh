find . -path "*/*.pyc"  -delete
find . -path "*/*.pyo"  -delete
find . -path "*/__pycache__" -type d -exec rm -r {} ';'

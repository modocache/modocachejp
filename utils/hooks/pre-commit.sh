#!/bin/sh


set -e
set -u


if git-rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi


for file in `git diff-index --name-status $against -- | cut -c3-`; do
    
    # Check requirements.txt on update
    if [ "$file" = "requirements.txt" ]; then

        echo "[PRE-COMMIT] Testing validity of requirements.txt"
        
        pip install --no-install -r $file
        install_result=$?

        if [ $install_result -ne "0" ]; then
            echo "[PRE-COMMIT/ERROR] pip install -r --no-install $file failed."
            exit 1
        fi

    fi

done

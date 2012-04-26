#!/bin/sh


set -e
set -u


pushd `dirname "${0}"` > /dev/null
hook_dir=`pwd -L`
popd > /dev/null


prj_dir="`dirname $(dirname $hook_dir)`"


cp "$hook_dir/pre-commit.sh" "$prj_dir/.git/hooks/pre-commit"

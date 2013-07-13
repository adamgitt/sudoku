#!/bin/sh
intltool-update --pot --gettext-package=gnome-sudoku
for f in */LC_MESSAGES/*.po
do
echo Merging new translations into $f
msgmerge -U $f gnome-sudoku.pot
done

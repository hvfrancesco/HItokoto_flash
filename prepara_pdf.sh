#! /bin/sh

gs -o Hitokoto_flash_A5.pdf -sDEVICE=pdfwrite -sPAPERSIZE=a4 -dFIXEDMEDIA -dPDFFitPage -dCompatibilityLevel=1.5 $1
pdfbook --short-edge --suffix 'libro' Hitokoto_flash_A5.pdf
rm Hitokoto_flash_A5.pdf
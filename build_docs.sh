#! /bin/bash

cd `pwd`/docs;make html;make latex;cd _build/latex;make all-pdf
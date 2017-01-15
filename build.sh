#! /bin/bash

pip install -r requirements.txt -t ./lib
zip -rq9 lambda.zip * -x@exclude.txt

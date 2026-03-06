#!/bin/bash

echo "Creating data directories..."

mkdir -p data/raw

echo "Downloading Enron Email Dataset..."

curl -L https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz -o enron_mail.tar.gz

echo "Extracting dataset..."

tar -xzf enron_mail.tar.gz -C data/raw

rm enron_mail.tar.gz

echo "Dataset downloaded and extracted to data/raw/"
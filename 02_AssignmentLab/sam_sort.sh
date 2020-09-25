#!/bin/bash

for SEQ in *.sam
do
	samtools sort -o ${SEQ}.bam -O bam ${SEQ}
done
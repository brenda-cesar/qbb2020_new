#!/bin/bash

for SEQ in A01*
do
	bwa mem -R "@RG\tID:${SEQ}\tSM:${SEQ}" "sacCer3.fa" ${SEQ} > ${SEQ}.sam
done
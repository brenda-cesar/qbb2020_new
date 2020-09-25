#!/bin/bash

freebayes -f "sacCer3.fa" -p 1 --genotype-qualities A01_09.bam  A01_11.bam  A01_23.bam  A01_24.bam  A01_27.bam  A01_31.bam  A01_35.bam  A01_39.bam  A01_62.bam  A01_63.bam | vcffilter -f "QUAL > 20" > GeneVariants_Filtered.vcf
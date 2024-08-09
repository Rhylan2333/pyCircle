# scripts to prepare datasets

## calculate the length of chromosomes of each species

```shell
z data/MCscan_JCVI/
ouch d ./*.gz
z bed-format/
ouch d ./*.gz

rg '\tregion\t' ./Bmor.chr.renamed.gff | choose 0 4 -f '\t' | sd ' ' '\t' > ./chr_len.Bmor.tsv
rg '\tregion\t' ./Dmel.chr.renamed.gff | choose 0 4 -f '\t' | sd ' ' '\t' > ./chr_len.Dmel.tsv
```

## MCscan using JCVI

```shell
# mamba activate jcvi_env
z data/MCscan_JCVI/

mkdir -p bed-format

script -c '''
python -m jcvi.formats.gff bed --type=mRNA --key=ID ./Bmor.chr.renamed.gff -o ./bed-format/Bmor.bed
choose 3 < ./bed-format/Bmor.bed > ./Bmor.mRNA.IDlist
seqkit grep -f ./Bmor.mRNA.IDlist ./Bmor.rna.fa -o ./Bmor.rna.chr.fa

python -m jcvi.formats.gff bed --type=mRNA --key=ID ./Dmel.chr.renamed.gff -o ./bed-format/Dmel.bed
choose 3 < ./bed-format/Dmel.bed > ./Dmel.mRNA.IDlist
seqkit grep -f ./Dmel.mRNA.IDlist ./Dmel.rna.fa -o ./Dmel.rna.chr.fa

python -m jcvi.formats.fasta format ./Bmor.rna.chr.fa ./bed-format/Bmor.cds
python -m jcvi.formats.fasta format ./Dmel.rna.chr.fa ./bed-format/Dmel.cds

''' ./s0_format.log

z bed-format/

# If without --no_strip_names
# sd '\.\d+\t' '\t' ./Bmor.bed
# sd '\.\d+ ' ' ' ./Bmor.cds
# sd '\.\d+\t' '\t' ./Dmel.bed
# sd '\.\d+ ' ' ' ./Dmel.cds

script -c '''
python -m jcvi.compara.catalog ortholog Bmor Dmel --no_dotplot --self_remove=99.5 --no_strip_names
''' ./s1_pairwise-synteny-search.log

script -c '''
python -m jcvi.graphics.dotplot --qbed=./Bmor.bed --sbed=./Dmel.bed --colororientation --figsize=15x15 --dpi=300 --font=Arial --notex ./Bmor.Dmel.anchors -o ./Bmor.Dmel.dotplot.pdf
''' ./s1b_pairwise-synteny-visualization.dotplot.log

script -c '''
python -m jcvi.compara.synteny screen --simple ./Bmor.Dmel.anchors ./Bmor.Dmel.anchors.simple --qbed=./Bmor.bed --sbed=./Dmel.bed
''' ./s2_macrosynteny-visualization.screen.minspan.log

script -c '''
python -m jcvi.graphics.karyotype ../draw_fig_args/seqids.txt ../draw_fig_args/layout.txt -o ./karyotype.pdf --basepair --chrstyle=roundrect --figsize=22x10 --dpi=300 --font=Arial --notex --seed=1
''' ./s3_macrosynteny-visualization.karyotype.log

```

## adjust the chromosomes' order in seqids.txt

Order them (`./data/MCscan_JCVI/draw_fig_args/seqids.txt`) according to `./data/MCscan_JCVI/bed-format/karyotype.pdf`.

Then, change the chromosomes' order in `./data/MCscan_JCVI/chr_len.Bmor.tsv` and `./data/MCscan_JCVI/chr_len.Dmel.tsv`. Save them as `./data/chr_len.Bmor.ordered.tsv` and `./data/chr_len.Dmel.ordered.tsv`.

## about .anchors.sample

It should be in `./data/MCscan_JCVI/bed-format/Bmor.Dmel.anchors.simple`

## gene family

```shell
rg '\tgene\t' ./data/MCscan_JCVI/Bmor.chr.renamed.gff | rg 'Name=CYP' -i | choose 0 4 8 -f '\t' | sd 'ID=.+Name=' '' | sd ';.+$' '' | sd ' ' '\t' > ./data/prepare_genomic_labels.CYP450.Bmor.tsv
rg '\tgene\t' ./data/MCscan_JCVI/Dmel.chr.renamed.gff | rg 'Name=CYP' -i | choose 0 4 8 -f '\t' | sd 'ID=.+Name=' '' | sd ';.+$' '' | sd ' ' '\t' > ./data/prepare_genomic_labels.CYP450.Dmel.tsv

touch ./data/genomic_labels-CYP450.Bmor.tsv
echo -e 'chromosome\tstart\tannotation\tfill_parameters\ttext_parameters' >./data/genomic_labels-CYP450.Bmor.tsv
touch ./data/genomic_labels-CYP450.Dmel.tsv
echo -e 'chromosome\tstart\tannotation\tfill_parameters\ttext_parameters' > ./data/genomic_labels-CYP450.Dmel.tsv

touch ./data/linkinfo-CYP450.tsv
echo -e 'chromosome_1\tchr_1_start\tchromosome_2\tchr_2_start\tplot_parameters\tcomment' > ./data/linkinfo-CYP450.tsv

```

Then, prepare `./data/genomic_labels-CYP450.Bmor.tsv` and `./data/genomic_labels-CYP450.Dmel.tsv` files using `./data/prepare_genomic_labels.CYP450.Bmor.tsv` and `./data/prepare_genomic_labels.CYP450.Dmel.tsv`.

I highly recommend using a phylogenetic tree to prepare `./data/linkinfo-CYP450.tsv`.

## usie `pyCircle.ipynb`

## compress the files

```shell
z data/MCscan_JCVI/
script -c "
crabz -l 9 -p 12 ./Bmor.chr.renamed.gff -o ./Bmor.chr.renamed.gff.gz && rm -rfv ./Bmor.chr.renamed.gff
crabz -l 9 -p 12 ./Bmor.rna.chr.fa -o ./Bmor.rna.chr.fa.gz && rm -rfv ./Bmor.rna.chr.fa
crabz -l 9 -p 12 ./Bmor.rna.fa -o ./Bmor.rna.fa.gz && rm -rfv ./Bmor.rna.fa
crabz -l 9 -p 12 ./Dmel.chr.renamed.gff -o ./Dmel.chr.renamed.gff.gz && rm -rfv ./Dmel.chr.renamed.gff
crabz -l 9 -p 12 ./Dmel.rna.chr.fa -o ./Dmel.rna.chr.fa.gz && rm -rfv ./Dmel.rna.chr.fa
crabz -l 9 -p 12 ./Dmel.rna.fa -o ./Dmel.rna.fa.gz && rm -rfv ./Dmel.rna.fa
crabz -l 9 -p 12 ./bed-format/Bmor.bed -o ./bed-format/Bmor.bed.gz && rm -rfv ./bed-format/Bmor.bed
crabz -l 9 -p 12 ./bed-format/Bmor.cds -o ./bed-format/Bmor.cds.gz && rm -rfv ./bed-format/Bmor.cds
crabz -l 9 -p 12 ./bed-format/Dmel.bed -o ./bed-format/Dmel.bed.gz && rm -rfv ./bed-format/Dmel.bed
crabz -l 9 -p 12 ./bed-format/Dmel.cds -o ./bed-format/Dmel.cds.gz && rm -rfv ./bed-format/Dmel.cds
" ./s4_compress.log
```

# replace_stringtie_merge_geneid_with_locus_name
The python script `stringtieGeneIdReplace` replaces the default `StringTie Merge` `gene_id` with the gene locus name.

The RNA-seq analysis software `StringTie` is commonly used for transcriptome assembly. And the `merge` function is used to generate a combined transcripts that appears accross all samples. 
  
A very confused, sometimes misleading, part in the output .gtf file of `stringtie --merge` resides in the `gene_id` flag, where `StringTie` assigns a default name for each gene and transcript with a default prefix `MSTRG`.  
  
A user could change the default prefix by using the `-l` option, but the naming for each gene and transcript is done by `StringTie` by its alogrithm.  
  
However, this `gene_id` is not a unique identifier for all the genes. You will probably find that for some genes and transcripts, the same `gene_id` may be associated with multiple gene locus, which is specifed by the `ref_name_id` in the meraged annotation file.  
  
This will lead to errors during the next step DE analysis, such as using `Ballgown`. Because the gene level differential expression is calculated based on the `StringTie` `gene_id` flag, which will assign one `gene_id` to one `ref_gene_id`, is there is one. And if one 'gene_id' correponds multiple 'ref_gene_id'， reads from different gene locus in such case will be combined to count for a single gene where the `MSTRG.x` appears.  
  
  
To reduce the error caused by the naming, this python script search each line of the `StringTie Merge` output `.gtf` file and do the following replacement:  

1. If there is a `ref_gene_id` flag, which is the gene locus id for that gene or transcript, then replace the `MSTRG.x` in `gene_id` flag with the actual gene locus id.
2. If a `ref_gene_id` flag is not available for a gene or transcript, but the same `MSTRG.x` corresponds to another gene or transcript. Then the script will determine whether the the particular `MSTRG.x` corresponds to multiple gene locus, if not, the script will replace the only locus name associated with that `gene_id` but not the `transcript_id`.
3. If a `MSTRG.x` flag associates multiple genes and transcripts, the replace will only be done for those having a `ref_gene_id` flag.
4. If no `ref_gene_id` flag associates with a particular `MSTRG.x`, that `MSTRG.x` will be left as it is and no replacement will happen.

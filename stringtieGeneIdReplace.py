
# This is the first version of StringtieGeneIdReplace.py. This python script search each line of the StringTie Merge output .gtf file and do the following replacement:

# 1. If there is a ref_gene_id flag, which is the gene locus id for that gene or transcript,
#    then replace the MSTRG.x in gene_id flag with the actual gene locus id.
# 2. If a ref_gene_id flag is not available for a gene or transcript, but the same MSTRG.x corresponds to another gene or transcript.
#    Then the script will determine whether the particular MSTRG.x corresponds to multiple gene locus,
#    if not, the script will replace the only locus name associated with that gene_id but not replace the transcript_id in the same line.
# 3. If a MSTRG.x flag associates multiple genes and transcripts, the replace will only be done for those having a ref_gene_id flag.
# 4. If no ref_gene_id flag associates with a particular MSTRG.x, that MSTRG.x will be left as it is and no replacement will happen.


import re

## Read the .gtf file and store each line as element in a list
with open(r"F:\Zhenhua_RNA_Seq\7.transcripts_assemble\unique_DESeq2\stringtie_merged.gtf") as file_obj:
    file_list = file_obj.readlines()


## Define an empty list and an empty dictionary to temporarily store the variables.
id_dict = {}
temp_list = []

## Loop through each line of the .gtf file
for line in file_list:

##  StringTie output has two lines in the beginning started with '#',
##  skip those lines.
    if line[0] is not '#':

##      Regular expression to find all the strings in a double quote "",
##      store the matches in a list, the first element of this list for each line is the 'MSTRG.x';
##      the list element of this list may be the locus name.
        r = re.findall('"(.+?)"', line)

##      Regular expression to match Arabidopsis Locus pattern
        id_pattern = 'AT[1-5CM]G\d{5}'

##      Determines if a 'ref_gene_id', that is with a Locus name, in the line.
        if re.match(id_pattern, r[-1]):

##          If there is a locus name, then determines if the locus name is in the dictionary.
##          if it is, make the replacement, and add the changed line to a temporary list;
##          if it isn't, add the locus name to the temporary dict, then do the replacement.
            if r[-1] in id_dict:
                temp_list.append(line.replace(r[0], r[-1]))
            else:
                id_dict[r[-1]] = r[0]
                temp_list.append(line.replace(r[0], r[-1]))

##      If there is no locus name in that line, just add that line to the temopary list as it is.
        else:
            temp_list.append(line)


## After the first round of iteration, get the values and keys of the dictionary.
## And define an other empty list to store the final lines for output.
id_values = list(id_dict.values())
id_keys = list(id_dict.keys())
out_list = []

## Loop over the first temporary list to deal with the lines with 'MSTRG.x' tags.
for line in temp_list:

##  Again, find all the strings in the double quote.
    r = re.findall('"(.+?)"', line)

##  If the first element of r has 'MSTRG', then count that particular 'MSTRG.x' in the temporary dictionary.
    if 'MSTRG' in r[0]:

##      If the particular 'MSTRG.x' appears only once, meaning now only one locus name associates with it,
##      then replace that locus name with the 'MSTRG.x' and append it to the second temporary list.
        
##      If the particular 'MSTRG.x' appears more than once, meaning it is hard to assign a locuse name to it,
##      then make no change, just append the line to the list.
        mstrg_count = id_values.count(r[0])
        if mstrg_count == 1:
            locus = id_keys[id_values.index(r[0])]
            out_list.append(line.replace(r[0], locus, 1))
        else:
            out_list.append(line)

##  If there is no 'MSTRG' in the first element of r, meaning the replacement has been done in the first loop,
##  then make no change, just append that line to the output list.
    else:
        out_list.append(line)


## Join each element of the output list as a string
out_file_str = ''.join(out_list)

## Write the final string into a new .gtf file.
with open(r'F:\Zhenhua_RNA_Seq\7.transcripts_assemble\unique_DESeq2\modified_stringtie_merged.gtf', 'w') as output:
    output.write(out_file_str)


            


        

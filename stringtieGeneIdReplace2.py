
# This version of the script optimized for R package DESeq2 that is used to do the DE gene analysis.
#
# It comes to the attention that DEseq2 will take both 'gene_id' and 'gene_name' flag to differentiate different genes,
# in the final DE gene result, users would see each rowname is in the format of "gene_id|gene_name".
#
# Therefore, for those transcripts or genes that went through the ID replacement of the first version of this script,
# if the 'MSTRG.x' corresponds to only one 'ref_gene_id' and may have a transcript that has the same 'MSTRG.x' but without a 'ref_gene_id',
# then you will likely end up with the same 'ref_gene_id' having two seperate gene identities in the DE gene list.
#
# For example: 'MSTRG.16185' corresponds to 'AT5G07190', and there is another transcript with the same 'MSTRG.16185', but no 'ref_gene_id'
# After the replacement by the first version of this script, you will find a duplicated 'AT5G07190' in the DEseq2 DE gene list, like this:
# AT5G07190|ATS3
# AT5G07190
#
# Because the program considers the ones with no 'ref_gene_id' as a different gene. This introduced a little inaccuracy of the analysis.
#
# To sovle this, this script will consider those transcrips, which does not have a 'ref_gene_id'
# but with a 'MSTRG.x' which assocites with a single unique 'ref_gene_id', as a new transcript without replacing the 'MSTRG.x' by the unique 'ref_gene_id',
# whereas adds an extra flag 'gene_name' in the end of the line with the corresponding single 'ref_gene_id' as the value of that flag.
#
# Therefore, in the DESeq2 final list, you would see something like this
# AT5G07190|ATS3
# MSTRG.16185|AT5G07190
#
# Genes like these 'MSTRG.16185|AT5G07190' can be filtered for either been removed from the list or for further analysis.


import re
import argparse


parser = argparse.ArgumentParser(description="Make your Gene Id more accurate in Stringtie and DESeq2 output")
parser.add_argument("Input_file", help="File names for input, including path if needed")
parser.add_argument("Output_file", help="File names for output, including path if needed")
args = parser.parse_args()
inputpath = args.Input_file
outputpath = args.Output_file

# Read the .gtf file and store each line as element in a list
with open(inputpath) as file_obj:
    file_list = file_obj.readlines()


# Define an empty list and an empty dictionary to temporarily store the variables.
id_dict = {}
temp_list = []

# Loop through each line of the .gtf file
for line in file_list:

    # StringTie output has two lines in the beginning started with '#',
    # skip those lines.
    if line[0] != '#':

        # Regular expression to find all the strings in a double quote "",
        # store the matches in a list, the first element of this list for each line is the 'MSTRG.x';
        # the list element of this list may be the locus name.
        r = re.findall('"(.+?)"', line)

        # Regular expression to match Arabidopsis Locus pattern
        id_pattern = 'AT[1-5CM]G\d{5}'

        # Determines if a 'ref_gene_id', that is with a Locus name, in the line.
        if re.match(id_pattern, r[-1]):

            # If there is a locus name, then determines if the locus name is in the dictionary.
            # if it is, make the replacement, and add the changed line to a temporary list;
            # if it isn't, add the locus name to the temporary dict, then do the replacement.
            if r[-1] in id_dict:
                temp_list.append(line.replace(r[0], r[-1]))
            else:
                id_dict[r[-1]] = r[0]
                temp_list.append(line.replace(r[0], r[-1]))

        # If there is no locus name in that line, just add that line to the temopary list as it is.
        else:
            temp_list.append(line)


# After the first round of iteration, get the values and keys of the dictionary.
# And define an other empty list to store the final lines for output.
id_values = list(id_dict.values())
id_keys = list(id_dict.keys())
out_list = []

# Loop over the first temporary list to deal with the lines with 'MSTRG.x' tags.
for line in temp_list:

    #  Again, find all the strings in the double quote.
    r = re.findall('"(.+?)"', line)

    #  If the first element of r has 'MSTRG', then count that particular 'MSTRG.x' in the temporary dictionary.
    if 'MSTRG' in r[0]:
        mstrg_count = id_values.count(r[0])

        # If the particular 'MSTRG.x' appears only once, meaning now only one locus name associates with it,
        # then remove the \n character in the current line,
        # add a gene_name tag with the corresponding locus name in double quote, and end with a new \n;
        # then append it to the second temporary list.

        # If the particular 'MSTRG.x' appears more than once, meaning it is hard to assign a locuse name to it,
        # then make no change, just append the line to the list.
        if mstrg_count == 1:
            locus = id_keys[id_values.index(r[0])]
            out_list.append(line.rstrip() + ' gene_name ' + '"' + locus + '"; \n')
        else:
            out_list.append(line)

    # If there is no 'MSTRG' in the first element of r, meaning the replacement has been done in the first loop,
    # then make no change, just append that line to the output list.
    else:
        out_list.append(line)


# Join each element of the output list as a string
out_file_str = ''.join(out_list)


# Write the final string into a new .gtf file.
with open(outputpath, 'w') as output:
    output.write(out_file_str)

import re

with open(r'F:\Zhenhua_RNA_Seq\7.transcripts_assemble\stringtie_merged.gtf') as file_obj:
    file_list = file_obj.readlines()


id_dict = {}
temp_list = []

for line in file_list:
    if line[0] is not '#':
        r = re.findall('"(.+?)"', line)
        if 'AT' in r[-1]:
            if r[0] in id_dict:
                temp_list.append(line.replace(r[0], r[-1]))
            else:
                id_dict[r[-1]] = r[0]
                temp_list.append(line.replace(r[0], r[-1]))

        else:
            temp_list.append(line)


id_values = list(id_dict.values())
id_keys = list(id_dict.keys())
out_list = []

for line in temp_list:
    r = re.findall('"(.+?)"', line)
    if 'MSTRG' in r[0]:
        mstrg_count = id_values.count(r[0])
        if mstrg_count == 1:
            locus = id_keys[id_values.index(r[0])]
            out_list.append(line.replace(r[0], locus, 1))
        else:
            out_list.append(line)
    else:
        out_list.append(line)


out_file_str = ''.join(out_list)

with open(r'F:\Zhenhua_RNA_Seq\7.transcripts_assemble\modified_stringtie_merged.gtf', 'w') as output:
    output.write(out_file_str)


            


        

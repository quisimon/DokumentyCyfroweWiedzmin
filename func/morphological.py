import morfeusz2

name = "Gerard"

# analizator
morfeusz = morfeusz2.Morfeusz()
variant_list = morfeusz.analyse(name)

for v in variant_list:
    ign1, ign2, an, *ign3 = v
    flect, lemma, tags, types, *ign = an
    if "imię" in types:
        tag_list = tags.split(":")
        gender = tag_list[-1]

flex_list = morfeusz.generate(name)
for f in flex_list:
    voc, ign1, tags, *ign2 = f
    tag_list = tags.split(":")
    if 'voc' in tag_list:
        name_voc = voc

print(name_voc)
#!/usr/bin/env python3

# translit.py
# 
# Transliteration tools for bibliographic data
# 
#   Version 0.1.4
#   Copyright 2022 Enabling Languages.
#   Released under MIT license.

from icu import Transliterator, UTransDirection
import unicodedata as ud
import regex as re

#from string import punctuation

# test_strings = [
#     "Bot lāingān kīeokap kānsāng khit khwāmsāmāt nai kānvāngphǣn thāng kānngœ̄n phư̄a phatthanā læ khanyāi kitchakān kānphalit khǭng khǭpkhūa / hīaphīang pen phāsā ʻĀngkit doī, Thǭ. ʻInping Manīvong, Nǭ. Somchai Sulitham ; pǣ doī, DǭRǭ. Tīam Vannasuk ; kūatkǣ doī, Thǭ. Yungthǭng Sīthāmāt, Nǭ. Thǭngsavāt Bupphā.",
#     "Kō̜n cha mī Mư̄ang Vīang Sai thān thīman kānpativat : bot banthưk khwāmsongcham / Somphō̜n Sīsuvanna. Phim khang thī 1. [Viangchan, Laos] : Samnakphim Nakpaphan Lāo, 2019.",
#     "Lom hāi chai khō̧ng phǣndin / Kom Khāosān Mǣnying Lāo Sūn Kāng Sahāphan Mǣnying Lāo. Phim khang thī nưng. Vīangchan : Lāo Dūangdư̄an, 2019.",
#     "Sēnthāng sū santiphāp / khonkhwā læ hīaphīang, Suli Detvongphan.  Phim khang thi 1. Nakhō̜n Lūang Vīangchan : Samnakphim Sīkhīeo, 2019.",
#     "Khwamcheppūat thi suaingam / Sǭnsai Khūnmanī.  Phim khang thi nung. Viangchan : Lao Dūangdư̄an, 2019."
# ]


test_strings = [
    "Khwamcheppūat thi suaingam / Sǭnsai Khūnmanī.  Phim khang thi nung. Viangchan : Lao Dūangdư̄an, 2019."
]

# temp = test_str.split()
# res = []
# for wrd in temp:
#     res.append(repl_dict.get(wrd, wrd))
# res = ' '.join(res)
# print("\n\n" + res)
# print(type(res))

# def to_native(bib_data, translit_table="lao", dir="reverse"):
#     if translit_table == "lao":
#         print("in lao")
#         from laoo_t_latn_m0_ALALOC import translit_dict, translit_rules
#         word_dict = translit_dict[dir]
#         label = "Lao-Latin/ALALOC"
#         #custom_transliterator = Transliterator.createFromRules(label, translit_rules, UTransDirection.REVERSE)
#         res = " ".join(word_dict.get(ele, ele) for ele in bib_data.split())
#         translit_result = res
#         #translit_result = custom_transliterator.transliterate(res)
#     else:
#         translit_result = bib_data
#     return translit_result

def prep_string(s, d, b):
    if d.lower() == "reverse" and b.lower() != "both":
        s = s.lower()
    s = ud.normalize('NFD', s)
    s = s.replace("\u0327", "\u0328").replace("\u031C", "\u0328")
    return ud.normalize('NFC', s)

# temp = test_str.split()
# res = []
# for wrd in temp:
#     res.append(repl_dict.get(wrd, wrd))
# res = ' '.join(res)
# print("\n\n" + res)
# print(type(res))

# direction (dir) = direction of transliteration ; forward (to Latin) | reverse (from Latin) 
# bicameral script (bicameral) = latin_only | both
def to_native(bib_data, translit_table="laoo_t_latn_m0_ALALOC", dir="reverse", bicameral="latin_only" ):
    bib_data = prep_string(bib_data, dir, bicameral)
    word_dict = {}
    if translit_table == "laoo_t_latn_m0_ALALOC":
        from laoo_t_latn_m0_ALALOC import translit_dict, translit_rules
        word_dict = translit_dict[dir]
        label = "Lao-Latin/ALALOC"
        #custom_transliterator = Transliterator.createFromRules(label, translit_rules, UTransDirection.REVERSE)
        #res = " ".join(word_dict.get(ele, ele) for ele in bib_data.split())
        bib_data_split = re.split('(\W+?)', bib_data)
        res = "".join(word_dict.get(ele, ele) for ele in bib_data_split)
        translit_result = res
        #translit_result = custom_transliterator.transliterate(res)
    else:
        translit_result = bib_data
    return translit_result


for i in test_strings:
    print("Original string:\n" + i + "\n")
    print("Transformed string:\n" + to_native(i) + "\n")

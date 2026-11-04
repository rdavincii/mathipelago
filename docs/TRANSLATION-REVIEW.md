# Bahasa Melayu wording to have reviewed by a native-speaker teacher

The Malay text was written by an AI assistant and has **not** been reviewed by a person. Treat all of it as draft.
Items where wording choice is most uncertain:

| Where | Choice made | Question for the reviewer |
|---|---|---|
| `skill.sharing` / share puzzles | "Perkongsian adil (bahagi)", "Kongsi … dengan adil" | Is "kongsi" the right school-level word for dividing equally (vs "agih")? |
| Place value | "Sa, Puluh, Ratus, Ribu" | Confirm "sa" (ones) matches what pupils learn. |
| Perimeter / shapes | "perimeter", "segi empat sama", "segi empat tepat", "layang-layang", "rombus", "trapezium" | Confirm standard KSSR terms. |
| Data / averages | "min (purata)", "carta palang" | Confirm terms for Year 6 level. |
| Ratio | "nisbah", "sukatan" for "batch" in the festival drink problem | Is "sukatan" natural here? Maybe "adunan"/"kali". |
| Negative numbers | "−3", "di bawah sifar", "suhu turun" | Natural phrasing for pupils. |
| Ranks | "Peneroka, Pengembara, Peneroka Mahir" | Do these feel right for ages 7 to 12? |
| Feedback strings | "Alamak", "Jom", "Sedikit lebih tinggi!" | Tone appropriate for school-age children and parents. |
| Parents' text | privacy / storage paragraphs | Formal register acceptable? Legal wording must come from a lawyer. |
| `fb.numberIs` | "nombor yang paling kecil/besar" | Grammar when `{goal}` is substituted. |

| Fractions / decimals | "pecahan", "perpuluhan", "peratus", "min (purata)", "poligon", "heksagon", "pentagon" | Confirm terms and that "nisbah 1 : 3" reads naturally. |
| Pals | "Habuan" (treat), "Belai" (pet), "Kawan super", "Baru kenal" | Are these natural and kind for children? |
| Dashboard | "Papan pemuka", "Sedang belajar / Semakin maju / Kuat" | Confirm wording for skill levels. |
| Test banner | "MOD UJIAN: pek premium dibuka untuk ujian sahaja" | Only needed while test mode is on. |

| New skills and islands (levels 25 to 212) | "Masa (jam, minit, saat)", "Nombor negatif", "Pembundaran dan anggaran", "Nisbah", "Gandaan", "Faktor", "Tatasusunan dan baris" | Confirm skill names. |
| Generated level text | many levels share sentence patterns ("Selesaikan tiga langkah…", "Padankan setiap … dengan …") | Template wording was written once, so a single mistake can repeat; read a sample from each island. |
| Players | "Pemain", "Sandaran" (backup), "Cipta pemain" | Natural for families? Is "sandaran" understood? |
| Hats | "Topi kelasi", "Topi ahli sihir", "Fon kepala", "Gogal", "Bandana" | Natural names for each accessory? |

| Music / skills | "Muzik", "Kelantangan muzik", "Kemahiran yang telah dipelajari", ranks "Belum lagi / Bermula / Mahir / Pakar" | Natural wording for children? |
| New islands | "Gunung Berapi Ember", "Teluk Lanun", "Kanopi Hutan Belantara", "Kerajaan Gula-gula", "Lembah Dinosaur", "Kilang Robot", "Arena Sukan", "Kubu Istana", "Jambatan Pelangi", "Malam Karnival" | Island names and blurbs read well? |

Mathematical consistency between English and Malay is partly machine-checked (`tests/run-tests.js` compares every number
in each pair), but meaning and naturalness are not.

## Added in v0.5.0 (please review in Bahasa Melayu)
* Levels 213 to 312 (islands 24 to 33, `tools/mk/p21.py` to `p30.py`): template-generated like levels 25 to 212; names, stories and critter blurbs need a teacher's check.
* New screens and messages: the daily gift (`streak.*`), "found" items (`find.*`), and the version / what's-new card (`ver.*` and `js/changelog.js`, which holds its own English and Malay text).

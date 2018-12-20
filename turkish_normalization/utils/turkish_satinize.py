from unidecode import unidecode

turkish_lcase = "abcçdefgğhıijklmnoöprsştuüvyz"
turkish_ucase = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
subs_table = [
    ("$", "ş"),
    ("q", "g"),
    ("0", "o"),
    ("€", "e"),
    ("ß", "b"),
    ("@", "a"),
    ("w", "v"),
    ("μ", "u"),
    ("ø", "o"),
    ("æ", "a"),
    ("ı", "i"),
    ("μ", "u"),

]

low_translate_table = {ord(f_c): t_c for f_c, t_c in zip(turkish_ucase, turkish_lcase)}
subs_translate_table = {ord(f_c): t_c for f_c, t_c in subs_table}


def turkish_lower(src_str):
    # first translate turkish characters
    src_str = src_str.translate(low_translate_table)
    # then translate rest of it
    return src_str.casefold()


def turkish_substitute(src_str):
    return src_str.translate(subs_translate_table)


def shave_accents(src_str):
    # Taken from 'Fluent Python' page 126
    norm_txt = ud.normalize("NFD", src_str)
    shaved = "".join(c for c in norm_txt if not ud.combining(c))
    return ud.normalize("NFC", shaved)


def turkish_sanitize(src_str):
    # first replace german character, because it's lowercase different
    src_str = src_str.replace("ß", "b")
    src_str = turkish_lower(src_str)  # make it lower case
    # substitute commonly wrong written chars
    src_str = turkish_substitute(src_str)
    return unidecode(src_str)  # shave accents


def turkish_compare(str1, str2):
    return turkish_sanitize(str1) == turkish_sanitize(str2)

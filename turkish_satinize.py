import unicodedata as ud

lcase_table = "abcçdefgğhıijklmnoöprsştuüvyz\u00E2\u00EE\u00FB\u00F4"
ucase_table = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ\u00C2\u00CE\u00DB\u00D4"
subs_table = [("$", "ş"), ("q", "g"), ("0", "o"), ("€", "e"), ("ß", "b"), ("@", "a")]

low_translate_table = {ord(f_c): t_c for f_c, t_c in zip(ucase_table, lcase_table)}
subs_translate_table = {ord(f_c): t_c for f_c, t_c in subs_table}


def turkishLower(src_str):
    src_str = src_str.translate(low_translate_table)
    return src_str.casefold()


def turkishSubstitute(src_str):
    return src_str.translate(subs_translate_table)


def shave_accents(src_str):
    # Taken from 'Fluent Python' page 126
    norm_txt = ud.normalize("NFD", src_str)
    shaved = "".join(c for c in norm_txt if not ud.combining(c))
    return ud.normalize("NFC", shaved)


# TODO: if we are gonna shave accents than we dont need turkish_lower
# TODO: however we need to shave accents of öçğşü (or é) but not i


def turkishSanitize(src_str):
    src_str = turkishSubstitute(
        src_str
    )  # first substitute commonly wrong written chars
    src_str = turkishLower(src_str)  # make it lower case
    return shave_accents(src_str)  # shave accents


def turkishCompare(str1, str2):
    return turkishSanitize(str1) == turkishSanitize(str2)

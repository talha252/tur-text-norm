import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):
        return codecs.charmap_encode(input,errors,encoding_table)

    def decode(self,input,errors='strict'):
        return codecs.charmap_decode(input,errors,decoding_table)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input,self.errors,decoding_table)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API
def getregentry(name):
    if name != "lev-turkish":
        return None
    else:
        return codecs.CodecInfo(
            name='lev-turkish',
            encode=Codec().encode,
            decode=Codec().decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=StreamReader,
            streamwriter=StreamWriter,
        )

### Decoding Table

decoding_table = (
    'a'    #  0x00 -> LATIN SMALL LETTER A
    'i'    #  0x01 -> LATIN SMALL LETTER I
    'e'    #  0x02 -> LATIN SMALL LETTER E
    'n'    #  0x03 -> LATIN SMALL LETTER N
    'l'    #  0x04 -> LATIN SMALL LETTER L
    'r'    #  0x05 -> LATIN SMALL LETTER R
    'm'    #  0x06 -> LATIN SMALL LETTER M
    'd'    #  0x07 -> LATIN SMALL LETTER D
    'ı'    #  0x08 -> LATIN SMALL LETTER DOTLESS I
    's'    #  0x09 -> LATIN SMALL LETTER S
    'k'    #  0x0a -> LATIN SMALL LETTER K
    't'    #  0x0b -> LATIN SMALL LETTER T
    'y'    #  0x0c -> LATIN SMALL LETTER Y
    'u'    #  0x0d -> LATIN SMALL LETTER U
    'o'    #  0x0e -> LATIN SMALL LETTER O
    'z'    #  0x0f -> LATIN SMALL LETTER Z
    'b'    #  0x10 -> LATIN SMALL LETTER B
    'c'    #  0x11 -> LATIN SMALL LETTER C
    'h'    #  0x12 -> LATIN SMALL LETTER H
    'g'    #  0x13 -> LATIN SMALL LETTER G
    'ş'    #  0x14 -> LATIN SMALL LETTER S WITH CEDILLA
    "'"    #  0x15 -> APOSTROPHE
    'ü'    #  0x16 -> LATIN SMALL LETTER U WITH DIAERESIS
    'p'    #  0x17 -> LATIN SMALL LETTER P
    'j'    #  0x18 -> LATIN SMALL LETTER J
    'f'    #  0x19 -> LATIN SMALL LETTER F
    'ğ'    #  0x1a -> LATIN SMALL LETTER G WITH BREVE
    'v'    #  0x1b -> LATIN SMALL LETTER V
    'ç'    #  0x1c -> LATIN SMALL LETTER C WITH CEDILLA
    'ö'    #  0x1d -> LATIN SMALL LETTER O WITH DIAERESIS
    'w'    #  0x1e -> LATIN SMALL LETTER W
    'x'    #  0x1f -> LATIN SMALL LETTER X
    '0'    #  0x20 -> DIGIT ZERO
    'q'    #  0x21 -> LATIN SMALL LETTER Q
    '1'    #  0x22 -> DIGIT ONE
    '2'    #  0x23 -> DIGIT TWO
    '3'    #  0x24 -> DIGIT THREE
    '5'    #  0x25 -> DIGIT FIVE
    '4'    #  0x26 -> DIGIT FOUR
    '8'    #  0x27 -> DIGIT EIGHT
    '9'    #  0x28 -> DIGIT NINE
    '7'    #  0x29 -> DIGIT SEVEN
    'ə'    #  0x2a -> LATIN SMALL LETTER SCHWA
    '6'    #  0x2b -> DIGIT SIX
    'â'    #  0x2c -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    'î'    #  0x2d -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    '_'    #  0x2e -> LOW LINE
    'ê'    #  0x2f -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    'ï'    #  0x30 -> LATIN SMALL LETTER I WITH DIAERESIS
    'é'    #  0x31 -> LATIN SMALL LETTER E WITH ACUTE
    'û'    #  0x32 -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    'ý'    #  0x33 -> LATIN SMALL LETTER Y WITH ACUTE
    'а'    #  0x34 -> CYRILLIC SMALL LETTER A
    'ä'    #  0x35 -> LATIN SMALL LETTER A WITH DIAERESIS
    'º'    #  0x36 -> MASCULINE ORDINAL INDICATOR
    'ș'    #  0x37 -> LATIN SMALL LETTER S WITH COMMA BELOW
    'í'    #  0x38 -> LATIN SMALL LETTER I WITH ACUTE
    'ι'    #  0x39 -> GREEK SMALL LETTER IOTA
    'е'    #  0x3a -> CYRILLIC SMALL LETTER IE
    'ã'    #  0x3b -> LATIN SMALL LETTER A WITH TILDE
    'ó'    #  0x3c -> LATIN SMALL LETTER O WITH ACUTE
    'á'    #  0x3d -> LATIN SMALL LETTER A WITH ACUTE
    'α'    #  0x3e -> GREEK SMALL LETTER ALPHA
    'ɑ'    #  0x3f -> LATIN SMALL LETTER ALPHA
    'ì'    #  0x40 -> LATIN SMALL LETTER I WITH GRAVE
    'о'    #  0x41 -> CYRILLIC SMALL LETTER O
    'ñ'    #  0x42 -> LATIN SMALL LETTER N WITH TILDE
    'ә'    #  0x43 -> CYRILLIC SMALL LETTER SCHWA
    'ū'    #  0x44 -> LATIN SMALL LETTER U WITH MACRON
    'т'    #  0x45 -> CYRILLIC SMALL LETTER TE
    'è'    #  0x46 -> LATIN SMALL LETTER E WITH GRAVE
    'ģ'    #  0x47 -> LATIN SMALL LETTER G WITH CEDILLA
    'ú'    #  0x48 -> LATIN SMALL LETTER U WITH ACUTE
    'н'    #  0x49 -> CYRILLIC SMALL LETTER EN
    'р'    #  0x4a -> CYRILLIC SMALL LETTER ER
    'с'    #  0x4b -> CYRILLIC SMALL LETTER ES
    'å'    #  0x4c -> LATIN SMALL LETTER A WITH RING ABOVE
    'ű'    #  0x4d -> LATIN SMALL LETTER U WITH DOUBLE ACUTE
    'õ'    #  0x4e -> LATIN SMALL LETTER O WITH TILDE
    'ô'    #  0x4f -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    'ò'    #  0x50 -> LATIN SMALL LETTER O WITH GRAVE
    'м'    #  0x51 -> CYRILLIC SMALL LETTER EM
    'к'    #  0x52 -> CYRILLIC SMALL LETTER KA
    'ο'    #  0x53 -> GREEK SMALL LETTER OMICRON
    'у'    #  0x54 -> CYRILLIC SMALL LETTER U
    'ķ'    #  0x55 -> LATIN SMALL LETTER K WITH CEDILLA
    'š'    #  0x56 -> LATIN SMALL LETTER S WITH CARON
    'ć'    #  0x57 -> LATIN SMALL LETTER C WITH ACUTE
    'ù'    #  0x58 -> LATIN SMALL LETTER U WITH GRAVE
    'à'    #  0x59 -> LATIN SMALL LETTER A WITH GRAVE
    'ø'    #  0x5a -> LATIN SMALL LETTER O WITH STROKE
    'п'    #  0x5b -> CYRILLIC SMALL LETTER PE
    'г'    #  0x5c -> CYRILLIC SMALL LETTER GHE
    'ÿ'    #  0x5d -> LATIN SMALL LETTER Y WITH DIAERESIS
    'і'    #  0x5e -> CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
    'ő'    #  0x5f -> LATIN SMALL LETTER O WITH DOUBLE ACUTE
    'ɾ'    #  0x60 -> LATIN SMALL LETTER R WITH FISHHOOK
    'ĺ'    #  0x61 -> LATIN SMALL LETTER L WITH ACUTE
    'ë'    #  0x62 -> LATIN SMALL LETTER E WITH DIAERESIS
    'ŕ'    #  0x63 -> LATIN SMALL LETTER R WITH ACUTE
    'ź'    #  0x64 -> LATIN SMALL LETTER Z WITH ACUTE
    'б'    #  0x65 -> CYRILLIC SMALL LETTER BE
    'ī'    #  0x66 -> LATIN SMALL LETTER I WITH MACRON
    'ε'    #  0x67 -> GREEK SMALL LETTER EPSILON
    'ś'    #  0x68 -> LATIN SMALL LETTER S WITH ACUTE
    'ů'    #  0x69 -> LATIN SMALL LETTER U WITH RING ABOVE
    'ţ'    #  0x6a -> LATIN SMALL LETTER T WITH CEDILLA
    'đ'    #  0x6b -> LATIN SMALL LETTER D WITH STROKE
    'ā'    #  0x6c -> LATIN SMALL LETTER A WITH MACRON
    'ĝ'    #  0x6d -> LATIN SMALL LETTER G WITH CIRCUMFLEX
    'ν'    #  0x6e -> GREEK SMALL LETTER NU
    'ň'    #  0x6f -> LATIN SMALL LETTER N WITH CARON
    'č'    #  0x70 -> LATIN SMALL LETTER C WITH CARON
    'ł'    #  0x71 -> LATIN SMALL LETTER L WITH STROKE
    'τ'    #  0x72 -> GREEK SMALL LETTER TAU
    'η'    #  0x73 -> GREEK SMALL LETTER ETA
    'ǝ'    #  0x74 -> LATIN SMALL LETTER TURNED E
    'κ'    #  0x75 -> GREEK SMALL LETTER KAPPA
    'į'    #  0x76 -> LATIN SMALL LETTER I WITH OGONEK
    'ρ'    #  0x77 -> GREEK SMALL LETTER RHO
    'υ'    #  0x78 -> GREEK SMALL LETTER UPSILON
    'ž'    #  0x79 -> LATIN SMALL LETTER Z WITH CARON
    'ō'    #  0x7a -> LATIN SMALL LETTER O WITH MACRON
    'ａ'    #  0x7b -> FULLWIDTH LATIN SMALL LETTER A
    'æ'    #  0x7c -> LATIN SMALL LETTER AE
    '𝐞'    #  0x7d -> MATHEMATICAL BOLD SMALL E
    'ď'    #  0x7e -> LATIN SMALL LETTER D WITH CARON
    'ɐ'    #  0x7f -> LATIN SMALL LETTER TURNED A
    'х'    #  0x80 -> CYRILLIC SMALL LETTER HA
    'ｅ'    #  0x81 -> FULLWIDTH LATIN SMALL LETTER E
    'ѕ'    #  0x82 -> CYRILLIC SMALL LETTER DZE
    'μ'    #  0x83 -> GREEK SMALL LETTER MU
    'λ'    #  0x84 -> GREEK SMALL LETTER LAMDA
    'ą'    #  0x85 -> LATIN SMALL LETTER A WITH OGONEK
    '𝐚'    #  0x86 -> MATHEMATICAL BOLD SMALL A
    'ｎ'    #  0x87 -> FULLWIDTH LATIN SMALL LETTER N
    '²'    #  0x88 -> SUPERSCRIPT TWO
    'ｉ'    #  0x89 -> FULLWIDTH LATIN SMALL LETTER I
    'π'    #  0x8a -> GREEK SMALL LETTER PI
    'ᵃ'    #  0x8b -> MODIFIER LETTER SMALL A
    'ᵉ'    #  0x8c -> MODIFIER LETTER SMALL E
    'ｒ'    #  0x8d -> FULLWIDTH LATIN SMALL LETTER R
    'β'    #  0x8e -> GREEK SMALL LETTER BETA
    '𝒆'    #  0x8f -> MATHEMATICAL BOLD ITALIC SMALL E
    '𝐢'    #  0x90 -> MATHEMATICAL BOLD SMALL I
    'є'    #  0x91 -> CYRILLIC SMALL LETTER UKRAINIAN IE
    'ę'    #  0x92 -> LATIN SMALL LETTER E WITH OGONEK
    'ʼ'    #  0x93 -> MODIFIER LETTER APOSTROPHE
    '𝑒'    #  0x94 -> MATHEMATICAL ITALIC SMALL E
    '𝐧'    #  0x95 -> MATHEMATICAL BOLD SMALL N
    'ⁿ'    #  0x96 -> SUPERSCRIPT LATIN SMALL LETTER N
    'ʻ'    #  0x97 -> MODIFIER LETTER TURNED COMMA
    'ʇ'    #  0x98 -> LATIN SMALL LETTER TURNED T
    'ă'    #  0x99 -> LATIN SMALL LETTER A WITH BREVE
    'ɹ'    #  0x9a -> LATIN SMALL LETTER TURNED R
    'ｌ'    #  0x9b -> FULLWIDTH LATIN SMALL LETTER L
    '𝐫'    #  0x9c -> MATHEMATICAL BOLD SMALL R
    'ᵒ'    #  0x9d -> MODIFIER LETTER SMALL O
    '𝐥'    #  0x9e -> MATHEMATICAL BOLD SMALL L
    'ῐ'    #  0x9f -> GREEK SMALL LETTER IOTA WITH VRACHY
    'ɴ'    #  0xa0 -> LATIN LETTER SMALL CAPITAL N
    '𝒂'    #  0xa1 -> MATHEMATICAL BOLD ITALIC SMALL A
    'ǧ'    #  0xa2 -> LATIN SMALL LETTER G WITH CARON
    '𝐭'    #  0xa3 -> MATHEMATICAL BOLD SMALL T
    'ά'    #  0xa4 -> GREEK SMALL LETTER ALPHA WITH TONOS
    'ʹ'    #  0xa5 -> MODIFIER LETTER PRIME
    'œ'    #  0xa6 -> LATIN SMALL LIGATURE OE
    '𝒊'    #  0xa7 -> MATHEMATICAL BOLD ITALIC SMALL I
    'ί'    #  0xa8 -> GREEK SMALL LETTER IOTA WITH TONOS
    'ｓ'    #  0xa9 -> FULLWIDTH LATIN SMALL LETTER S
    'ℓ'    #  0xaa -> SCRIPT SMALL L
    'ż'    #  0xab -> LATIN SMALL LETTER Z WITH DOT ABOVE
    'э'    #  0xac -> CYRILLIC SMALL LETTER E
    '𝐨'    #  0xad -> MATHEMATICAL BOLD SMALL O
    'ｍ'    #  0xae -> FULLWIDTH LATIN SMALL LETTER M
    'ｔ'    #  0xaf -> FULLWIDTH LATIN SMALL LETTER T
    '𝒕'    #  0xb0 -> MATHEMATICAL BOLD ITALIC SMALL T
    '𝒐'    #  0xb1 -> MATHEMATICAL BOLD ITALIC SMALL O
    'ｄ'    #  0xb2 -> FULLWIDTH LATIN SMALL LETTER D
    'ｋ'    #  0xb3 -> FULLWIDTH LATIN SMALL LETTER K
    'ｏ'    #  0xb4 -> FULLWIDTH LATIN SMALL LETTER O
    'δ'    #  0xb5 -> GREEK SMALL LETTER DELTA
    'น'    #  0xb6 -> THAI CHARACTER NO NU
    '𝑎'    #  0xb7 -> MATHEMATICAL ITALIC SMALL A
    '𝐝'    #  0xb8 -> MATHEMATICAL BOLD SMALL D
    'ω'    #  0xb9 -> GREEK SMALL LETTER OMEGA
    '𝒏'    #  0xba -> MATHEMATICAL BOLD ITALIC SMALL N
    'έ'    #  0xbb -> GREEK SMALL LETTER EPSILON WITH TONOS
    '𝐬'    #  0xbc -> MATHEMATICAL BOLD SMALL S
    '𝑖'    #  0xbd -> MATHEMATICAL ITALIC SMALL I
    'ě'    #  0xbe -> LATIN SMALL LETTER E WITH CARON
    '𝙖'    #  0xbf -> MATHEMATICAL SANS-SERIF BOLD ITALIC SMALL A
    '𝒔'    #  0xc0 -> MATHEMATICAL BOLD ITALIC SMALL S
    'ก'    #  0xc1 -> THAI CHARACTER KO KAI
    'ᴀ'    #  0xc2 -> LATIN LETTER SMALL CAPITAL A
    'ό'    #  0xc3 -> GREEK SMALL LETTER OMICRON WITH TONOS
    '𝒶'    #  0xc4 -> MATHEMATICAL SCRIPT SMALL A
    'ｕ'    #  0xc5 -> FULLWIDTH LATIN SMALL LETTER U
    '𝒓'    #  0xc6 -> MATHEMATICAL BOLD ITALIC SMALL R
    'ｙ'    #  0xc7 -> FULLWIDTH LATIN SMALL LETTER Y
    '𝑡'    #  0xc8 -> MATHEMATICAL ITALIC SMALL T
    '𝑜'    #  0xc9 -> MATHEMATICAL ITALIC SMALL O
    'ᴇ'    #  0xca -> LATIN LETTER SMALL CAPITAL E
    'ɯ'    #  0xcb -> LATIN SMALL LETTER TURNED M
    '𝙚'    #  0xcc -> MATHEMATICAL SANS-SERIF BOLD ITALIC SMALL E
    'ʸ'    #  0xcd -> MODIFIER LETTER SMALL Y
    'ᵗ'    #  0xce -> MODIFIER LETTER SMALL T
    '𝒍'    #  0xcf -> MATHEMATICAL BOLD ITALIC SMALL L
    '𝑠'    #  0xd0 -> MATHEMATICAL ITALIC SMALL S
    'ʰ'    #  0xd1 -> MODIFIER LETTER SMALL H
    'ʀ'    #  0xd2 -> LATIN LETTER SMALL CAPITAL R
    'ʞ'    #  0xd3 -> LATIN SMALL LETTER TURNED K
    '𝐲'    #  0xd4 -> MATHEMATICAL BOLD SMALL Y
    '𝑛'    #  0xd5 -> MATHEMATICAL ITALIC SMALL N
    'ї'    #  0xd6 -> CYRILLIC SMALL LETTER YI
    '𝐮'    #  0xd7 -> MATHEMATICAL BOLD SMALL U
    'ม'    #  0xd8 -> THAI CHARACTER MO MA
    'ʳ'    #  0xd9 -> MODIFIER LETTER SMALL R
    'ɢ'    #  0xda -> LATIN LETTER SMALL CAPITAL G
    '𝐦'    #  0xdb -> MATHEMATICAL BOLD SMALL M
    '³'    #  0xdc -> SUPERSCRIPT THREE
    'ᵘ'    #  0xdd -> MODIFIER LETTER SMALL U
    '𝚎'    #  0xde -> MATHEMATICAL MONOSPACE SMALL E
    '𝗮'    #  0xdf -> MATHEMATICAL SANS-SERIF BOLD SMALL A
    '𝕖'    #  0xe0 -> MATHEMATICAL DOUBLE-STRUCK SMALL E
    '𝙩'    #  0xe1 -> MATHEMATICAL SANS-SERIF BOLD ITALIC SMALL T
    '𝒉'    #  0xe2 -> MATHEMATICAL BOLD ITALIC SMALL H
    'ᵍ'    #  0xe3 -> MODIFIER LETTER SMALL G
    '𝙞'    #  0xe4 -> MATHEMATICAL SANS-SERIF BOLD ITALIC SMALL I
    '𝓮'    #  0xe5 -> MATHEMATICAL BOLD SCRIPT SMALL E
    'ɪ'    #  0xe6 -> LATIN LETTER SMALL CAPITAL I
    'ʎ'    #  0xe7 -> LATIN SMALL LETTER TURNED Y
    '𝗲'    #  0xe8 -> MATHEMATICAL SANS-SERIF BOLD SMALL E
    'ｇ'    #  0xe9 -> FULLWIDTH LATIN SMALL LETTER G
    'ᵈ'    #  0xea -> MODIFIER LETTER SMALL D
    '𝓪'    #  0xeb -> MATHEMATICAL BOLD SCRIPT SMALL A
    '𝒅'    #  0xec -> MATHEMATICAL BOLD ITALIC SMALL D
    '𝑟'    #  0xed -> MATHEMATICAL ITALIC SMALL R
    'ř'    #  0xee -> LATIN SMALL LETTER R WITH CARON
    'ɔ'    #  0xef -> LATIN SMALL LETTER OPEN O
    '𝘢'    #  0xf0 -> MATHEMATICAL SANS-SERIF ITALIC SMALL A
    'ᴏ'    #  0xf1 -> LATIN LETTER SMALL CAPITAL O
    'ƃ'    #  0xf2 -> LATIN SMALL LETTER B WITH TOPBAR
    '𝔢'    #  0xf3 -> MATHEMATICAL FRAKTUR SMALL E
    'บ'    #  0xf4 -> THAI CHARACTER BO BAIMAI
    '𝗶'    #  0xf5 -> MATHEMATICAL SANS-SERIF BOLD SMALL I
    'ɥ'    #  0xf6 -> LATIN SMALL LETTER TURNED H
    'ｚ'    #  0xf7 -> FULLWIDTH LATIN SMALL LETTER Z
    'ń'    #  0xf8 -> LATIN SMALL LETTER N WITH ACUTE
    'ˡ'    #  0xf9 -> MODIFIER LETTER SMALL L
    'ᵐ'    #  0xfa -> MODIFIER LETTER SMALL M
    '𝚊'    #  0xfb -> MATHEMATICAL MONOSPACE SMALL A
    'ｈ'    #  0xfc -> FULLWIDTH LATIN SMALL LETTER H
    'ť'    #  0xfd -> LATIN SMALL LETTER T WITH CARON
    '𝐛'    #  0xfe -> MATHEMATICAL BOLD SMALL B
    '𝒊'    #  0xff -> MATHEMATICAL BOLD ITALIC SMALL I
)
### Encoding table
encoding_table=codecs.charmap_build(decoding_table)
codecs.register(getregentry)

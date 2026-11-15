
import html, re, unicodedata

EMOJI_DICT = {
    '🤮': 'icon_nôn_mửa', '🤢': 'icon_buồn_nôn', '💩': 'icon_phân', '🤬': 'icon_chửi_bới',
    '😡': 'icon_tức_giận', '😠': 'icon_giận_dữ', '👿': 'icon_ác_quỷ', '🖕': 'icon_ngón_tay_thối',
    '👎': 'icon_chê_bai', '🤡': 'icon_hề_hước', '🐶': 'icon_chó', '🐕': 'icon_chó',
    '🐷': 'icon_lợn', '🐖': 'icon_lợn', '🐂': 'icon_bò', '🐃': 'icon_trâu_bò',
    '🙂': 'icon_mỉa_mai', '🙃': 'icon_châm_chọc', '😏': 'icon_khinh_khỉnh', '😒': 'icon_khó_chịu',
    '🙄': 'icon_đảo_mắt', '🥱': 'icon_nhàm_chán', '😴': 'icon_buồn_ngủ', '🇻🇳': 'icon_cờ_việt_nam',
    '❤': 'icon_yêu_thích', '💖': 'icon_yêu_thích', '💐': 'icon_hoa_tri_ân', '🌸': 'icon_hoa_tri_ân',
    '🕯': 'icon_thắp_nến', '🪦': 'icon_bia_mộ', '🫡': 'icon_chào_kính_cẩn', '🙏': 'icon_cầu_nguyện',
    '😭': 'icon_khóc_xúc_động', '😢': 'icon_khóc_xúc_động', '🥺': 'icon_xúc_động', '🥹': 'icon_xúc_động',
    '🔥': 'icon_bùng_nổ', '👍': 'icon_thích', '😂': 'icon_cười_lớn', '🤣': 'icon_cười_lớn',
}

TEENCODE_DICT = {
    'vc': 'vãi cứt', 'vcl': 'vãi cả lồn', 'vl': 'vãi lồn', 'vcc': 'vãi cả cặc',
    'vlon': 'vãi lồn', 'vkl': 'vãi cả lồn', 'vleu': 'vãi lồn', 'vloz': 'vãi lồn',
    'cl': 'cái lồn', 'clgt': 'cái lồn gì thế', 'cmn': 'con mẹ nó', 'cmnr': 'con mẹ nó rồi',
    'cc': 'con cặc', 'cclgt': 'con cặc gì thế', 'cẹc': 'cặc', 'kẹc': 'cặc',
    'đm': 'địt mẹ', 'dm': 'địt mẹ', 'dcm': 'địt con mẹ', 'đcm': 'địt con mẹ',
    'dmm': 'địt mẹ mày', 'đmm': 'địt mẹ mày', 'đkm': 'địt con mẹ', 'dkm': 'địt con mẹ',
    'cml': 'con mặt lồn', 'sml': 'sấp mặt lồn', 'dell': 'đéo',
    'đếch': 'đéo', 'đíu': 'đéo', 'méo': 'đéo',
    'ngu lol': 'ngu lồn', 'ngu l': 'ngu lồn', 'ngu loz': 'ngu lồn', 'ngu cc': 'ngu con cặc',
    'xàm lol': 'xàm lồn', 'xàm l': 'xàm lồn', '3 que': 'ba que',
    'rác rưởi': 'rác rưởi', 'rác': 'rác rưởi',
    'dẩm dờ': 'dẩm dờ', 'dẩm': 'dẩm dờ', 'xàm xí': 'xàm xí', 'xàm': 'xàm xí',
    'hãm tài': 'hãm tài', 'hãm': 'hãm tài',
    'k': 'không', 'ko': 'không', 'kh': 'không', 'dc': 'được',
    'bt': 'biết', 'bít': 'biết', 'r': 'rồi', 'rùi': 'rồi', 'mn': 'mọi người', 'mng': 'mọi người',
    'z': 'vậy', 'zậy': 'vậy', 'mik': 'mình', 'mk': 'mình',
}

HTML_PATTERN = re.compile(r'<.*?>')
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
WHITESPACE_PATTERN = re.compile(r'\s+')
LAUGHTER_PATTERN = re.compile(r'(?i)\b(k{3,}|h{3,}|(ha){2,}|(hi){2,}|(he){2,}|(ho){2,}|a+h+a+|h+a+h+)\b')
SLEEP_PATTERN = re.compile(r'(?i)\b(z{3,})\b')

# Chuỗi viết tắt thô tục bị ngụy trang bằng dấu chấm/gạch (d.c.m, v.c.l, c.l.g.t ...).
# Dấu phân cách bắt buộc có ít nhất một ký tự . - _ / * (khoảng trắng chỉ được đi kèm).
_SEP = r'\s*[\.\-_/\*]+\s*'
def _obf(letters):
    return re.compile(r'(?i)\b' + _SEP.join(letters) + r'\b')

OBFUSCATION_RULES = [
    (_obf(['c', 'l', 'g', 't']), ' cái_lồn_gì_thế '),
    (_obf(['[đd]', 'c', 'm', 'm']), ' địt_con_mẹ_mày '),
    (_obf(['[đd]', 'c', 'm']), ' địt_con_mẹ '),
    (_obf(['v', 'c', 'l']), ' vãi_cả_lồn '),
    (_obf(['v', 'c', '[đd]']), ' vãi_cả_đái '),
    (_obf(['[đd]', 'm', 'm']), ' địt_mẹ_mày '),
    (_obf(['c', 'm', 'm']), ' con_mẹ_mày '),
    (_obf(['c', 'm', 'n']), ' con_mẹ_nó '),
    (_obf(['[đd]', 'm']), ' địt_mẹ '),
    (_obf(['c', 'l']), ' cái_lồn '),
]

MISC_RULES = [
    (re.compile(r'(?i)\bc(?:[\.\-_/\*]+ứ[\.\-_/\*]*|ứ[\.\-_/\*]+)t\b'), 'cứt'),
    (re.compile(r'(?i)\bđ\s+ịt\b'), 'địt'),
    (re.compile(r'(?i)\bl\s+ồn\b'), 'lồn'),
    (re.compile(r'(?i)\bc\s+ặc\b'), 'cặc'),
    (re.compile(r'(?i)\bm\s+ẹ\b'), 'mẹ'),
    (re.compile(r'(?i)\bl0n\b'), 'lồn'),
    (re.compile(r'(?i)\bđ!t\b'), 'địt'),
    (re.compile(r'(?i)\bb@\s*que\b'), 'ba que'),
]

TEENCODE_PATTERN = re.compile(
    r'(?u)\b(' + '|'.join(sorted(map(re.escape, TEENCODE_DICT.keys()), key=len, reverse=True)) + r')\b')


def reduce_elongation(text):
    # Chỉ rút gọn khi một ký tự lặp từ 3 lần trở lên: giữ nguyên 'good', 'book', 'xoong', 'boong'.
    text = re.sub(r'(?i)o{3,}', 'oo', text)
    text = re.sub(r'(?i)e{3,}', 'ee', text)
    text = re.sub(r'(?i)([a-zA-Zà-ỹÀ-Ỹ])\1{2,}', r'\1', text)
    return text


def minimal_clean(text):
    # Làm sạch tối thiểu: giải mã HTML, bỏ thẻ/URL, chuẩn hóa Unicode, chữ thường, gọn khoảng trắng.
    if not isinstance(text, str):
        return ''
    text = html.unescape(text)
    text = HTML_PATTERN.sub(' ', text)
    text = URL_PATTERN.sub(' ', text)
    text = unicodedata.normalize('NFC', text).lower()
    return WHITESPACE_PATTERN.sub(' ', text).strip()


def clean_text(text):
    # Tiền xử lý đầy đủ (không có trạng thái học từ dữ liệu nên không gây rò rỉ).
    if not isinstance(text, str):
        return ''
    text = html.unescape(text)
    text = HTML_PATTERN.sub(' ', text)
    text = URL_PATTERN.sub(' ', text)
    text = unicodedata.normalize('NFC', text).replace('\ufe0f', '')
    for k, v in EMOJI_DICT.items():
        text = text.replace(k, f' {v} ')
    text = text.lower()
    text = LAUGHTER_PATTERN.sub(' icon_cười_lớn ', text)
    text = SLEEP_PATTERN.sub(' icon_ngủ ', text)
    for pat, rep in OBFUSCATION_RULES:
        text = pat.sub(rep, text)
    for pat, rep in MISC_RULES:
        text = pat.sub(rep, text)
    text = reduce_elongation(text)
    text = TEENCODE_PATTERN.sub(lambda m: TEENCODE_DICT[m.group(0)], text)
    return WHITESPACE_PATTERN.sub(' ', text).strip()

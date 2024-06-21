def is_real_data(txt: str) -> bool:
    return txt[0] == '0' or txt[0] == '1'

def real_data_trid(txt: str) -> str:
    return txt.split('|')[1]
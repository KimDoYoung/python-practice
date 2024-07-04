from backend.app.domains.stock_api_base_model import StockApiBaseModel

class SearchStockInfoItem(StockApiBaseModel):
    pdno: str # 상품번호 
    prdt_type_cd: str # 상품유형코드 
    mket_id_cd: str # 시장ID코드 AGR.농축산물파생 BON.채권파생 CMD.일반상품시장 CUR.통화파생 ENG.에너지파생 EQU.주식파생 ETF.ETF파생 IRT.금리파생 KNX.코넥스 KSQ.코스닥 MTL.금속파생 SPI.주가지수파생 STK.유가증권
    scty_grp_id_cd: str # 증권그룹ID코드 BC.수익증권 DR.주식예탁증서 EF.ETF EN.ETN EW.ELW FE.해외ETF FO.선물옵션 FS.외국주권 FU.선물 FX.플렉스 선물 GD.금현물 IC.투자계약증권 IF.사회간접자본투융자회사 KN.코넥스주권 MF.투자회사 OP.옵션 RT.부동산투자회사 SC.선박투자회사 SR.신주인수권증서 ST.주권 SW.신주인수권증권 TC.신탁수익증권
    excg_dvsn_cd: str # 거래소구분코드 01.한국증권 02.증권거래소 03.코스닥 04.K-OTC 05.선물거래소 06.CME 07.EUREX 21.금현물 50.미국주간 51.홍콩 52.상해B 53.심천 54.홍콩거래소 55.미국 56.일본 57.상해A 58.심천A 59.베트남 61.장전시간외시장 64.경쟁대량매매 65.경매매시장 81.시간외단일가시장
    setl_mmdd: str # 결산월일 
    lstg_stqt: str # 상장주수 
    lstg_cptl_amt: str # 상장자본금액 
    cpta: str # 자본금 
    papr: str # 액면가 
    issu_pric: str # 발행가격 
    kospi200_item_yn: str # 코스피200종목여부 
    scts_mket_lstg_dt: str # 유가증권시장상장일자 
    scts_mket_lstg_abol_dt: str # 유가증권시장상장폐지일자 
    kosdaq_mket_lstg_dt: str # 코스닥시장상장일자 
    kosdaq_mket_lstg_abol_dt: str # 코스닥시장상장폐지일자 
    frbd_mket_lstg_dt: str # 프리보드시장상장일자 
    frbd_mket_lstg_abol_dt: str # 프리보드시장상장폐지일자 
    reits_kind_cd: str # 리츠종류코드 
    etf_dvsn_cd: str # ETF구분코드 
    oilf_fund_yn: str # 유전펀드여부 
    idx_bztp_lcls_cd: str # 지수업종대분류코드 
    idx_bztp_mcls_cd: str # 지수업종중분류코드 
    idx_bztp_scls_cd: str # 지수업종소분류코드 
    stck_kind_cd: str # 주식종류코드 000.해당사항없음 101.보통주 201.우선주 202.2우선주 203.3우선주 204.4우선주 205.5우선주 206.6우선주 207.7우선주 208.8우선주 209.9우선주 210.10우선주 211.11우선주 212.12우선주 213.13우선주 214.14우선주 215.15우선주 216.16우선주 217.17우선주 218.18우선주 219.19우선주 220.20우선주 301.후배주 401.혼합주
    mfnd_opng_dt: str # 뮤추얼펀드개시일자 
    mfnd_end_dt: str # 뮤추얼펀드종료일자 
    dpsi_erlm_cncl_dt: str # 예탁등록취소일자 
    etf_cu_qty: str # ETFCU수량 
    prdt_name: str # 상품명 
    prdt_name120: str # 상품명120 
    prdt_abrv_name: str # 상품약어명 
    std_pdno: str # 표준상품번호 
    prdt_eng_name: str # 상품영문명 
    prdt_eng_name120: str # 상품영문명120 
    prdt_eng_abrv_name: str # 상품영문약어명 
    dpsi_aptm_erlm_yn: str # 예탁지정등록여부 
    etf_txtn_type_cd: str # ETF과세유형코드 
    etf_type_cd: str # ETF유형코드 
    lstg_abol_dt: str # 상장폐지일자 
    nwst_odst_dvsn_cd: str # 신주구주구분코드 
    sbst_pric: str # 대용가격 
    thco_sbst_pric: str # 당사대용가격 
    thco_sbst_pric_chng_dt: str # 당사대용가격변경일자 
    tr_stop_yn: str # 거래정지여부 
    admn_item_yn: str # 관리종목여부 
    thdt_clpr: str # 당일종가 
    bfdy_clpr: str # 전일종가 
    clpr_chng_dt: str # 종가변경일자 
    std_idst_clsf_cd: str # 표준산업분류코드 
    std_idst_clsf_cd_name: str # 표준산업분류코드명 
    idx_bztp_lcls_cd_name: str # 지수업종대분류코드명 
    idx_bztp_mcls_cd_name: str # 지수업종중분류코드명 
    idx_bztp_scls_cd_name: str # 지수업종소분류코드명 
    ocr_no: str # OCR번호 
    crfd_item_yn: str # 크라우드펀딩종목여부 
    elec_scty_yn: str # 전자증권여부 
    issu_istt_cd: str # 발행기관코드 
    etf_chas_erng_rt_dbnb: str # ETF추적수익율배수 
    etf_etn_ivst_heed_item_yn: str # ETFETN투자유의종목여부 
    stln_int_rt_dvsn_cd: str # 대주이자율구분코드 
    frnr_psnl_lmt_rt: str # 외국인개인한도비율 
    lstg_rqsr_issu_istt_cd: str # 상장신청인발행기관코드 
    lstg_rqsr_item_cd: str # 상장신청인종목코드 
    trst_istt_issu_istt_cd: str # 신탁기관발행기관코드 

class SearchStockInfoDto(StockApiBaseModel):
    rt_cd: str # 성공 실패 여부 
    msg_cd: str # 응답코드 
    msg1: str # 응답메세지 
    output: SearchStockInfoItem
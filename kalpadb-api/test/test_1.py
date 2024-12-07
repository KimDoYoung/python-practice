from korean_lunar_calendar import KoreanLunarCalendar

def solYmd2lunYmd(solYmd):
    calendar = KoreanLunarCalendar()
    y = int(solYmd[:4])
    M = int(solYmd[4:6])
    d = int(solYmd[6:])

    calendar.setSolarDate(y, M, d)

    # Lunar Date (ISO Format)

    return calendar.LunarIsoFormat().replace('-', '') # 20201208


solYmds = '20210101|20210102'
solYmdArray = solYmds.split('|')
lunYmdArray = []
for solYmd in solYmdArray:
    lunYmdArray.append(solYmd2lunYmd(solYmd))

print(lunYmdArray) # ['20201219', '20201220']
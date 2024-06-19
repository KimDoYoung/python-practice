# lucy_calc.py
import sympy as sp 

def calc(template, variables):
    # 문자열 수식을 sympy의 기호로 변환
    expr = sp.sympify(template)
    # 변수값 대입을 위한 사전
    subs = {sp.symbols(key): value for key, value in variables.items()}
    
    try:
        # 수식을 평가하여 결과 반환
        result = expr.evalf(subs=subs)
    except Exception as e:
        # 평가 중 에러가 발생하면 에러 메시지 반환
        return f"Error: {e}"

    return result

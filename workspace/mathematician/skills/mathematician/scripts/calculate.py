#!/usr/bin/env python3
"""
数值计算工具
支持基本运算、矩阵运算、数值积分、微分方程求解等
"""

import sys
import argparse
import json
from pathlib import Path

try:
    import numpy as np
    import scipy as sp
    from scipy import integrate, optimize, linalg
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def basic_calc(a, b, operation):
    """基本算术运算"""
    ops = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
        "div": lambda a, b: a / b if b != 0 else float('inf'),
        "pow": lambda a, b: a ** b,
        "mod": lambda a, b: a % b,
    }
    if operation in ops:
        return ops[operation](a, b)
    return None


def matrix_ops(matrix_a, matrix_b, operation):
    """矩阵运算"""
    if not HAS_NUMPY:
        return {"error": "需要 numpy 和 scipy 库"}
    
    A = np.array(matrix_a)
    
    if operation == "transpose":
        result = np.transpose(A)
    elif operation == "inverse":
        try:
            result = np.linalg.inv(A)
        except np.linalg.LinAlgError:
            return {"error": "矩阵不可逆"}
    elif operation == "det" or operation == "determinant":
        result = np.linalg.det(A)
    elif operation == "eigen":
        eigenvalues, eigenvectors = np.linalg.eig(A)
        result = {"eigenvalues": eigenvalues.tolist(), "eigenvectors": eigenvectors.tolist()}
    elif matrix_b is not None:
        B = np.array(matrix_b)
        if operation == "multiply":
            result = np.dot(A, B)
        elif operation == "add":
            result = A + B
        elif operation == "subtract":
            result = A - B
    else:
        return {"error": f"未知运算: {operation}"}
    
    return {"result": result.tolist() if hasattr(result, 'tolist') else result}


def numerical_integration(func_str, a, b, method="quad"):
    """数值积分"""
    if not HAS_NUMPY:
        return {"error": "需要 numpy 和 scipy 库"}
    
    try:
        # 将字符串转换为函数
        def f(x):
            return eval(func_str, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt})
        
        if method == "quad":
            result, error = integrate.quad(f, a, b)
            return {"result": result, "error": error, "method": "quadrature"}
        elif method == "simpson":
            x = np.linspace(a, b, 1001)
            y = f(x)
            result = integrate.simpson(y, x)
            return {"result": result, "method": "simpson"}
        elif method == "trapezoid":
            x = np.linspace(a, b, 1001)
            y = f(x)
            result = integrate.trapezoid(y, x)
            return {"result": result, "method": "trapezoid"}
    except Exception as e:
        return {"error": str(e)}


def solve_ode(func_str, y0, t_span, method="RK45"):
    """求解常微分方程"""
    if not HAS_NUMPY:
        return {"error": "需要 numpy 和 scipy 库"}
    
    try:
        from scipy.integrate import solve_ivp
        
        def f(t, y):
            return eval(func_str, {"t": t, "y": y, "np": np})
        
        result = solve_ivp(f, t_span, y0, method=method, dense_output=True)
        
        return {
            "success": result.success,
            "t": result.t.tolist(),
            "y": result.y.tolist(),
            "method": method
        }
    except Exception as e:
        return {"error": str(e)}


def root_finding(func_str, x0, method="bisection"):
    """求根运算"""
    if not HAS_NUMPY:
        return {"error": "需要 numpy 和 scipy 库"}
    
    try:
        def f(x):
            if isinstance(x, (int, float)):
                return eval(func_str, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt})
            return np.array([eval(func_str, {"x": xi, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt}) for xi in x])
        
        if method == "bisection":
            result = optimize.bisect(f, x0[0], x0[1])
        elif method == "newton":
            result = optimize.newton(f, x0)
        elif method == "brentq":
            result = optimize.brentq(f, x0[0], x0[1])
        elif method == "fsolve":
            result = optimize.fsolve(f, x0)[0]
        else:
            return {"error": f"未知方法: {method}"}
        
        return {"root": result, "method": method}
    except Exception as e:
        return {"error": str(e)}


def interpolation(x_data, y_data, x_eval, method="cubic"):
    """插值运算"""
    if not HAS_NUMPY:
        return {"error": "需要 numpy 和 scipy 库"}
    
    try:
        from scipy.interpolate import interp1d
        
        f = interp1d(x_data, y_data, kind=method)
        y_eval = f(x_eval)
        
        return {"x": x_eval, "y": y_eval.tolist(), "method": method}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="数值计算工具")
    subparsers = parser.add_subparsers(dest="command", help="计算类型")
    
    # 基本运算
    basic_parser = subparsers.add_parser("basic", help="基本运算")
    basic_parser.add_argument("a", type=float)
    basic_parser.add_argument("b", type=float)
    basic_parser.add_argument("op", choices=["add", "sub", "mul", "div", "pow", "mod"])
    
    # 矩阵运算
    matrix_parser = subparsers.add_parser("matrix", help="矩阵运算")
    matrix_parser.add_argument("--A", required=True, help="矩阵A (JSON格式)")
    matrix_parser.add_argument("--B", help="矩阵B (JSON格式)")
    matrix_parser.add_argument("--op", required=True, choices=["transpose", "inverse", "det", "eigen", "multiply", "add", "subtract"])
    
    # 数值积分
    integral_parser = subparsers.add_parser("integrate", help="数值积分")
    integral_parser.add_argument("--func", required=True, help="函数表达式 (用x表示变量)")
    integral_parser.add_argument("--a", type=float, required=True, help="积分下限")
    integral_parser.add_argument("--b", type=float, required=True, help="积分上限")
    integral_parser.add_argument("--method", default="quad", choices=["quad", "simpson", "trapezoid"])
    
    # ODE求解
    ode_parser = subparsers.add_parser("ode", help="求解常微分方程")
    ode_parser.add_argument("--func", required=True, help="导数表达式 (用t,y表示)")
    ode_parser.add_argument("--y0", required=True, help="初始值 (逗号分隔)")
    ode_parser.add_argument("--t0", type=float, required=True)
    ode_parser.add_argument("--t1", type=float, required=True)
    
    # 求根
    root_parser = subparsers.add_parser("root", help="求根运算")
    root_parser.add_argument("--func", required=True, help="函数表达式")
    root_parser.add_argument("--x0", required=True, help="初始值或区间 (逗号分隔)")
    root_parser.add_argument("--method", default="bisection", choices=["bisection", "newton", "brentq", "fsolve"])
    
    # 插值
    interp_parser = subparsers.add_parser("interp", help="插值运算")
    interp_parser.add_argument("--x", required=True, help="x数据 (逗号分隔)")
    interp_parser.add_argument("--y", required=True, help="y数据 (逗号分隔)")
    interp_parser.add_argument("--xe", required=True, help="要插值的点 (逗号分隔)")
    interp_parser.add_argument("--method", default="cubic", choices=["linear", "cubic"])
    
    args = parser.parse_args()
    
    if not HAS_NUMPY:
        print(json.dumps({"error": "需要 numpy 和 scipy 库。请运行: pip install numpy scipy"}))
        sys.exit(1)
    
    if args.command == "basic":
        result = basic_calc(args.a, args.b, args.op)
        print(json.dumps({"result": result}))
    elif args.command == "matrix":
        A = json.loads(args.A)
        B = json.loads(args.B) if args.B else None
        result = matrix_ops(A, B, args.op)
        print(json.dumps(result, indent=2))
    elif args.command == "integrate":
        result = numerical_integration(args.func, args.a, args.b, args.method)
        print(json.dumps(result, indent=2))
    elif args.command == "ode":
        y0 = [float(x) for x in args.y0.split(",")]
        t_span = [args.t0, args.t1]
        result = solve_ode(args.func, y0, t_span)
        print(json.dumps(result, indent=2))
    elif args.command == "root":
        x0_str = args.x0.split(",")
        x0 = [float(x) for x in x0_str]
        result = root_finding(args.func, x0, args.method)
        print(json.dumps(result, indent=2))
    elif args.command == "interp":
        x_data = [float(x) for x in args.x.split(",")]
        y_data = [float(y) for y in args.y.split(",")]
        x_eval = [float(x) for x in args.xe.split(",")]
        result = interpolation(x_data, y_data, x_eval, args.method)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

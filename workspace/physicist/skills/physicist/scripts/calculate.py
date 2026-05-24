#!/usr/bin/env python3
"""
Physicist 数值计算工具
支持基本运算、矩阵运算、数值积分、常微分方程求解等
"""

import sys
import argparse
import numpy as np


def basic_calc(a, b, op):
    """基本数学运算"""
    ops = {
        'add': lambda: a + b,
        'sub': lambda: a - b,
        'mul': lambda: a * b,
        'div': lambda: a / b if b != 0 else float('inf'),
        'pow': lambda: a ** b,
    }
    if op not in ops:
        print(f"未知运算: {op}")
        return None
    return ops[op]()


def matrix_op(A, op):
    """矩阵运算"""
    A = np.array(A)
    if op == 'det':
        return np.linalg.det(A)
    elif op == 'inv':
        return np.linalg.inv(A)
    elif op == 'eig':
        eigenvalues, eigenvectors = np.linalg.eig(A)
        return eigenvalues, eigenvectors
    elif op == 'trace':
        return np.trace(A)
    elif op == 'norm':
        return np.linalg.norm(A)
    else:
        print(f"未知矩阵运算: {op}")
        return None


def integrate_func(func_str, a, b, method='quad'):
    """数值积分"""
    try:
        func = eval(f"lambda x: {func_str}")
    except Exception as e:
        print(f"函数解析错误: {e}")
        return None
    
    if method == 'quad':
        result, error = integrate.quad(func, a, b)
        return result, error
    elif method == 'trapz':
        x = np.linspace(a, b, 1000)
        y = func(x)
        return integrate.trapz(y, x)
    else:
        print(f"未知积分方法: {method}")
        return None


def solve_ode(func_str, y0, t_span, method='RK45'):
    """求解常微分方程"""
    from scipy.integrate import solve_ivp
    
    try:
        # 注意：这里需要将 func_str 转换为正确的函数格式
        exec(f"def odes(t, y): return {func_str}")
        odes = locals()['odes']
    except Exception as e:
        print(f"函数解析错误: {e}")
        return None
    
    sol = solve_ivp(odes, t_span, y0, method=method, dense_output=True)
    return sol


def main():
    parser = argparse.ArgumentParser(
        description="Physicist 数值计算工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本运算
  python3 calculate.py basic 10 5 add
  
  # 矩阵运算
  python3 calculate.py matrix --A "[[1,2],[3,4]]" --op det
  
  # 数值积分
  python3 calculate.py integrate --func "x**2" --a 0 --b 1
  
  # ODE求解
  python3 calculate.py ode --func "[y[1], -y[0]]" --y0 "[0, 1]" --t0 0 --t1 10
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 基本运算
    basic_parser = subparsers.add_parser('basic', help='基本运算')
    basic_parser.add_argument('a', type=float, help='第一个数')
    basic_parser.add_argument('b', type=float, help='第二个数')
    basic_parser.add_argument('op', choices=['add', 'sub', 'mul', 'div', 'pow'], help='运算')
    
    # 矩阵运算
    matrix_parser = subparsers.add_parser('matrix', help='矩阵运算')
    matrix_parser.add_argument('--A', required=True, help='矩阵 (JSON格式)')
    matrix_parser.add_argument('--op', required=True, choices=['det', 'inv', 'eig', 'trace', 'norm'], help='运算')
    
    # 数值积分
    integrate_parser = subparsers.add_parser('integrate', help='数值积分')
    integrate_parser.add_argument('--func', required=True, help='被积函数 (Python表达式, x为变量)')
    integrate_parser.add_argument('--a', type=float, required=True, help='积分下限')
    integrate_parser.add_argument('--b', type=float, required=True, help='积分上限')
    integrate_parser.add_argument('--method', default='quad', choices=['quad', 'trapz'], help='积分方法')
    
    # ODE求解
    ode_parser = subparsers.add_parser('ode', help='常微分方程求解')
    ode_parser.add_argument('--func', required=True, help='ODE函数 (return [dy1/dt, dy2/dt, ...])')
    ode_parser.add_argument('--y0', required=True, help='初始条件 (JSON格式列表)')
    ode_parser.add_argument('--t0', type=float, required=True, help='起始时间')
    ode_parser.add_argument('--t1', type=float, required=True, help='结束时间')
    ode_parser.add_argument('--method', default='RK45', help='求解方法')
    
    args = parser.parse_args()
    
    if args.command == 'basic':
        result = basic_calc(args.a, args.b, args.op)
        print(f"结果: {result}")
    
    elif args.command == 'matrix':
        A = json.loads(args.A)
        result = matrix_op(A, args.op)
        print(f"结果: {result}")
    
    elif args.command == 'integrate':
        result = integrate_func(args.func, args.a, args.b, args.method)
        if result:
            if isinstance(result, tuple):
                print(f"积分结果: {result[0]}, 误差估计: {result[1]}")
            else:
                print(f"积分结果: {result}")
    
    elif args.command == 'ode':
        y0 = json.loads(args.y0)
        result = solve_ode(args.func, y0, [args.t0, args.t1], args.method)
        if result:
            print(f"求解成功! 时间范围: {result.t[0]:.2f} 到 {result.t[-1]:.2f}")
            print(f"解的点数: {len(result.t)}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    raise SystemExit(main())

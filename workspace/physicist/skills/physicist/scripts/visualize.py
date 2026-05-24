#!/usr/bin/env python3
"""
Physicist 物理可视化工具
支持函数绘图、场分布图、相轨迹等
"""

import sys
import argparse
import numpy as np


def plot_function(func_str, x0, x1, title="Function Plot", xlabel="x", ylabel="y"):
    """绘制函数图像"""
    try:
        import matplotlib.pyplot as plt
        
        x = np.linspace(x0, x1, 1000)
        func = eval(f"lambda x: {func_str}")
        y = func(x)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y)
        plt.xlabel(f'${xlabel}$')
        plt.ylabel(f'${ylabel}$')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        
        if len(sys.argv) > 2 and sys.argv[2] == '--save':
            plt.savefig(sys.argv[3] if len(sys.argv) > 3 else 'plot.png')
            print(f"图像已保存")
        else:
            plt.show()
        
    except Exception as e:
        print(f"绘图错误: {e}")


def plot_phase_trajectory(funcs_str, y0_list, t_span, title="Phase Trajectory"):
    """绘制相轨迹"""
    try:
        import matplotlib.pyplot as plt
        from scipy.integrate import solve_ivp
        
        exec(f"def odes(t, y): return {funcs_str}")
        odes = locals()['odes']
        
        plt.figure(figsize=(8, 8))
        
        for y0 in y0_list:
            sol = solve_ivp(odes, t_span, y0, dense_output=True)
            plt.plot(sol.y[0], sol.y[1], label=f'y0={y0}')
        
        plt.xlabel('$q$')
        plt.ylabel('$p$')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(f"绘图错误: {e}")


def plot_field(potential_func, x_range, y_range, title="Field Plot"):
    """绘制场分布图"""
    try:
        import matplotlib.pyplot as plt
        
        x = np.linspace(x_range[0], x_range[1], 100)
        y = np.linspace(y_range[0], y_range[1], 100)
        X, Y = np.meshgrid(x, y)
        
        potential = eval(f"lambda x, y: {potential_func}")
        Z = potential(X, Y)
        
        plt.figure(figsize=(10, 8))
        plt.contourf(X, Y, Z, levels=20, cmap='viridis')
        plt.colorbar(label='Potential')
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.title(title)
        plt.show()
        
    except Exception as e:
        print(f"绘图错误: {e}")


def plot_3d_surface(func_str, x_range, y_range, title="3D Surface"):
    """绘制3D表面图"""
    try:
        import matplotlib.pyplot as plt
        
        x = np.linspace(x_range[0], x_range[1], 50)
        y = np.linspace(y_range[0], y_range[1], 50)
        X, Y = np.meshgrid(x, y)
        
        func = eval(f"lambda x, y: {func_str}")
        Z = func(X, Y)
        
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_zlabel('$z$')
        ax.set_title(title)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()
        
    except Exception as e:
        print(f"绘图错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Physicist 物理可视化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 函数图像
  python3 visualize.py function --func "np.sin(x)" --x0 0 --x1 "2*np.pi" --title "sin(x)"
  
  # 相轨迹
  python3 visualize.py phase --func "[y[1], -y[0]]" --y0 "[[0,1],[0,2]]" --t0 0 --t1 "20"
  
  # 场分布
  python3 visualize.py field --potential "1/np.sqrt(x**2+y**2)" --x-range "[-3,3]" --y-range "[-3,3]"
  
  # 3D表面
  python3 visualize.py surface --func "np.sin(np.sqrt(x**2+y**2))" --x-range "[-5,5]" --y-range "[-5,5]"
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 函数图像
    func_parser = subparsers.add_parser('function', help='绘制函数图像')
    func_parser.add_argument('--func', required=True, help='函数表达式 (numpy可用np.)')
    func_parser.add_argument('--x0', type=float, required=True, help='x起始值')
    func_parser.add_argument('--x1', required=True, help='x结束值 (可用np.pi等)')
    func_parser.add_argument('--title', default='Function Plot', help='图表标题')
    func_parser.add_argument('--xlabel', default='x', help='x轴标签')
    func_parser.add_argument('--ylabel', default='y', help='y轴标签')
    
    # 相轨迹
    phase_parser = subparsers.add_parser('phase', help='绘制相轨迹')
    phase_parser.add_argument('--func', required=True, help='ODE函数 (return [dy0/dt, dy1/dt, ...])')
    phase_parser.add_argument('--y0', required=True, help='初始条件列表 (JSON格式)')
    phase_parser.add_argument('--t0', type=float, required=True, help='起始时间')
    phase_parser.add_argument('--t1', required=True, help='结束时间')
    phase_parser.add_argument('--title', default='Phase Trajectory', help='图表标题')
    
    # 场分布
    field_parser = subparsers.add_parser('field', help='绘制场分布')
    field_parser.add_argument('--potential', required=True, help='势函数表达式')
    field_parser.add_argument('--x-range', required=True, help='x范围 [min,max] (JSON格式)')
    field_parser.add_argument('--y-range', required=True, help='y范围 [min,max] (JSON格式)')
    field_parser.add_argument('--title', default='Field Plot', help='图表标题')
    
    # 3D表面
    surf_parser = subparsers.add_parser('surface', help='绘制3D表面图')
    surf_parser.add_argument('--func', required=True, help='曲面函数表达式 f(x,y)')
    surf_parser.add_argument('--x-range', required=True, help='x范围 [min,max] (JSON格式)')
    surf_parser.add_argument('--y-range', required=True, help='y范围 [min,max] (JSON格式)')
    surf_parser.add_argument('--title', default='3D Surface', help='图表标题')
    
    args = parser.parse_args()
    
    if args.command == 'function':
        x1_val = eval(args.x1)
        plot_function(args.func, args.x0, x1_val, args.title, args.xlabel, args.ylabel)
    
    elif args.command == 'phase':
        import json
        y0_list = json.loads(args.y0)
        t1_val = float(args.t1) if isinstance(args.t1, (int, float)) else eval(args.t1)
        plot_phase_trajectory(args.func, y0_list, [args.t0, t1_val], args.title)
    
    elif args.command == 'field':
        import json
        x_range = json.loads(args.x_range)
        y_range = json.loads(args.y_range)
        plot_field(args.potential, x_range, y_range, args.title)
    
    elif args.command == 'surface':
        import json
        x_range = json.loads(args.x_range)
        y_range = json.loads(args.y_range)
        plot_3d_surface(args.func, x_range, y_range, args.title)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    raise SystemExit(main())

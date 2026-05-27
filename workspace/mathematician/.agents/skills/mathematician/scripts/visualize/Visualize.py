#!/usr/bin/env python3
"""
数据可视化工具
支持统计图表、数学函数绘图、数据分布图等
"""

import sys
import json
import argparse
from pathlib import Path

try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # 无头模式
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class Visualize:
    """数据可视化类"""

    @staticmethod
    def plot_function(func_str, x_range, output_path="plot.png", title="Function Plot"):
        """绘制数学函数图像"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库。请运行: pip install matplotlib"}

        try:
            x = np.linspace(x_range[0], x_range[1], 1000)

            # 安全地评估函数表达式
            safe_dict = {
                "x": x, "np": np, "sin": np.sin, "cos": np.cos,
                "tan": np.tan, "exp": np.exp, "log": np.log,
                "sqrt": np.sqrt, "abs": np.abs, "pi": np.pi, "e": np.e
            }
            y = eval(func_str, safe_dict)

            plt.figure(figsize=(10, 6))
            plt.plot(x, y, 'b-', linewidth=2)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title(title)
            plt.grid(True, alpha=0.3)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_data(x_data, y_data, output_path="plot.png", title="Data Plot", xlabel="x", ylabel="y"):
        """绘制数据图表"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            plt.plot(x_data, y_data, 'b-o', markersize=4)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.grid(True, alpha=0.3)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_histogram(data, output_path="histogram.png", bins=30, title="Distribution", xlabel="Value", ylabel="Frequency"):
        """绘制直方图"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.grid(True, alpha=0.3, axis='y')
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_scatter(x_data, y_data, output_path="scatter.png", title="Scatter Plot", xlabel="x", ylabel="y"):
        """绘制散点图"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            plt.scatter(x_data, y_data, alpha=0.6, s=50)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.grid(True, alpha=0.3)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_multi(x_data_list, y_data_list, labels, output_path="multi.png", title="Multiple Plots", xlabel="x", ylabel="y"):
        """绘制多条曲线"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            for x, y, label in zip(x_data_list, y_data_list, labels):
                plt.plot(x, y, '-', label=label, linewidth=2)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_bar(categories, values, output_path="bar.png", title="Bar Chart", xlabel="Category", ylabel="Value"):
        """绘制柱状图"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            plt.bar(categories, values, alpha=0.7, edgecolor='black')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.grid(True, alpha=0.3, axis='y')
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def plot_box(data_list, labels, output_path="box.png", title="Box Plot"):
        """绘制箱线图"""
        if not HAS_MATPLOTLIB:
            return {"error": "需要 matplotlib 库"}

        try:
            plt.figure(figsize=(10, 6))
            plt.boxplot(data_list, labels=labels)
            plt.title(title)
            plt.grid(True, alpha=0.3, axis='y')
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()

            return {"success": True, "output": output_path}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description="数据可视化工具")
        subparsers = parser.add_subparsers(dest="command", help="图表类型")

        # 函数图像
        func_parser = subparsers.add_parser("function", help="绘制函数图像")
        func_parser.add_argument("--func", required=True, help="函数表达式 (用x表示变量)")
        func_parser.add_argument("--x0", type=float, default=-10, help="x起始值")
        func_parser.add_argument("--x1", type=float, default=10, help="x结束值")
        func_parser.add_argument("--output", default="plot.png", help="输出文件")
        func_parser.add_argument("--title", default="Function Plot", help="图表标题")

        # 数据图表
        data_parser = subparsers.add_parser("data", help="绘制数据图表")
        data_parser.add_argument("--x", required=True, help="x数据 (逗号分隔)")
        data_parser.add_argument("--y", required=True, help="y数据 (逗号分隔)")
        data_parser.add_argument("--output", default="plot.png", help="输出文件")
        data_parser.add_argument("--title", default="Data Plot", help="图表标题")
        data_parser.add_argument("--xlabel", default="x", help="x轴标签")
        data_parser.add_argument("--ylabel", default="y", help="y轴标签")

        # 直方图
        hist_parser = subparsers.add_parser("histogram", help="绘制直方图")
        hist_parser.add_argument("--data", required=True, help="数据 (逗号分隔)")
        hist_parser.add_argument("--bins", type=int, default=30, help="箱数")
        hist_parser.add_argument("--output", default="histogram.png", help="输出文件")
        hist_parser.add_argument("--title", default="Distribution", help="图表标题")
        hist_parser.add_argument("--xlabel", default="Value", help="x轴标签")
        hist_parser.add_argument("--ylabel", default="Frequency", help="y轴标签")

        # 散点图
        scatter_parser = subparsers.add_parser("scatter", help="绘制散点图")
        scatter_parser.add_argument("--x", required=True, help="x数据 (逗号分隔)")
        scatter_parser.add_argument("--y", required=True, help="y数据 (逗号分隔)")
        scatter_parser.add_argument("--output", default="scatter.png", help="输出文件")
        scatter_parser.add_argument("--title", default="Scatter Plot", help="图表标题")
        scatter_parser.add_argument("--xlabel", default="x", help="x轴标签")
        scatter_parser.add_argument("--ylabel", default="y", help="y轴标签")

        # 柱状图
        bar_parser = subparsers.add_parser("bar", help="绘制柱状图")
        bar_parser.add_argument("--categories", required=True, help="类别 (逗号分隔)")
        bar_parser.add_argument("--values", required=True, help="值 (逗号分隔)")
        bar_parser.add_argument("--output", default="bar.png", help="输出文件")
        bar_parser.add_argument("--title", default="Bar Chart", help="图表标题")
        bar_parser.add_argument("--xlabel", default="Category", help="x轴标签")
        bar_parser.add_argument("--ylabel", default="Value", help="y轴标签")

        # 箱线图
        box_parser = subparsers.add_parser("box", help="绘制箱线图")
        box_parser.add_argument("--data", required=True, help="数据组 (用;分隔每组,组内用逗号)")
        box_parser.add_argument("--labels", required=True, help="标签 (逗号分隔)")
        box_parser.add_argument("--output", default="box.png", help="输出文件")
        box_parser.add_argument("--title", default="Box Plot", help="图表标题")

        args = parser.parse_args()

        if not HAS_MATPLOTLIB:
            print(json.dumps({"error": "需要 matplotlib 库。请运行: pip install matplotlib"}))
            sys.exit(1)

        if args.command == "function":
            result = cls.plot_function(args.func, [args.x0, args.x1], args.output, args.title)
            print(json.dumps(result, indent=2))
        elif args.command == "data":
            x_data = [float(x) for x in args.x.split(",")]
            y_data = [float(y) for y in args.y.split(",")]
            result = cls.plot_data(x_data, y_data, args.output, args.title, args.xlabel, args.ylabel)
            print(json.dumps(result, indent=2))
        elif args.command == "histogram":
            data = [float(d) for d in args.data.split(",")]
            result = cls.plot_histogram(data, args.output, args.bins, args.title, args.xlabel, args.ylabel)
            print(json.dumps(result, indent=2))
        elif args.command == "scatter":
            x_data = [float(x) for x in args.x.split(",")]
            y_data = [float(y) for y in args.y.split(",")]
            result = cls.plot_scatter(x_data, y_data, args.output, args.title, args.xlabel, args.ylabel)
            print(json.dumps(result, indent=2))
        elif args.command == "bar":
            categories = args.categories.split(",")
            values = [float(v) for v in args.values.split(",")]
            result = cls.plot_bar(categories, values, args.output, args.title, args.xlabel, args.ylabel)
            print(json.dumps(result, indent=2))
        elif args.command == "box":
            data_groups = [[float(d) for d in group.split(",")] for group in args.data.split(";")]
            labels = args.labels.split(",")
            result = cls.plot_box(data_groups, labels, args.output, args.title)
            print(json.dumps(result, indent=2))
        else:
            parser.print_help()


if __name__ == "__main__":
    raise SystemExit(Visualize.main())

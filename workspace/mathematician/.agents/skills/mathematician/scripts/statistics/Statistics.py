#!/usr/bin/env python3
"""
统计分析工具
支持描述统计、假设检验、回归分析、时间序列分析
"""

import sys
import json
import argparse
from pathlib import Path
from itertools import combinations

try:
    import numpy as np
    from scipy import stats, integrate
    from scipy.stats import t, norm, chi2, f as f_dist
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


class Statistics:
    """统计分析类"""

    @staticmethod
    def descriptive_stats(data):
        """描述性统计"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            data = np.array(data)
            return {
                "n": int(len(data)),
                "mean": float(np.mean(data)),
                "median": float(np.median(data)),
                "std": float(np.std(data, ddof=1)),
                "var": float(np.var(data, ddof=1)),
                "min": float(np.min(data)),
                "max": float(np.max(data)),
                "q1": float(np.percentile(data, 25)),
                "q3": float(np.percentile(data, 75)),
                "iqr": float(np.percentile(data, 75) - np.percentile(data, 25)),
                "skewness": float(stats.skew(data)),
                "kurtosis": float(stats.kurtosis(data))
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def t_test(sample1, sample2, alternative="two-sided", equal_var=True):
        """t检验"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            s1 = np.array(sample1)
            s2 = np.array(sample2)

            if equal_var:
                statistic, pvalue = stats.ttest_ind(s1, s2, alternative=alternative)
            else:
                statistic, pvalue = stats.ttest_ind(s1, s2, equal_var=False, alternative=alternative)

            return {
                "test": "t-test",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "alternative": alternative,
                "equal_variance": equal_var,
                "n1": len(s1),
                "n2": len(s2),
                "mean1": float(np.mean(s1)),
                "mean2": float(np.mean(s2))
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def paired_t_test(sample1, sample2):
        """配对t检验"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            s1 = np.array(sample1)
            s2 = np.array(sample2)

            statistic, pvalue = stats.ttest_rel(s1, s2)
            diff = s1 - s2

            return {
                "test": "paired-t-test",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "mean_diff": float(np.mean(diff)),
                "std_diff": float(np.std(diff, ddof=1)),
                "n": len(diff)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def chi_square_test(observed, expected=None):
        """卡方检验"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            obs = np.array(observed)

            if expected is None:
                # 拟合优度检验
                n_categories = len(obs)
                expected = np.array([np.sum(obs) / n_categories] * n_categories)
                statistic, pvalue = stats.chisquare(obs, expected)
            else:
                exp = np.array(expected)
                statistic, pvalue = stats.chisquare(obs, exp)

            return {
                "test": "chi-square",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "df": len(obs) - 1
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def correlation(x, y, method="pearson"):
        """相关性分析"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            x = np.array(x)
            y = np.array(y)

            if method == "pearson":
                r, pvalue = stats.pearsonr(x, y)
            elif method == "spearman":
                r, pvalue = stats.spearmanr(x, y)
            elif method == "kendall":
                r, pvalue = stats.kendalltau(x, y)
            else:
                return {"error": f"未知方法: {method}"}

            # 决定系数 R^2
            r2 = r ** 2

            return {
                "method": method,
                "correlation": float(r),
                "pvalue": float(pvalue),
                "r_squared": float(r2),
                "n": len(x)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def linear_regression(x, y):
        """线性回归"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            x = np.array(x)
            y = np.array(y)

            # 一元线性回归
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            # 计算预测值和残差
            y_pred = slope * x + intercept
            residuals = y - y_pred
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            return {
                "type": "linear",
                "slope": float(slope),
                "intercept": float(intercept),
                "r_value": float(r_value),
                "r_squared": float(r_squared),
                "p_value": float(p_value),
                "std_err": float(std_err),
                "equation": f"y = {slope:.4f}x + {intercept:.4f}",
                "n": len(x)
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def anova(*groups):
        """方差分析"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            groups = [np.array(g) for g in groups]
            statistic, pvalue = stats.f_oneway(*groups)

            # 计算各组均值
            means = [float(np.mean(g)) for g in groups]

            return {
                "test": "ANOVA",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "n_groups": len(groups),
                "group_means": means,
                "group_sizes": [len(g) for g in groups]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def normality_test(data, method="shapiro"):
        """正态性检验"""
        if not HAS_SCIPY:
            return {"error": "需要 scipy 库"}

        try:
            data = np.array(data)

            if method == "shapiro":
                statistic, pvalue = stats.shapiro(data)
            elif method == "kstest":
                statistic, pvalue = stats.kstest(data, 'norm')
            elif method == "normaltest":
                statistic, pvalue = stats.normaltest(data)
            else:
                return {"error": f"未知方法: {method}"}

            is_normal = pvalue > 0.05

            return {
                "test": f"normality-{method}",
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "is_normal": is_normal,
                "conclusion": "数据服从正态分布" if is_normal else "数据不服从正态分布"
            }
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description="统计分析工具")
        subparsers = parser.add_subparsers(dest="command", help="分析类型")

        # 描述性统计
        desc_parser = subparsers.add_parser("describe", help="描述性统计")
        desc_parser.add_argument("--data", required=True, help="数据 (逗号分隔)")

        # t检验
        t_parser = subparsers.add_parser("ttest", help="t检验")
        t_parser.add_argument("--s1", required=True, help="样本1 (逗号分隔)")
        t_parser.add_argument("--s2", required=True, help="样本2 (逗号分隔)")
        t_parser.add_argument("--alternative", default="two-sided", choices=["two-sided", "less", "greater"])
        t_parser.add_argument("--equal-var", action="store_true", default=True, help="假设方差相等")
        t_parser.add_argument("--paired", action="store_true", help="配对t检验")

        # 卡方检验
        chi_parser = subparsers.add_parser("chi2", help="卡方检验")
        chi_parser.add_argument("--observed", required=True, help="观测值 (逗号分隔)")
        chi_parser.add_argument("--expected", help="期望值 (逗号分隔,可选)")

        # 相关性
        corr_parser = subparsers.add_parser("corr", help="相关性分析")
        corr_parser.add_argument("--x", required=True, help="变量x (逗号分隔)")
        corr_parser.add_argument("--y", required=True, help="变量y (逗号分隔)")
        corr_parser.add_argument("--method", default="pearson", choices=["pearson", "spearman", "kendall"])

        # 线性回归
        reg_parser = subparsers.add_parser("regress", help="线性回归")
        reg_parser.add_argument("--x", required=True, help="自变量x (逗号分隔)")
        reg_parser.add_argument("--y", required=True, help="因变量y (逗号分隔)")

        # ANOVA
        anova_parser = subparsers.add_parser("anova", help="方差分析")
        anova_parser.add_argument("--groups", required=True, help="分组数据 (用;分隔每组,组内用逗号)")

        # 正态性检验
        norm_parser = subparsers.add_parser("normality", help="正态性检验")
        norm_parser.add_argument("--data", required=True, help="数据 (逗号分隔)")
        norm_parser.add_argument("--method", default="shapiro", choices=["shapiro", "kstest", "normaltest"])

        args = parser.parse_args()

        if not HAS_SCIPY:
            print(json.dumps({"error": "需要 scipy 库。请运行: pip install scipy"}))
            sys.exit(1)

        if args.command == "describe":
            data = [float(d) for d in args.data.split(",")]
            result = cls.descriptive_stats(data)
            print(json.dumps(result, indent=2))
        elif args.command == "ttest":
            s1 = [float(x) for x in args.s1.split(",")]
            s2 = [float(x) for x in args.s2.split(",")]
            if args.paired:
                result = cls.paired_t_test(s1, s2)
            else:
                result = cls.t_test(s1, s2, args.alternative, args.equal_var)
            print(json.dumps(result, indent=2))
        elif args.command == "chi2":
            obs = [float(x) for x in args.observed.split(",")]
            exp = [float(x) for x in args.expected.split(",")] if args.expected else None
            result = cls.chi_square_test(obs, exp)
            print(json.dumps(result, indent=2))
        elif args.command == "corr":
            x = [float(x) for x in args.x.split(",")]
            y = [float(y) for y in args.y.split(",")]
            result = cls.correlation(x, y, args.method)
            print(json.dumps(result, indent=2))
        elif args.command == "regress":
            x = [float(x) for x in args.x.split(",")]
            y = [float(y) for y in args.y.split(",")]
            result = cls.linear_regression(x, y)
            print(json.dumps(result, indent=2))
        elif args.command == "anova":
            groups = [[float(d) for d in g.split(",")] for g in args.groups.split(";")]
            result = cls.anova(*groups)
            print(json.dumps(result, indent=2))
        elif args.command == "normality":
            data = [float(d) for d in args.data.split(",")]
            result = cls.normality_test(data, args.method)
            print(json.dumps(result, indent=2))
        else:
            parser.print_help()


if __name__ == "__main__":
    raise SystemExit(Statistics.main())

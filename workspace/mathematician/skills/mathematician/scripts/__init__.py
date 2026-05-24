"""mathematician scripts 包的公共接口。"""

from scripts.calculate import main as calculate_main
from scripts.statistics import main as statistics_main
from scripts.visualize import main as visualize_main

__all__ = ['calculate_main', 'statistics_main', 'visualize_main']

"""fortunetelling scripts 包的公共接口。"""

from scripts.bazi  import main as bazi_main
from scripts.lunar import main as lunar_main
from scripts.fate  import main as fate_main

__all__ = ["bazi_main", "lunar_main", "fate_main"]

# File: utils/analysis/__init__.py
"""
Pakiet analizy ruchu sieciowego i wykrywania zagrożeń.

Zawiera moduły do analizy pakietów sieciowych i oceny ryzyka zagrożeń.
"""

# Import klasy BehavioralAnalyzer, aby była dostępna przy imporcie pakietu analysis
from .behavioral_analyzer import BehavioralAnalyzer

# Definiowanie, które elementy są eksportowane podczas `from analysis import *`
__all__ = ["BehavioralAnalyzer"]

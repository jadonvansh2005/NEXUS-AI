import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.fact_memory.fact_extractor import FactExtractor

extractor = FactExtractor()

test_cases = [
    "what i am learning ??",
    "what is my nickname ??",
    "this is vansh pratap singh call sign patty"
]

for tc in test_cases:
    result = extractor.extract(tc)
    print(f"INPUT: {tc} => EXTRACTED: {result}")

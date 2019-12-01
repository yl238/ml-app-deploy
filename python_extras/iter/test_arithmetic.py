from fractions import Fraction
from decimal import Decimal

from arithmetic_progression import ArithmeticProgression 


def test_ap():
    ap = ArithmeticProgression(0, 1, 3)
    assert list(ap) == [0, 1, 2]

    ap = ArithmeticProgression(0, 1/3, 1)
    assert list(ap) == [0.0, 0.3333333333333333, 0.6666666666666666]

    ap = ArithmeticProgression(0, Fraction(1, 3), 1)
    assert list(ap) == [Fraction(0, 1), Fraction(1, 3), Fraction(2, 3)]

    ap = ArithmeticProgression(0, Decimal('.1'), .3)
    assert list(ap) == [Decimal('0.0'), Decimal('0.1'), Decimal('0.2')]
    
if __name__ == '__main__':
    test_ap()
    print('Test passed!')
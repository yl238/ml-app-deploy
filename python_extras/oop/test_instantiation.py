from array import array

from vector import Vector

def test_instantiation():
    assert repr(Vector([3.1, 4.2])) == "Vector([3.1, 4.2])"
    assert repr(Vector((3, 4, 5))) == "Vector([3.0, 4.0, 5.0])"
    assert repr(Vector(range(4))) == 'Vector([0.0, 1.0, 2.0, 3.0])'

def test_abs():
    assert abs(Vector(())) == 0
    assert abs(Vector([0])) == 0
    assert abs(Vector((3, 4))) == 5

def test_slice():
    vec = Vector(range(7))
    assert vec[1:4] == array('d', [1.0, 2.0, 3.0])


if __name__ == '__main__':
    test_instantiation()
    test_abs()
    test_slice()

    print('All tests passed!')
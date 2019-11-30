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
    assert vec[1:4] == Vector([1.0, 2.0, 3.0])
    assert vec[-1:] == Vector([6.0])

def test_getattr():
    v = Vector(range(10))
    assert v.x == 0.0
    assert (v.y, v.z, v.t) == (1.0, 2.0, 3.0) 

def test_format():
    assert format(Vector([-1, -1, -1, -1]), 'h') == \
        '<2.0, 2.0943951023931957, 2.186276035465284, 3.9269908169872414>'
    assert format(Vector([2, 2, 2, 2]), '.3eh') == \
        '<4.000e+00, 1.047e+00, 9.553e-01, 7.854e-01>'
    assert format(Vector([0, 1, 0, 0]), '0.5fh') == \
        '<1.00000, 1.57080, 0.00000, 0.00000>'

if __name__ == '__main__':
    test_instantiation()
    test_abs()
    test_slice()
    test_getattr()
    test_format()

    print('All tests passed!')
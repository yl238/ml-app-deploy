from python_extras.oop.vector import Vector

def test_instantiation():
    assert Vector([3.1, 4.2]) == 'Vector([3.1, 4.2])'
    assert Vector((3, 4, 5)) == 'Vector([3.0, 4.0, 5.0])'



if __name__ == '__main__':
    test_instantiation()
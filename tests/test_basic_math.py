import operator

import numpy
import pytest

from oneflow_complex.tensor import ComplexTensor


def _get_complex_array(*shape):
    return numpy.random.randn(*shape) + 1j + numpy.random.randn(*shape)


@pytest.mark.parametrize(
    "op",
    [
        operator.add,
        lambda x, y: x.__radd__(y),
        operator.iadd,
        operator.sub,
        lambda x, y: x.__rsub__(y),
        operator.isub,
        operator.mul,
        lambda x, y: x.__rmul__(y),
        operator.imul,
        operator.truediv,
        lambda x, y: x.__rtruediv__(y),
        operator.itruediv,
        operator.matmul,
        lambda x, y: x.__rmatmul__(y),
    ],
)
@pytest.mark.parametrize("one_is_real", [True, False])
def test_binary_operation(op, one_is_real):
    n1 = _get_complex_array(10, 10)
    if one_is_real:
        n2 = numpy.random.randn(10, 10)
    else:
        n2 = _get_complex_array(10, 10)
    t1 = ComplexTensor(n1.copy())
    t2 = ComplexTensor(n2.copy())

    x = op(n1, n2)
    y = op(t1, t2)
    y = y.numpy()
    numpy.testing.assert_allclose(x, y)


@pytest.mark.parametrize(
    "nop,top",
    [
        (numpy.linalg.inv, lambda x: x.inverse()),
        (lambda x: x.conj(), None),
        (operator.neg, None),
    ],
)
def test_unary_operation(nop, top):
    if top is None:
        top = nop
    n1 = _get_complex_array(10, 10)
    t1 = ComplexTensor(n1.copy())

    x = nop(n1)
    y = top(t1)
    y = y.numpy()
    numpy.testing.assert_allclose(x, y)


@pytest.mark.parametrize("num", [-2, -1, 0, 1, 2, 0.5, -0.5, 1.5, -1.5])
def test_pow(num):
    n1 = _get_complex_array(10, 10)
    t1 = ComplexTensor(n1.copy())

    x = n1 ** num
    y = t1 ** num
    y = y.numpy()
    numpy.testing.assert_allclose(x, y)


def test_sum():
    n1 = _get_complex_array(10, 10)
    t1 = ComplexTensor(n1.copy())
    x = n1.sum()
    y = t1.sum()
    y = y.numpy()
    numpy.testing.assert_allclose(x, y)


def test_mean():
    n1 = _get_complex_array(10, 10)
    t1 = ComplexTensor(n1.copy())
    x = n1.mean()
    y = t1.mean()
    y = y.numpy()
    numpy.testing.assert_allclose(x, y)


def test_inverse():
    t = ComplexTensor(_get_complex_array(1, 10, 10))
    x = t @ t.inverse()
    numpy.testing.assert_allclose(x.real.numpy()[0], numpy.eye(10), atol=1e-11)
    numpy.testing.assert_allclose(x.imag.numpy()[0], numpy.zeros((10, 10)), atol=1e-11)


def test_inverse2():
    t = ComplexTensor(_get_complex_array(1, 10, 10))
    x = t @ t.inverse2()
    numpy.testing.assert_allclose(x.real.numpy()[0], numpy.eye(10), atol=1e-11)
    numpy.testing.assert_allclose(x.imag.numpy()[0], numpy.zeros((10, 10)), atol=1e-11)

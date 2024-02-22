import sys
import os
import pytest
import platform

from numpy.f2py.crackfortran import (
    _selected_int_kind_func as selected_int_kind,
    _selected_real_kind_func as selected_real_kind,
)
from . import util, conftest


@pytest.fixture(scope="module")
def kind_test_spec():
    spec = util.F2PyModuleSpec(
        test_class_name="TestKind",
        sources=[util.getpath("tests", "src", "kind", "foo.f90")],
    )
    return spec


@pytest.mark.skipif(sys.maxsize < 2**31 + 1, reason="Fails for 32 bit machines")
@pytest.mark.parametrize("_mod", ["kind_test_spec"], indirect=True)
def test_int(_mod):
    """Test `int` kind_func for integers up to 10**40."""
    selectedintkind = _mod.selectedintkind

    for i in range(40):
        assert selectedintkind(i) == selected_int_kind(
            i
        ), f"selectedintkind({i}): expected {selected_int_kind(i)!r} but got {selectedintkind(i)!r}"


@pytest.mark.parametrize("_mod", ["kind_test_spec"], indirect=True)
def test_real(_mod):
    """Test (processor-dependent) `real` kind_func for real numbers of up to 31 digits precision (extended/quadruple)."""
    selectedrealkind = _mod.selectedrealkind

    for i in range(32):
        assert selectedrealkind(i) == selected_real_kind(
            i
        ), f"selectedrealkind({i}): expected {selected_real_kind(i)!r} but got {selectedrealkind(i)!r}"


@pytest.mark.xfail(
    platform.machine().lower().startswith("ppc"),
    reason="Some PowerPC may not support full IEEE 754 precision",
)
@pytest.mark.parametrize("_mod", ["kind_test_spec"], indirect=True)
def test_quad_precision(_mod):
    """Test kind_func for quadruple precision [`real(16)`] of 32+ digits."""
    selectedrealkind = _mod.selectedrealkind

    for i in range(32, 40):
        assert selectedrealkind(i) == selected_real_kind(
            i
        ), f"selectedrealkind({i}): expected {selected_real_kind(i)!r} but got {selectedrealkind(i)!r}"

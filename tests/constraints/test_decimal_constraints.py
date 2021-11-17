from decimal import Decimal
from typing import Optional

import pytest
from hypothesis import given
from hypothesis.strategies import decimals
from pydantic import ConstrainedDecimal

from pydantic_factories.constraints.numbers import handle_constrained_decimal


def create_constrained_field(
    gt: Optional[Decimal] = None,
    ge: Optional[Decimal] = None,
    lt: Optional[Decimal] = None,
    le: Optional[Decimal] = None,
    multiple_of: Optional[Decimal] = None,
) -> ConstrainedDecimal:
    field = ConstrainedDecimal()
    field.ge = ge
    field.gt = gt
    field.lt = lt
    field.le = le
    field.multiple_of = multiple_of
    return field


def test_handle_constrained_decimal_without_constraints():
    result = handle_constrained_decimal(create_constrained_field())
    assert isinstance(result, Decimal)


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_ge(minimum):
    result = handle_constrained_decimal(create_constrained_field(ge=minimum))
    assert result >= minimum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_gt(minimum):
    result = handle_constrained_decimal(create_constrained_field(gt=minimum))
    assert result > minimum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_le(maximum):
    result = handle_constrained_decimal(create_constrained_field(le=maximum))
    assert result <= maximum


@given(decimals(allow_nan=False, allow_infinity=False, min_value=-1000000000, max_value=1000000000))
def test_handle_constrained_decimal_handles_lt(maximum):
    result = handle_constrained_decimal(create_constrained_field(lt=maximum))
    assert result < maximum


def test_handle_constrained_decimal_raises_for_non_zero_multiple_of():
    with pytest.raises(AssertionError):
        handle_constrained_decimal(create_constrained_field(multiple_of=Decimal(1)))


def test_handle_constrained_decimal_handles_multiple_of_zero_value():
    # due to a bug in the pydantic hypothesis plugin, this code can only be tested in isolation
    # see: https://github.com/samuelcolvin/pydantic/issues/3418
    assert handle_constrained_decimal(create_constrained_field(multiple_of=Decimal(0))) == 0
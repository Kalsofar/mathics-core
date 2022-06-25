from mathics.core.number import get_type

from mathics.core.atoms import (
    Complex,
    Integer,
    Real,
    Rational,
    String,
)
from mathics.core.symbols import (
    BaseElement,
    SymbolFalse,
    SymbolNull,
    SymbolTrue,
)
from mathics.core.systemsymbols import SymbolRule


def from_python(arg):
    """Converts a Python expression into a Mathics expression.

    TODO: I think there are number of subtleties to be explained here.
    In particular, the expression might beeen the result of evaluation
    a sympy expression which contains sympy symbols.

    If the end result is to go back into Mathics for further
    evaluation, then probably no problem.  However if the end result
    is produce say a Python string, then at a minimum we may want to
    convert backtick (context) symbols into some Python identifier
    symbol like underscore.
    """
    from mathics.core.convert.expression import to_mathics_list
    from mathics.core.expression import Expression
    from mathics.core.list import ListExpression

    if isinstance(arg, BaseElement):
        return arg

    number_type = get_type(arg)
    if arg is None:
        return SymbolNull
    if isinstance(arg, bool):
        return SymbolTrue if arg else SymbolFalse
    if isinstance(arg, int) or number_type == "z":
        return Integer(arg)
    elif isinstance(arg, float) or number_type == "f":
        return Real(arg)
    elif number_type == "q":
        return Rational(arg)
    elif isinstance(arg, complex):
        return Complex(Real(arg.real), Real(arg.imag))
    elif number_type == "c":
        return Complex(arg.real, arg.imag)
    elif isinstance(arg, str):
        return String(arg)
        # if arg[0] == arg[-1] == '"':
        #     return String(arg[1:-1])
        # else:
        #     return Symbol(arg)
    elif isinstance(arg, dict):
        entries = [
            Expression(
                SymbolRule,
                from_python(key),
                from_python(arg[key]),
            )
            for key in arg
        ]
        return ListExpression(*entries)
    elif isinstance(arg, list) or isinstance(arg, tuple):
        return to_mathics_list(*arg, elements_conversion_fn=from_python)
    elif isinstance(arg, bytearray) or isinstance(arg, bytes):
        return Expression(SymbolByteArray, ByteArrayAtom(arg))
    else:
        raise NotImplementedError

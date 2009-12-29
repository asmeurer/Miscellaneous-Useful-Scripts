#!/usr/bin/env python
#
#  SymPy Stuff That Didn't Make it in.py
"""
This is a collection of stuff that I wrote that didn't make it into SymPy for
whatever reason.  I spent too much time on these things to just delete them
entirely.

Aaron Meurer
"""

# Bad algorithm (slow).  Now done by expand(mul)
def distribute(expr):
    """
    Recursively takes a Mul with Adds and turns it into just an Add of Muls
    This should probably be refactored into expand.  See Issue 1455.  Note that
    this is slower than just expand, so unless you only want distribution, use
    that.  The advantage is that it will not do things like expand logs and
    exponentials.  It only distributes on the top level, i.e., it doesn't do
    anything with things like sin(x*(y+z)).

    Examples:
    >>> from sympy import *
    >>> x, y, z, a, b = symbols('xyzab')
    >>> distribute(x*(y+z)*(a+b))
    a*x*y + a*x*z + b*x*y + b*x*z

    >>> expand(log(x**2)*(a+b))
    2*a*log(x) + 2*b*log(x)
    >>> distribute(log(x**2)*(a+b))
    a*log(x**2) + b*log(x**2)
    >>> expand(exp(x+y)*(a+b))
    a*exp(x)*exp(y) + b*exp(x)*exp(y)
    >>> distribute(exp(x+y)*(a+b))
    a*exp(x + y) + b*exp(x + y)

    >>> distribute(sin(x*(y+z)))
    sin(x*(y + z))
    """
    if any(not getattr(i, 'is_commutative', False) for i in expr.atoms(Symbol)):
        # TODO: non_commutative case needs to be implemented
        return expr
    tryagain = _distribute(expr)
    while tryagain != expr:
        expr = tryagain
        tryagain = _distribute(expr)
    return expr

def _distribute(expr, i=0):
    if expr.is_Add:
        return Add(*(_distribute(i) for i in expr.args))
    if expr.is_Mul:
        term = expr.args[i]
    else:
        term = expr
    if term.is_Add:
        return Add(*(Mul(*(_distribute(expr.extract_multiplicatively(term)),i)) for i in term.args))
    else:
        i += 1
        if i < len(expr.args):
            return _distribute(expr, i)
        else:
            return expr


# Here is the test.  Compare to expand(mul), expecially the long one for speed.
def test_distribute():
    x, y, z = symbols('xyz')
    assert distribute(x*(y+z)) == x*y + x*z
    assert distribute(x*(y+z)*y*(x+z)) == x**2*y**2 + x*y*z**2 + x*z*y**2 + y*z*x**2
    assert distribute(x+y) == x+y
    assert distribute(x*y) == x*y
    assert distribute((x+1)*(x+2)*(x+3)*(x+4)*(x+5)*(x+6)*(x+7)*(x+8)) == \
    40320 + 109584*x + 118124*x**2 + 67284*x**3 + 22449*x**4 + 4536*x**5 + \
    546*x**6 + 36*x**7 + x**8
    assert distribute((x+y)*(x+z)) == x*y + x*z + y*z + x**2
    assert distribute((x+1)*(y+1)) == 1 + x + y + x*y
    assert distribute(sin(x)*(sin(x)+cos(x)**2/sin(x))) == cos(x)**2 + sin(x)**2
    assert distribute((x+y+z)*(x+1)*y) == x*y + y*z + x*y*z + y**2 + x*y**2 + y*x**2
    assert distribute((log(x**2)+log(y))*z) == z*log(y) + z*log(x**2)
    assert distribute(exp(x+y)*(x+y)) == x*exp(x + y) + y*exp(x + y)
    assert distribute((x*(x+y)**(x*(x+y)))) == x*(x + y)**(x*(x + y))


# Not the best way to test because of import *, but neat reverse try clause
@XFAIL
def test_issue_1454():
    from sympy import *
    assert not hasattr(x, 'k')
    try:
        i
    except NameError:
        pass
    else:
        raise ValueError, "Global variable i should not be defined."

# Might actually be useful for something some day.
# (And it was.  Now part of separatevars)
def _separatemul(expr, *symbols):
    """
    Takes in a Mul and returns a dictionary of separate parts in the symbols.
    Any part that has no symbols is returned as _coeff in the dictionary.
    If the expression is not separable, it returns None.

    Example:
    >>> _separatemul(2*x**2*sin(y),x,y,z)
    {x:x**2, y:sin(y), z:1, _coeff:2}
    """
    assert expr.is_Mul
    ret = dict(((i,sympify(1)) for i in symbols))
    ret[_coeff] = sympify(1)
    for i in expr.args:
        expsym = i.atoms(Symbol)
        if len(set(symbols).intersection(expsym)) > 1:
            return None
        if len(set(symbols).intersection(expsym)) == 0:
            # There are no symbols, so it is part of the coefficient
            ret[_coeff] *= i
        else:
            ret[expsym.pop()] *= i

    return ret


# -*- coding: latin-1 -*-

from myhdl import *
import unittest
from unittest import TestCase
from random import randrange
from mux2 import *


class mux2_unit_test( TestCase ):

    def test_case_mux2( self ):
        """Testando 1000 vezes o mux"""
        def test( a, b, sel, result ):
            for i in range( 10 ):
                r_a, r_b = intbv( randrange( 32 ) )[32:], intbv( randrange( 32 ) )[32:]
                a.next, b.next = r_a, r_b
                sel.next = randrange( 2 )
                yield delay( 10 )
                if sel.val == 0:
                    expected = r_a
                else:
                    expected = r_b
                actual = result
                self.assertEqual( actual, expected )

        for width in range( 1000 ):
            a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
            sel = Signal( intbv( 0 )[1:] )
            mux = mux2( a, b, sel, result )
            check = test( a, b, sel, result )
            sim = Simulation( mux, check )
            sim.run( quiet=1 )

if __name__ == '__main__':
    unittest.main()

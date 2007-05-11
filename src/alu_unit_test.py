from myhdl import *
import unittest
from unittest import TestCase
from random import randrange
from alu import *


class alu_unit_test( TestCase ):

    def test_case_addition( self ):
        """ checando a soma entre inteiros """
        def test( a, b, sel, result, error ):
            for i in range( 10 ):
                r_a, r_b = randrange( 32 ), randrange( 32 )
                a.next, b.next = r_a, r_b
                sel.next = 0x0
                yield delay( 10 )
                expect = r_a + r_b
                actual = result
                self.assertEqual( actual, expect )

        for width in range( 100 ):
            a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
            sel = Signal(intbv(0)[4:])
            error = Signal(intbv(0)[1:])
            sum = ALU( a, b, sel, result, error )
            check = test(a, b, sel, result, error)
            sim = Simulation( sum, check )
            sim.run( quiet=1 )

    def test_case_subtraction( self ):
        """ checando a subtracao entre inteiros """
        def test( a, b, sel, result, error ):
            for i in range( 10 ):
                r_a, r_b = randrange( 32 ), randrange( 32 )
                a.next, b.next = r_a, r_b
                sel.next = 0x1
                yield delay( 10 )
                expect = r_a - r_b
                actual = result
                self.assertEqual( actual, intbv(expect)[32:] )

        for width in range( 100 ):
            a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
            sel = Signal(intbv(0)[4:])
            error = Signal(intbv(0)[1:])
            sum = ALU( a, b, sel, result, error )
            check = test(a, b, sel, result, error)
            sim = Simulation( sum, check )
            sim.run( quiet=1 )


if __name__ == '__main__':
    unittest.main()

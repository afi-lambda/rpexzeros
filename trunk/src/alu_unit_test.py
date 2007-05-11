#!/usr/bin/python

#-------------------------
# Module Unittest ALU
#-------------------------
# Author: Rodrigo Peixoto
# Date: May 07 2007
#------------------------------------------------
# Description: This is the unittest of the
# rpexz processor's Arithmetic logic unit.
#------------------------------------------------

from myhdl import *
import unittest
from unittest import TestCase
from random import randrange
from alu import *


class alu_unit_test( TestCase ):

    def abstract_test_case( self, selection , func ):
        def test( a, b, sel, result, error ):
            for i in range( 10 ):
                r_a, r_b = randrange( 32 ), randrange( 32 )
                a.next, b.next = r_a, r_b
                sel.next = selection
                yield delay( 10 )
                expect = func( r_a, r_b )
                actual = result
                self.assertEqual( actual, intbv( expect )[32:] )

        for width in range( 100 ):
            a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
            sel = Signal( intbv( 0 )[4:] )
            error = Signal( intbv( 0 )[1:] )
            sum = ALU( a, b, sel, result, error )
            check = test( a, b, sel, result, error )
            sim = Simulation( sum, check )
            sim.run( quiet=1 )

    def test_case_addition( self ):
        """ Check Addition between 32 bit vectors"""
        return self.abstract_test_case( 0x0, lambda a, b: a+b )

    def test_case_subtraction( self ):
        """ Check Subtraction between 32 bit vectors"""
        return self.abstract_test_case( 0x1, lambda a, b: a - b )

    def test_case_and( self ):
        """ Check AND bit between 32 bit vectors"""
        return self.abstract_test_case(0x2, lambda a,b : a & b)

    def test_case_or( self ):
        """ Check OR bit between 32 bit vectors"""
        return self.abstract_test_case(0x3, lambda a,b : a | b)

    def test_case_not( self ):
        """ Check NOT bit 32 bit vectors"""
        return self.abstract_test_case(0x4, lambda a,b : ~ a )

    def test_case_xor( self ):
        """ Check XOR bit between 32 bit vectors"""
        return self.abstract_test_case(0x5, lambda a,b : a ^ b )

    def test_case_Multiplication( self ):
        """ Check Multiplication between 32 bit vectors"""
        return self.abstract_test_case(0x6, lambda a,b : a * b )

    def test_case_Division( self ):
        """ Check Division between 32 bit vectors"""
        def test( a, b, sel, result, error ):
            for i in range( 10 ):
                r_a, r_b = randrange( 32 ), randrange( 32 )
                #r_a, r_b = randrange( 32 ), intbv(0)[32:]
                a.next, b.next = r_a, r_b
                sel.next = 0x7
                yield delay( 10 )
                if r_b == intbv(0)[32:]:
                    self.assertEquals( error , intbv(1)[1:] )
                    self.assertEquals( result , intbv(0)[32:] )
                else:
                    expect = r_a // r_b
                    actual = result
                    self.assertEqual( actual, intbv(expect)[32:] )

        for width in range( 100 ):
            a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
            sel = Signal( intbv( 0 )[4:] )
            error = Signal( intbv( 0 )[1:] )
            sum = ALU( a, b, sel, result, error )
            check = test( a, b, sel, result, error )
            sim = Simulation( sum, check )
            sim.run( quiet=1 )


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python2.5
#import myhdl
from myhdl import *
#from myhdl import always_comb, Signal, intbv, Simulation
from random import randrange

def ALU( a, b, sel, result, error ):
    """
    a,b - input value (32 bits signed interger)
    sel - selection (4 bits) {
        0000 - Additoin
        0001 - Subtraction
        0010 - AND
        0011 - OR
        0100 - NOT
        0101 - XOR
        0110 - Multiplication
        0111 - Division
        ...  - (Don't care) Future expansion

    result - output value (32 bits)

    """

    @always_comb
    def execute_opertion():
        error.next = 0
        ###Addition
        if sel == 0x0:
            result.next = a + b
        ###Subtraction
        elif sel == 0x1:
            result.next = intbv( a - b )[32:]
        ###And
        elif sel == 0x2:
            result.next = a and b
        ###Or
        elif sel == 0x3:
            result.next = a or b
        ###Not
        elif sel == 0x4:
            result.next = not a
        ###XOR
        elif sel == 0x5:
            result.next = a ^ b
        ###Multiplication
        elif sel == 0x6:
            result.next = a * b
        ###Division
        elif sel == 0x7:
            if b == 0x0:
                error.next = 1
                result.next = 0x0
            else:
                result.next = a / b


        else: raise "Error - Selection Not implemented!"
    return execute_opertion

def basic_test():

    a, b, result = [Signal( intbv( 0 )[32:] ) for i in range( 3 )]
    sel = Signal( intbv( 0 )[4:] )
    error = Signal( intbv( 0 )[1:] )

    alu = ALU ( a, b, sel, result, error )

    def test():
        print "Sel  a    b    result      error"
        for x in range( 100 ):
            a.next, b.next, sel.next = randrange( 32 ), 0, randrange( 8 )
            yield delay( 10 )
            print "%-4s %-4s %-4s %-11s %s" % ( hex(sel), hex(a), hex(b), hex(result), error )

    teste = test()

    sim = Simulation( alu, teste )
    sim.run( 1000 )

if __name__ == '__main__':
    basic_test()

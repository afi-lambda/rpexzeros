#!/usr/bin/python
# -*- coding: latin-1 -*-
#--------------------------
# Module registrador
# Author: Rodrigo Peixoto
#--------------------------

from random import randrange
from exceptions  import Exception
from myhdl import *
from utils.clock_generator import *

HIGH, LOW = 1, 0

def registrador( clk, input_1, enable, clear, output_1 ):
    """
    Guarda vetores de oito bits
    clk:( 1 bit ) - clock do sistema
    inp: (vetor de bits tamanho 8) - entrada do registrador
    enable: (vetor de bits tamanho 8) - habilita o armazenamento da entrada
    clear: ( 1 bit ) - zera o registrador
    output: (vetor de bits tamanho 8) - saída, valor armazenado
    """
    @always( clk.posedge )
    def process():
        if clear == HIGH:
            output_1.next = 0
        else:
            if enable:
                output_1.next = input_1
    return process


def test_bench():
    clk, enable, clear = [Signal( intbv( 0 )[1:] ) for i in range( 3 )] # apenas replicando 3x
    input_1, output_1 = Signal( intbv( 0 )[8:] ), Signal( intbv( 0 )[8:] )

    reg = registrador( clk, input_1, enable, clear, output_1 )
    clkgen = clk_gen( clk )
    @instance
    def stimgen():
        for i in range( 10 ):
            input_1.next, enable.next, clear.next = randrange( 256 ), randrange( 2 ), randrange( 2 )
            yield clk.negedge
        raise StopSimulation

    @instance
    def monitor():
        print "input enable clear output"
        while 1:
            yield clk.posedge
            print "%-6s%-7s%-6s%-6s" % ( hex( input_1 ), enable, clear, hex( output_1 ) )
    return clkgen, stimgen, reg, monitor

if __name__ == '__main__':
    tb = test_bench()
    Simulation( tb ).run()

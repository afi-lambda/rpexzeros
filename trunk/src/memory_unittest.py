#!/usr/bin/python
#-*- coding: latin-1 -*-
#-------------------------
# Module Unittest ALU
#-------------------------
# Author: Rodrigo Peixoto
# Date: May 07 2007
#------------------------------------------------
# Description: This is the unittest of the
# rpexz processor's memory.
#------------------------------------------------

from myhdl import *
from random import randrange
from unittest import TestCase
from utils.clock_generator import *
import memory
import unittest

MEM_AUX = memory.fetch_system_memory()

class Memory_UnitTest( TestCase ):

    def btest_case_verifying_memory( self ):
        """Verificando o conteudo da memoria, fazendo varredura geral
        """
        def test( clk, chip_select, address, load_store, data_in, data_out ):
            l = len( MEM_AUX )
            for i in range( l ): #Sequencial
                chip_select.next = 1
                load_store.next = 0
                address.next = i
                yield clk.posedge
                yield clk.posedge
                chip_select.next = 0
                self.assertEqual( data_out, MEM_AUX[i] )

            for i in range( l ): #Aleatoria
                chip_select.next = 1
                load_store.next = 0
                aleatorio = randrange( l )
                address.next = aleatorio
                yield clk.posedge
                yield clk.posedge
                self.assertEqual( data_out, MEM_AUX[aleatorio] )

            raise StopSimulation

        clk_s = Signal( bool( 1 ) )
        clkgen = clk_gen( clk_s )
        address, data_in, data_out =[Signal( intbv( 0 )[32:] ) for i in range( 3 )]
        chip_select, load_store = [Signal( bool( 0 ) ) for i in range( 2 )]

        mem_test = memory.memory( clk_s, chip_select, address, load_store, data_in, data_out )

        #check = test( clk_s, chip_select, address, load_store, data_in, data_out )
        ch = traceSignals(test, clk_s, chip_select, address, load_store, data_in, data_out)
        #me = traceSignals(memory.memory, clk_s, chip_select, address, load_store, data_in, data_out  )
        #sim = Simulation( mem_test, check, clkgen )
        sim = Simulation( ch, mem_test, clkgen )
        sim.run( quiet=1 )

    def test_case_store_data_memory( self ):
        """Inserindo dados na memoria
        """
        MEM_AUX = memory.fetch_system_memory()
        def test( clk, chip_select, address, load_store, data_in, data_out ):
            count = len( MEM_AUX )
            for i in range( count+10 , count+100 ):
                chip_select.next = 1
                load_store.next = 1
                address.next = i
                data_in.next = i*32
                MEM_AUX[i]=i*32
                yield clk.posedge
                yield clk.posedge
                #chip_select.next = 1
                load_store.next = 0
                #address.next = i
                data_in.next = 0
                yield clk.posedge
                yield clk.posedge
                chip_select.next = 0
                self.assertEqual( data_out, MEM_AUX[i] )

            raise StopSimulation

        clk_s = Signal( bool( 1 ) )
        clkgen = clk_gen( clk_s )
        address, data_in, data_out =[Signal( intbv( 0 )[32:] ) for i in range( 3 )]
        chip_select, load_store = [Signal( bool( 0 ) ) for i in range( 2 )]

        mem_test = memory.memory( clk_s, chip_select, address, load_store, data_in, data_out )
        #check = test( clk_s, chip_select, address, load_store, data_in, data_out )
        #sim = Simulation( mem_test, check, clkgen )
        te = traceSignals(test, clk_s, chip_select, address, load_store, data_in, data_out)
        sim = Simulation( mem_test, te, clkgen )
        sim.run( quiet=1 )

if __name__ == '__main__':
    unittest.main()
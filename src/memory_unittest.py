#!/usr/bin/python
# -*- coding: latin-1
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
#import unittest
MEM_AUX = []


class Memory_UnitTest( TestCase ):

    def test_case_verifying_memory( self ):
        '''Verificando o conteudo da memoria, fazendo varredura geral
        '''
        def test( clk, enable, address, load_store, data_in, data_out ):

            for i in range( len( MEM_AUX ) ): #Sequencial
                enable.next = 1
                load_store.next = 0
                address.next = i
                yield clk.posedge
                yield clk.posedge
                enable.next = 0
                self.assertEqual( data_out, MEM_AUX[i] )

            for i in range( len( MEM_AUX ) ): #Aleatoria
                enable.next = 1
                load_store.next = 0
                aleatorio = randrange( i )
                address.next = aleatorio
                yield clk.posedge
                yield clk.posedge
                self.assertEqual( data_out, MEM_AUX[aleatorio] )

            raise StopSimulation

        clk_s = Signal( bool( 1 ) )
        clkgen = clk_gen( clk_s )
        address, data_in, data_out =[Signal( intbv( 0 )[32:] ) for i in range( 3 )]
        enable, load_store = [Signal( bool( 0 ) ) for i in range( 2 )]

        mem_test = memory.memory( clk_s, enable, address, load_store, data_in, data_out )
        check = test( clk_s, enable, address, load_store, data_in, data_out )
        sim = Simulation( mem_test, check, clkgen )
        sim.run( quiet=1 )

    def test_case_store_data_memory( self ):
        '''Inserindo dados na memoria
        '''
        MEM_AUX = memory.fetch_system_memory()
        def test( clk, enable, address, load_store, data_in, data_out ):
            count = len( MEM_AUX )
            for i in range( count+1 , count+100 ):
                enable.next = 1
                load_store.next = 1
                address.next = i
                data_in.next = i
                MEM_AUX.insert(i,i)
                yield clk.posedge
                yield clk.posedge
                enable.next = 1
                load_store.next = 0
                address.next = i
                data_in.next = 0
                yield clk.posedge
                yield clk.posedge
                self.assertEqual( data_out, MEM_AUX[i] )

            raise StopSimulation

        clk_s = Signal( bool( 0 ) )
        clkgen = clk_gen( clk_s )
        address, data_in, data_out =[Signal( intbv( 0 )[32:] ) for i in range( 3 )]
        enable, load_store = [Signal( bool( 0 ) ) for i in range( 2 )]

        mem_test = memory.memory( clk_s, enable, address, load_store, data_in, data_out )
        check = test( clk_s, enable, address, load_store, data_in, data_out )
        sim = Simulation( mem_test, check, clkgen )
        sim.run( quiet=1 )


if __name__ == '__main__':
    unittest.main()
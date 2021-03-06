# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################


import time

from base import ConnectedSocketTestCase
from ptc.constants import RETRANSMISSION_TIMEOUT, MAX_RETRANSMISSION_ATTEMPTS
from ptc.packet import ACKFlag


class RetransmissionTest(ConnectedSocketTestCase):
    
    def assert_retransmission(self, first_packet, second_packet):
        self.assertEquals(first_packet.get_seq_number(),
                          second_packet.get_seq_number())
        self.assertEquals(first_packet.get_ack_number(),
                          second_packet.get_ack_number())
        self.assertEquals(first_packet.get_payload(),
                          second_packet.get_payload())
        
    def get_retransmitted_packets(self):
        packets = list()
        while True:
            try:
                packet = self.receive(self.DEFAULT_TIMEOUT)
                packets.append(packet)
            except Exception:
                break
        # El primer paquete debería ser el original.
        return packets[1:]
    
    def wait_until_total_retransmission_time_expires(self):
        time.sleep((1 + MAX_RETRANSMISSION_ATTEMPTS) * RETRANSMISSION_TIMEOUT)
    
    def test_retransmission_after_lost_packet(self):
        self.socket.send(self.DEFAULT_DATA)
        first_packet = self.receive(self.DEFAULT_TIMEOUT)
        time.sleep(RETRANSMISSION_TIMEOUT)
        second_packet = self.receive(self.DEFAULT_TIMEOUT)

        self.assert_retransmission(first_packet, second_packet)
        
    def test_give_up_after_enough_retransmissions(self):
        self.socket.send(self.DEFAULT_DATA)
        self.wait_until_total_retransmission_time_expires()
        packets = self.get_retransmitted_packets()
        
        self.assertEquals(MAX_RETRANSMISSION_ATTEMPTS, len(packets))
        self.assertFalse(self.socket.is_connected())
        
    def test_packet_removed_from_retransmission_queue_after_ack(self):
        size = 10
        data = self.DEFAULT_DATA[:size]
        ack_number = self.DEFAULT_ISS + size
        ack_packet = self.packet_builder.build(flags=[ACKFlag],
                                               seq=self.DEFAULT_IRS,
                                               ack=ack_number,
                                               window=self.DEFAULT_IW)
        self.socket.send(data)
        self.receive()
        self.send(ack_packet)
        self.wait_until_total_retransmission_time_expires()
        packets = self.get_retransmitted_packets()
        
        self.assertGreater(MAX_RETRANSMISSION_ATTEMPTS, len(packets))
        self.assertTrue(self.socket.is_connected())
        
    def test_unaccepted_ack_ignored_when_updating_retransmission_queue(self):
        ack_number = self.DEFAULT_ISS + self.DEFAULT_IW + 1
        ack_packet = self.packet_builder.build(flags=[ACKFlag],
                                               seq=self.DEFAULT_IRS,
                                               ack=ack_number,
                                               window=self.DEFAULT_IW)
        self.socket.send(self.DEFAULT_DATA)
        self.send(ack_packet)
        self.wait_until_total_retransmission_time_expires()
        packets = self.get_retransmitted_packets()
        
        self.assertEquals(MAX_RETRANSMISSION_ATTEMPTS, len(packets))
        self.assertFalse(self.socket.is_connected())

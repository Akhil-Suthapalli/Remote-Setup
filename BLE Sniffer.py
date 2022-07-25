# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:40:02 2022

@Author: Akhil Suthapalli - R&D
@Contact: Suthapalli.Akhil@tvsmotor.com
@Mobile: +91 9494475575
"""


from SnifferAPI import Sniffer

a = Sniffer.Sniffer()
a.setPortnum("COM8")
a.start()
a.scan()


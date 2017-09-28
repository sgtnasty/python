#!/usr/bin/env python


import os
import sys
import uuid
import datetime
import random
import logging
import argparse
from enum import Enum

WeaponType = Enum('Weapon Slot', 'AutoRifle PulseRifle ScoutRifle HandCannon SniperRifle Shotgun FusionRifle Sidearm MachineGun RocketLancher Sword')
WeaponSlot = Enum('Weapon Type', 'Primary Secondary Heavy')
Rarity = Enum('Rarity', 'Common Uncommon Rare Legendary Exotic')


class Weapon(object):

    def __init__(self, name, slot, wtyp, atk, flav, rar):
        self.name = name
        self.weapon_slot = slot
        self.weapon_type = wtyp
        self.attack = atk
        self.flavor = flav
        self.rarity = rar


class AutoRifle(Weapon):

    def __init__(self, name, wslot, atk, flav, rar, rld, rng, sta, mag, rof, imp):
        super(AutoRifle, self).__init__(name, wslot, WeaponType.AutoRifle, atk, flav, rar)
        self.reload = rld
        self.range = rng
        self.stability = sta
        self.magazine = mag
        self.rateoffire = rof
        self.impact = imp
        pass

    def show(self):
        print(self.name.upper())
        print('{} - {}'.format(self.weapon_slot.name, self.weapon_type.name))
        print('\"{}\"'.format(self.flavor))
        print(self.rarity.name)
        print(u'  Rate of Fire: [******    ] {}'.format(self.rateoffire))
        print(u'  Impact:       [*****     ] {}'.format(self.impact))
        print(u'  Range:        [******    ] {}'.format(self.range))
        print(u'  Stability:    [***       ] {}'.format(self.stability))
        print(u'  Reload:       [********* ] {}'.format(self.reload))
        print(u'  Magazine: {}'.format(self.magazine))


if __name__ == '__main__':
    shadow_price = AutoRifle('Shadow Price', WeaponSlot.Primary, 250, 'A precision auto rifle left behind by Toland, the Shattered. It asks so little, and it offers so much.', Rarity.Legendary, 52, 25, 31, 19, 77, 28)
    shadow_price.show()

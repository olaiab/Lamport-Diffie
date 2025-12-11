#!/usr/bin/env python3

import secrets
import hashlib

NBITS = 256
NBYTES = NBITS // 8

class LD_OTS:
    '''
    Lamport-Diffie One time signature scheme (LD-OTS).
    Reads and writes 256 bit keys from/to files.
    Signs and verifies messages.
    '''
    @classmethod
    def loadSignature(self, filename):
        signature = []
        with open(filename, "rt") as f:
            for line in f.readlines():
                signature.append(bytes.fromhex(line[:-1]))
        return signature

    def __init__(self):
        self.public = None
        self.private = None

    def loadPublic(self, filename):
        self.public = self._loadKey(filename)

    def loadPrivate(self, filename):
        self.private = self._loadKey(filename)

    def _loadKey(self, filename):
        key = [[], []]
        with open(filename, "rt") as f:
            for line in f.readlines():
                if len(key[0]) == NBITS:
                    raise Exception('Incorrect file format.')
                pair = bytes.fromhex(line[:-1])
                if len(pair) != 2*NBYTES:
                    raise Exception('Incorrect file format.')
                key[0].append(pair[:NBYTES])
                key[1].append(pair[NBYTES:])
        return key

    def sign(self, message):
        '''
        Returns the signature of message with the private key.
        Should be used just once!
        To be probabilistic the actually signed digest is the SHA-256
        of the concatenation of a random 256 bits value and the message.
        '''
        assert self.private, 'No private key available'
        r = secrets.token_bytes(NBYTES)
        h = hashlib.sha256(r + message).digest()
        signature = [r]
        for ibyte, byte in enumerate(h):
            bits = format(byte, 'b').zfill(8)
            for ibit, bit in enumerate(bits):
                signature.append(self.private[int(bit)][ibyte*8 + ibit])
        return signature

    def verify(self, message, signature):
        '''
        Returns true if signature is a valid signature of the message
        with the public key.
        '''
        assert self.public, 'No public key available'
        # To be implemented

        '''
        d=mezuaren hasha
        h(Si) sinaduraren hasha
        Yi gako publikoa
        '''

        'mezua laburtu'
        r=signature[0]
        d=hashlib.sha256(r+message).digest()
        'd zeharkatu'
        for ibyte, byte in enumerate(d): 
            'byte bakoitzeko bitak lortu'
            bits = format(byte, 'b').zfill(8) 
            'bitak zeharkatu'
            for ibit, bit in enumerate(bits):
                '''
                if (bit=='0'):
                    '0 -> h(Si) eta Y0 konparatu'
                    if hashlib.sha256(signature[1 + ibyte*8 + ibit]).digest() != self.public[0][ibyte*8 + ibit]:
                        return False
                elif (bit=='1'):
                    '1 -> h(Si) eta Y1 konparatu'
                    if hashlib.sha256(signature[1 + ibyte*8 + ibit]).digest() != self.public[1][ibyte*8 + ibit]:
                        return False
                '''
                'Errazago'
                if hashlib.sha256(signature[1 + ibyte*8 + ibit]).digest() != self.public[int(bit)][ibyte*8 + ibit]:
                        return False
                
        return True
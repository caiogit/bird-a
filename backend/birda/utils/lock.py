# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import sys
import time
import socket
import random

DEBUG = True

# ============================================================================ #

def get_lock(process_name):
	"""
	Using named socks, tries to get a lock on a specified name.
	
	If lock is already acquired by some other process, return None.
	
	! Warning !
	In order to not lose the acquired lock, the returned object have to
	be stored in an active variable (e.g. global), in order to not allow
	garbage collector to dismiss it.
	
	:param process_name: "Token" on which acquire the lock (e.g. the class name)
	:return: Socket Object if the lock is sucessfully acquired, None otherwise
	"""
	
	lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	try:
		lock_socket.bind('\0' + process_name)
		return lock_socket
	except socket.error:
		return None

# ---------------------------------------------------------------------------- #

def wait_for_lock(process_name, max_sleep=0.2):
	"""
	Using named socks, tries to get a lock on a specified name.
	
	If lock is already acquired, retries at random intervals.
	
	! Warning !
	In order to not lose the acquired lock, the returned object have to
	be stored in an active variable (e.g. global), in order to not allow
	garbage collector to dismiss it.
	
	:param process_name: "Token" on which acquire the lock (e.g. the class name)
	:param max_sleep: max wait time between two get_lock trials
	:return: Socket Object if the lock is sucessfully acquired, None otherwise
	"""
	
	if DEBUG:
		print "Acquiring lock... ",
		sys.stdout.flush()
		
	# -------------------------------------- #
	lock = None
	trials = 0
	
	while not lock:
		trials += 1
		lock = get_lock(process_name)
		if not lock:
			random_wait = max_sleep * random.random()
			#print random_wait
			time.sleep(random_wait)
	# -------------------------------------- #
	
	if DEBUG:
		print "Acquired (%s trials)" % trials
		sys.stdout.flush()
	
	return lock

# ---------------------------------------------------------------------------- #

def release_lock(lock):
	"""
	Releases la lock
	
	:param lock: Lock object (i.e. socket) returned by a get_lock() or a wait_for_lock()
	:return: None
	"""
	
	# -------------------------------------- #
	lock.shutdown(socket.SHUT_RDWR)
	lock.close()
	# -------------------------------------- #
	
	if DEBUG:
		print "Lock released"
		sys.stdout.flush()

# ============================================================================ #

if __name__ == '__main__':
	pass
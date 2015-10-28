# -*- coding: utf-8 -*-

class Controller(object):

	# birda.storage.storage.Storage
	storage = None

	# Dictionary: "ontology_id" -> birda.w_model.birda_instance.BirdaInstance
	birda_instances = {}

	# ----------------------------------------------------------------------- #

	def __init__(self):
		pass

	# ----------------------------------------------------------------------- #

	def set_storage(self, storage):
		"""
		Set the current storage

		:param storage: (birda.storage.storage.Storage) New storage
		:return: None
		"""

		# Tear down actions of the previous storage, if any
		if storage:
			pass

		# Storage registration
		self.storage = storage

		# Load of birda_instances served by the new storage


	# ----------------------------------------------------------------------- #

	def load_ontologies(self):
		pass

	# ----------------------------------------------------------------------- #

	def get_ontologies(self):
		"""
		Get a list all all available ontologies

		:return: List of dictionaries in the form {'id':'...', 'title':'...', 'description':'...'}
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #
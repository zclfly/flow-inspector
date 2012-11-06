"""
Backend wrappers. Select and create the appropriate objects for 
backend communication.

Currently supported backends:
	- mongodb
	- mysql
	- oracle

Author: Lothar Braun 
"""

import sys
import config
import common
import time
import operator

class Collection:
	"""
		This class is a wrapper for the mongo db collection classes
		it takes requests for storing and querying data from the
		application and passes it to the backend classes, which are
		then responsible for storing and retriving the data in/from 
		the actual database.
		For backends other than mongo, a collection represents a 
		table (SQL) or another appropriate collection for flows that
		belong to the same cagegory
	"""
	def __init__(self, backendObject, collectionName):
		self.backendObject = backendObject
		self.collectionName = collectionName
		self.name = collectionName

	def createIndex(self, fieldName):
		"""
		Creates an index on the given field if the database 
		supports indexes
		"""
		self.backendObject.createIndex(self.collectionName, fieldName)

	def update(self, statement, document, insertIfNotExist):
		"""
		Updates or creates a flow in the database. 
		- statement - contains the id of the flow in the database (_id for mongo, primary key for sql)
		- document - contains the properties of the flow
		- insertIfNotExist: true: insert flow into db if it doesn't exist; false: only update entries of existing flows, do not create new flow
		"""
		self.backendObject.update(self.collectionName, statement, document, insertIfNotExist)

	def bucket_query(self, query_params):
		"""
		Queries the database for a set of flows that match the given properties. "query_param" is a dictionary with the following entries:
		- spec - mongo specific spec for the query. already encodes the arguments (applies only to mongo)
		- fields - database fields that should be queried and returned by the database
		- sort - list of fields that should be sorted, including the sort direction
		- count - maximum number of flows that should be returned
		- start_bucket: start interval for flows
		- end_bucket: end interval for flow queries
		- resolution: desired time resolution
		- bucket_size: size of buckets to be queried
		- biflow: whether we should have biflow aggregation or not
		- include_ports: only select flows that involve the ports in this list
		- exclude_ports: only select flows that do not involve the ports in this list
		- inlude_ips: only select flows that involve the ips in this list
		- exclude_ips: only select flows that do not involve the ips in this list
		- batch_size: database should select the flows in batch sizes of batchSize (ignored for most backends)
		"""
		return self.backendObject.bucket_query(self.collectionName, query_params)

	def index_query(self, query_params):
		"""
		Queries the database for static indexes on all flows in the database. query_params is a dict with the following entries:
		- spec - mongo specific spec for the query. already encodes the arguments (applies only to mongo)
		- fields - database fields that should be queried and returned by the database
		- sort - list of fields that should be sorted, including the sort direction
		- count - maximum number of flows that should be returned
		- start_bucket: start interval for flows
		- end_bucket: end interval for flow queries
		- resolution: desired time resolution
		- bucket_size: size of buckets to be queried
		- biflow: whether we should have biflow aggregation or not
		- include_ports: only select flows that involve the ports in this list
		- exclude_ports: only select flows that do not involve the ports in this list
		- inlude_ips: only select flows that involve the ips in this list
		- exclude_ips: only select flows that do not involve the ips in this list
		- batch_size: database should select the flows in batch sizes of batchSize (ignored for most backends)
		"""

		# remove any bucket requests
		return self.backendObject.index_query(self.collectionName, query_params)
 
	def dynamic_index_query(self, name, query_params):
		"""
		Queries the database for dynamic indexes which are calculated based on the start and end intervals
		- name - index name (ports or nodes)
		query_params is a dict with the following entries:
		- spec - mongo specific spec for the query. already encodes the arguments (applies only to mongo)
		- fields - database fields that should be queried and returned by the database
		- sort - list of fields that should be sorted, including the sort direction
		- count - maximum number of flows that should be returned
		- start_bucket: start interval for flows
		- end_bucket: end interval for flow queries
		- resolution: desired time resolution
		- bucket_size: size of buckets to be queried
		- biflow: whether we should have biflow aggregation or not
		- include_ports: only select flows that involve the ports in this list
		- exclude_ports: only select flows that do not involve the ports in this list
		- inlude_ips: only select flows that involve the ips in this list
		- exclude_ips: only select flows that do not involve the ips in this list
		- batch_size: database should select the flows in batch sizes of batchSize (ignored for most backends)
		"""
		return self.backendObject.index_query(self.collectionName, query_params)
 

	def find_one(self, spec, fields=None, sort=None):
		return self.backendObject.find_one(self.collectionName, spec, fields, sort)

	def flushCache(self, collectionName = None):
		return self.backendObject.flushCache(collectionName)

class Backend:
	def __init__(self, host, port, user, password, databaseName):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.databaseName = databaseName

	def connect(self):
		pass

	def getMinBucket(self, bucketSize = None):
		"""
		Gets the earliest bucket that is stored in the database for the given 
		bucket size. 
		"""
		pass

	def getMaxBucket(self, bucketSize = None):
		"""
		Gets the latest bucket that is stored in the database for the given 
		bucket size. 
		"""
		pass


	def getBucketSize(self, startTime, endTime, resolution):
		"""
		Calculates the bucket size that is closest to the requested resolution.
		The resolution is specified by the javascript client application and
		can be picked to be an arbitrary value.
		The bucket sizes are defined in config.py, and must not necessarily
		match to the requested resolution.
		"""
		pass

	def clearDatabase(self):
		"""
		Removes all data from the backend
		"""
		pass

	def getCollection(self, name):
		"""
		Creates and returns a wrapper "Collection" object which represents
		a collection/table in the database. 
		"""
		return Collection(self, name)
	
	def prepareCollections(self):
		"""
		This method is responsible for initializing the database on application 
		start. Some databases need to create tables when the database is used
		for the first time. Others require maintainance or sanity checking on 
		before the database can be used (e.g. writes). 
		All such initialization is done in this method. The method is only 
		called for writing processes (e.g. the preprocessor)
		"""
		pass

	def createIndex(self, collectionName, fieldName):
		"""
		Creates an index on the collection/table "collectionName" on the
		field "fieldName", if the database supports creating indexes.
		"""
		pass

	def update(self, collectionName, statement, document, insertIfNotExists):
		"""
		Adds or updates a flow in the collection "collectionName". See class
		Collection for full documentation. 
		"""
		pass

	def flushCache(self, collectionName=None):
		"""
		If the backend decides to have a separate cache, this method can be used
		to flush the cache. It will be called by the preprocessing scripts as
		soon as the script finishes.
		- collectionName: optional, if defined, only the collection with name "collectionName" 
		  		  will be flushed. If value is None, all collections are flushed and 
				  written to db.
		"""
		pass

	def bucket_query(self, collectionName, query_params):
		"""
		Queries flows from the database and collection "colletionName". See
		class Collection for full documentation of the parameters.
		"""
		pass

	def index_query(self, collectionName, query_params):
		"""
		Queries static indexes on the full database. See class Collection for 
		full documentation.
		"""
		pass

	def dynamic_index_query(self, name, query_params):
		pass 
	
	def find_one(self, collectionName, spec, fields, sort):
		pass

	def run_query(self, collectionName, query):
		pass






def getBackendObject(backend, host, port, user, password, databaseName):

	if backend == "mongo":
		from mongobackend import MongoBackend
		return MongoBackend(host, port, user, password, databaseName)
	elif backend == "mysql":
		from mysqlbackend import MysqlBackend
		return MysqlBackend(host, port, user, password, databaseName)
	elif backend == "oracle":
		from oraclebackend import OracleBackend
		return OracleBackend(host, port, user, password, databaseName)
	else:
		raise Exception("Backend " + backend + " is not a supported backend")
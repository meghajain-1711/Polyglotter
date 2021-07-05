from abc import ABC, abstractmethod
import random
import string
import networkx as nx

import matplotlib.pyplot as plt
import pickle


from intermine.webservice import Service
from intermine.webservice import Model
import requests
import json

import numpy as np
import math

from neo4j import *
import mysql.connector

# General get DB schema abstract class 
class GetDBSchema(ABC):
    def __init__(self, name, accessData):
        self.name = name
        self.accessData = accessData

    @abstractmethod
    def getDBSchema(self):
        raise NotImplementedError("The DB schema gathering method must be implemented in a child class.")

    def getGraphFromSchemaEdgeList(self, edge_list, saveName="dbSchema.obj", save=True):
        schemaGraph = nx.DiGraph()
        schemaGraph.clear()
        for node in edge_list:
            schemaGraph.add_node(node)
            for tail in edge_list[node]['references']:
                schemaGraph.add_edge(node, tail, weight=edge_list[tail]["weight"])

        # Get rid of self-loops
        schemaGraph.remove_edges_from(nx.selfloop_edges(schemaGraph))

        dbSchema = {"schema":edge_list, "graph":schemaGraph}

        if save:
            pickle.dump(dbSchema, open(saveName, "wb"))

        return dbSchema

class HumanMineGetDBSchema(GetDBSchema):
    def __init__(self, name, accessData):
        super().__init__(name, accessData)

        # Initialize HumanMine Web Service object
        self.service = Service(json.loads(requests.get(self.accessData).text)["instance"]["url"])

    # This has to be abstract 
    def getClassWeight(self, className, reference):        
        query = self.service.new_query(className)
        query.add_view(reference + ".*")
        return math.log(query.count())

    def getDBSchema(self):
        response = json.loads(requests.get(self.accessData).text)        
        dbUrl = response["instance"]["url"]+ "/service/model?format=json"
        dbModel = json.loads(requests.get(dbUrl).text)
     
        # Loop over the response to format the DB schema
        database_schema = dict()

        # First initialize the dict
        for element in dbModel['model']['classes'].keys():
            database_schema[element] = {'references':set(),'attributes':set(),'linking_attributes':dict(),'weight':1/len(dbModel['model']['classes'].keys())}	

        for element in dbModel['model']['classes'].keys():
            database_schema[element]['weight'] = float(math.log(dbModel['model']['classes'][element]['count']+1, 10))

            # Add classes links from collections, which in the case of HumanMine can be two-way
            for reference in dbModel['model']['classes'][element]['collections']:
                database_schema[element]['references'].add(dbModel['model']['classes'][element]['collections'][reference]['referencedType'])
                # Store attributes linking two classes (for join queries)
                dataArray = dbModel['model']['classes'][element]['collections'][reference]           
                database_schema[element]['linking_attributes'][dataArray['referencedType']] = dataArray['name']            
                if 'reverseReference' in dataArray:
                    database_schema[dataArray['referencedType']]['linking_attributes'][element] = dataArray['reverseReference']

            # Add classes links from references, which in the case of HumanMine can be two-way
            for reference in dbModel['model']['classes'][element]['references']:
                dataArray = dbModel['model']['classes'][element]['references'][reference]
                database_schema[element]['references'].add(dataArray['referencedType'])
                database_schema[element]['linking_attributes'][dataArray['referencedType']] = dataArray['name']
                if 'reverseReference' in dataArray:
                    database_schema[dataArray['referencedType']]['linking_attributes'][element] = dataArray['reverseReference']

            for attribute in dbModel['model']['classes'][element]['attributes'].keys():
                database_schema[element]['attributes'].add(attribute)


        self.getGraphFromSchemaEdgeList(database_schema, "HumanMinedbSchema.obj")

        print("The schema has " + str(len(dbModel['model']['classes'].keys())) + " classes.")
        
##USE MODEL 
'''
HumanMineSchema = HumanMineGetDBSchema('HumanMine WebService', "http://registry.intermine.org/service/instances/humanmine")
HumanMineSchema.getDBSchema()
'''

# child class to get the schema of the MySql database
class MySQLGetDBSchema(GetDBSchema):
    def __init__(self, name, accessData):
        super().__init__(name, accessData)

        # Initialize MySQL service object
        self.service = mysql.connector.connect(
                host=self.accessData["host"],
                user=self.accessData["user"],
                passwd=self.accessData["passwd"],
                database=self.accessData["database"],
                port=self.accessData["port"]
            )

    # This has to be abstract 
    def getClassWeight(self, className, reference): 
        cursor = self.service.cursor()
        cursor.execute("SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE table_name = '" + className + "'")
        classWeight = cursor.fetchone()
        return math.log(classWeight[0])

    def getDBSchema(self):       
        database_schema = dict()
        # Get classes
        schema = dict()

        cursor = self.service.cursor()
        cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES where table_schema = '" + self.accessData["database"] + "'")
        classes = cursor.fetchall()
        for clss in classes:
            if clss[0] not in schema:
                schema[clss[0]] = dict()

        # Table relationships
        cursor = self.service.cursor()
        cursor.execute("SELECT constraint_name, table_name, referenced_table_name FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS where UNIQUE_CONSTRAINT_SCHEMA = '" + self.accessData["database"] + "'")
        relationships = cursor.fetchall()
        for rltn in relationships:
            if rltn[2] not in schema[rltn[1]]:
                schema[rltn[1]][rltn[2]] = set()
            if rltn[0] not in schema[rltn[1]][rltn[2]]:
                schema[rltn[1]][rltn[2]].add(rltn[0])
        
        # Use the common format for this framework
        database_schema = dict()

        for element in schema.keys():
            database_schema[element] = {'references':list(),'attributes':list(),'weight':1/len(schema.keys())}
    
            database_schema[element]['weight'] = float(math.log(self.getClassWeight(element, "")+1, 10))

            for reference in schema[element]:
                database_schema[element]['references'].append(reference)

            # Get the properties (attributes) of the node
            nodeProperties = set()
            cursor = self.service.cursor()
            cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '" + element + "'")
            attrs = cursor.fetchall()
            for attr in attrs:
                if attr[0] not in nodeProperties:
                    nodeProperties.add(attr[0])

            for attribute in nodeProperties:
                database_schema[element]['attributes'].append(attribute)

        self.getGraphFromSchemaEdgeList(database_schema, "MySQLdbSchema.obj")

        print("The schema has " + str(len(database_schema.keys())) + " classes.")   

        ##USE MODEL 
        '''
        
MySQLSchema = MySQLGetDBSchema('MySQL Example', {"host":"localhost", "user": "root", "passwd": "test", "database": "testdb", "port": 3308})
MySQLSchema.getDBSchema()
        '''




#child class to get the schema of the Neo4j DB
class Neo4jGetDBSchema(GetDBSchema):
    def __init__(self, name, accessData):
        super().__init__(name, accessData)

        # Initialize HumanMine Web Service object
        self.service = GraphDatabase.driver(
            uri=self.accessData["url"],
            auth=(self.accessData["user"], self.accessData["passwd"]),
            encrypted = False, 
            max_connection_lifetime=30 * 60,
            max_connection_pool_size=150, 
            connection_acquisition_timeout=2 * 60,
            connection_timeout=3,
            max_retry_time=1)

    # This has to be abstract 
    def getClassWeight(self, className, reference):  
        with self.service.session() as session:
            classWeight = session.run("MATCH (n:" + className + ") RETURN count(distinct(n))").single().value()      
        return math.log(classWeight)

    def getDBSchema(self):       
        database_schema = dict()
        with self.service.session() as session:
            allRelationships = session.run("MATCH (n)-[rel]-(n2) RETURN n,rel,n2")

            schema = dict()
            for result in allRelationships:
                leftNode = list(result["n"].labels)[0]
                rightNode = list(result["n2"].labels)[0]
                edge = result["rel"].type

                if leftNode not in schema:
                    schema[leftNode] = dict()

                if rightNode not in schema:
                    schema[rightNode] = dict()

                if leftNode not in schema[rightNode]:
                    schema[rightNode][leftNode] = set()

                if rightNode not in schema[leftNode]:
                    schema[leftNode][rightNode] = set()

                if edge not in schema[leftNode][rightNode]:
                    schema[leftNode][rightNode].add(edge)
        
            # Use the common format for this framework
            database_schema = dict()

            for element in schema.keys():
                database_schema[element] = {'references':list(),'attributes':list(),'weight':1/len(schema.keys())}
        
                database_schema[element]['weight'] = float(math.log(self.getClassWeight(element, "")+1, 10))

                for reference in schema[element]:
                    database_schema[element]['references'].append(reference)

                # Get the properties (attributes) of the node
                nodeProperties = set()
                for attrs in session.run("MATCH (n:" + element + ") RETURN DISTINCT keys(n) as keys"):
                    for attr in attrs:
                        for x in attr:
                            nodeProperties.add(x)

                for attribute in nodeProperties:
                    database_schema[element]['attributes'].append(attribute)

            self.getGraphFromSchemaEdgeList(database_schema, "neo4jdbSchema.obj")

            print("The schema has " + str(len(database_schema.keys())) + " classes.")  

            ##USE MODEL
            ''' 

Neo4jSchema = Neo4jGetDBSchema('Neo4j Example', {"user": "neo4j", "passwd": "test", "url": "bolt://0.0.0.0:7687"})
Neo4jSchema.getDBSchema()
'''
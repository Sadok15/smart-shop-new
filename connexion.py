from flask import g
from mysql.connector import errors

from werkzeug.local import LocalProxy
import traceback

import mysql.connector
def get_db():
    if "db" not in g:
        try:
            g.db = connexion()
        except (errors.InterfaceError, errors.DatabaseError):
            raise ConnectionError("Problème de connexion à la base de donnée")
    return g.db


def connexion():
    cnx =mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            #password="insert_password",
            database="smart_shop"
        )
    return cnx

def select_query_fetch_one(query):
    """buffered fetchone"""
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor(buffered=True)
        cursor.execute(query)
        action = cursor.fetchone()
        sequence = cursor.column_names
        row = dict(zip(sequence, action))
        cursor.close()
        return row
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except TypeError:
        # query result is None => TypeError: zip argument #2 must support iteration
        return
    except:
        print(query)
        print(traceback.format_exc())


def model_select_query_fetch_one(query, model):
    """buffered fetchone"""
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor(buffered=True)
        cursor.execute(query)
        action = cursor.fetchone()
        sequence = cursor.column_names
        row = model(**dict(zip(sequence, action)))
        cursor.close()
        return row
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except TypeError:
        # query result is None => TypeError: zip argument #2 must support iteration
        return
    except:
        print(query)
        print(traceback.format_exc())


def selectquery(query):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        actions = cursor.fetchall()
        sequence = cursor.column_names
        result = [dict(zip(sequence, action)) for action in actions]
        cursor.close()
        return result
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except TypeError:
        # query result is None => TypeError: zip argument #2 must support iteration
        return
    except Exception as e:
        print(query)
        print(traceback.format_exc())

def modelselectquery(query, model):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        actions = cursor.fetchall()
        sequence = cursor.column_names
        result = [model(**dict(zip(sequence, action))) for action in actions]
        cursor.close()
        return result
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except TypeError:
        # query result is None => TypeError: zip argument #2 must support iteration
        return
    except Exception as e:
        print(query)
        print(traceback.format_exc())


def selectqueryfetchone(query):
    """nonbuffered fetchone"""
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        _id = cursor.fetchone()
        cursor.close()
        return _id[0]
    except (IndexError, TypeError):
        return
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")


def updatequery(query):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        affected_row = cursor.rowcount
        db.commit()
        cursor.close()
        if affected_row > 0:
            return 0
        else:
            return 1
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except:
        print(traceback.format_exc())


def updatequeryrowcount(query, arg):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query, arg)
        affected_row = cursor.rowcount
        db.commit()
        cursor.close()
        if affected_row > 0:
            return 0
        else:
            return 1
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except:
        print(query)
        print(traceback.format_exc())


def getRealId(attr, table, real_id):
    query = (
        f"SELECT {attr} FROM {table} "
        f'WHERE md5({attr}) ="{real_id}" '
        f'OR  MD5({attr}) = MD5("{real_id}") '
        f"LIMIT 1"
    )
    return selectqueryfetchone(query)

def insertquery(query):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        id_add = cursor.lastrowid
        db.commit()
        cursor.close()
        return id_add
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except:
        print(query)
        print(traceback.format_exc())


def deletequery(query):
    try:
        db = LocalProxy(get_db)
        cursor = db.cursor()
        cursor.execute(query)
        affected_row = cursor.rowcount
        db.commit()
        cursor.close()
        return affected_row
    except (errors.InterfaceError, errors.OperationalError, ConnectionError):
        raise ConnectionError("Problème de connexion à la base de donnée")
    except:
        print(query)
        print(traceback.format_exc())
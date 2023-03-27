import sqlite3
import numpy as np
from src.SQLiteWrapper import SQLiteWrapper

class UserDB:
    def __init__(self, db_name):
        self.res = SQLiteWrapper(db_name)

    def add_user(self, face_encoding, name):
        face_blob = face_encoding.tobytes()
        r = self.res.insert("facialrecognition", [None, sqlite3.Binary(face_blob), name])
        # self.res.close()
    
    def Extract(self, lst, pos):
        if(pos == 1):
            return [np.frombuffer(item[pos]) for item in lst]
        else:
            return [item[pos] for item in lst]

    def get_users(self):

        r = self.res.select("facialrecognition")
        # self.res.close()
        
        known_face_encodings = self.Extract(r, 1)
        known_face_names = self.Extract(r, 2)

        return known_face_encodings, known_face_names
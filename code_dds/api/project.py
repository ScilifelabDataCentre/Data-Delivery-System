from flask import Blueprint, g, jsonify, request
from flask_restful import Resource, Api
import json


class ProjectFiles(Resource):
    def get(self, project):

        files = {}

        query = f"""SELECT * FROM Files
                WHERE id IN (SELECT fileid FROM ProjectFiles
                            WHERE projectid='{project}')"""

        try:
            cursor = g.db.cursor()
        except:     # TODO: Fix exception
            pass
        else:
            cursor.execute(query)

            for file in cursor:
                print(file, flush=True)
                files[file[1]] = {
                    'directory_path': file[2],
                    'size': file[3],
                    'format': file[4],
                    'compressed': True if file[5] == 1 else False,
                    'public_key': file[6],
                    'salt': file[7],
                    'date_uploaded': file[8]
                }

        return jsonify(files)


class DatabaseUpdate(Resource):
    def post(self):
        # 1. Check if exists
        # 2. If exists -- update, otherwise create
        print("HEELLOOOO", flush=True)
        all_ = request.form
        print(f"all: {all_}", flush=True)
        # project = request.form
        # file = request.form['file']
        # print(f"file: {file}", flush=True)
        query = f"""SELECT id FROM Files
                WHERE name_='{all_['file']}'"""
        try:
            cursor = g.db.cursor()
        except:     # TODO: Fix execption
            pass
        else:
            cursor.execute(query)

            all_files = cursor.fetchall()
            if len(all_files) == 0:
                # The file is not in the database --> create
                insert_query = \
                    f"""INSERT INTO Files (name_, directory_path, size,
                                           format_, compressed, public_key,
                                           salt, date_uploaded)
                        VALUES ('{all_["file"]}', '{all_["directory_path"]}',
                                '{all_["size"]}', 'format?',
                                '{1 if all_["ds_compressed"] else 0}', 
                                '{all_["key"]}', '{all_["salt"]}', NOW());"""
                try:
                    cursor.execute(insert_query)
                    g.db.commit()
                except Exception as e:
                    print(e, flush=True)
                else:
                    print("successful? ", flush=True)
                
            elif len(all_files) > 1:
                pass    # There are multiple files, should not be possible --> error
            else:
                pass    # The file exists in the database --> update
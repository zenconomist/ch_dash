
class SaveXlsxFilesAsCSV:
        
        def __init__(self, path, npath):
            self.path = path
            self.npath = npath
            self.f = self.list_files()
            
        def list_files(self):
            from os import walk
            f = []
            path = self.path
            for (dirpath, dirnames, filenames) in walk(path):
                f.extend(filenames)
            return f
            
        def files_to_csv(self):
            path = self.path
            npath = self.npath
            self.list_files()
            g = []
            g = self.f
            import pandas as pd
            for each in g:
                file = pd.read_excel(path + each)
                
                if ".XLSX" in each:
                    file_csv_name = (npath + each.replace(".XLSX", ".csv"))
                else:
                    file_csv_name = (npath + each.replace(".xlsx", ".csv"))
                
                file.to_csv(file_csv_name, sep=',', encoding='utf-8')

class IntoPostgres:

        def __init__(self, dbase, host, port, usern, pw):
            self.dbase = dbase
            self.host = host
            self.port = port
            self.usern = usern
            self.pw = pw
            
        def pcur(self, db, h, p, u, pw):
            db = self.dbase
            h = self.host
            p = self.port
            u = self.usern
            pw = self.pw
            import psycopg2 as psy
            self.conn = psy.connect(database=db, host=h, port=p, user=u, password=pw)
            self.cur = self.conn.cursor()
            return self.cur

        def pX(self, sql_input): #postgres execute
            self.cur.execute(sql_input)

        def file_list(self,path):
            from os import walk
            self.f = []
            for (dirpath, dirnames, filenames) in walk(path):
                f.extend(filenames)
                break
            return self.f

        def in_pg(self, path, table):
            from os import walk
            f = []
            for (dirpath, dirnames, filenames) in walk(path):
               f.extend(filenames)
               break

            for each in f:
                g = open(path + each, 'r', encoding="utf8")
                self.cur.copy_expert("COPY " + table + " FROM STDIN WITH CSV HEADER", g)
                self.pX("COMMIT;")
        

        def excel_to_pg(self, path, npath, table, columns=[]):
            import pandas as pd
            from os import walk
            
            f = []
            for (dirpath, dirnames, filenames) in walk(path):
                f.extend(filenames)
                break
            l = columns.index(columns[-1])

            for each in f:
                g = pd.read_excel(path + each)
                h = g[columns]
                i = h.assign(filename=each)
                if ".XLSX" in each:
                    nfile = (each.replace(".XLSX", ".csv"))
                else:
                    nfile = (each.replace(".xlsx", ".csv"))
                i.to_csv(npath + nfile, sep=",", encoding='utf8')
                j = open(npath + nfile, 'r', encoding='utf8')
                self.cur.copy_expert("COPY " + table + " FROM STDIN WITH CSV HEADER ", j)
                
        def excel_to_pg2(self, path, npath, table, columns=[]):
            import pandas as pd
            from os import walk
            from pathlib import Path
            f = []
            for (dirpath, dirnames, filenames) in walk(path):
                f.extend(filenames)
                break
            l = columns.index(columns[-1])

            for each in f:
                g = pd.read_excel(path / each)
                h = g[columns]
                i = h.assign(filename=each)
                if ".XLSX" in each:
                    nfile = (each.replace(".XLSX", ".csv"))
                else:
                    nfile = (each.replace(".xlsx", ".csv"))
                i.to_csv(npath / nfile, sep=",")#, encoding='utf8')
                j = open(npath / nfile, 'r', encoding='utf8')
                self.cur.copy_expert("COPY " + table + " FROM STDIN WITH CSV HEADER ", j)
                

               






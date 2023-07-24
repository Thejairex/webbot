class Utils:
    def __init__(self) -> None:
        pass
    
    def filterSqlFile(self, url, last_orden: tuple, last_executed: tuple):
        def filter(lineas, table, index):
            last = [last_orden, last_executed]
            add = False
            list = []
            
            if not last_orden:
                add = True
            if not last_executed:
                add = True
                
            for linea in lineas:
                if f'INSERT INTO "{table}"' in linea:
                    orden = linea.replace(';','')
                    orden = orden.split(" ")[-1]
                    if eval(orden.split(" ")[-1])  == last[index]:
                        add = True
                        continue
                    if add:
                        list.append(linea.replace(';',''))
            return list
        
        
    
        with open("static/"+url, 'r') as file:
            lineas = file.read()
            lineas = lineas.split("\n")
            
            self.ordenes = filter(lineas, "Ordenes", 0)
            self.executados = filter(lineas, "Executedos", 1)
        return self.ordenes ,self.executados
                    
class Security:
    def __init__(self) -> None:
        self.IMAGES_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        self.SQLS_ALLOWED_EXTENSIONS = set(['sql'])

    def verify_extensions_images(self, file):
        file = file.split(".")
        
        if file[1] in self.IMAGES_ALLOWED_EXTENSIONS:
            return True
        return False
    
    def verify_extensions_sqls(self, file):
        file = file.split(".")
        
        if file[1] in self.SQLS_ALLOWED_EXTENSIONS:
            return True
        return False
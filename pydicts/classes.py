from pydicts.lod import lod_has_key, lod_print, lod_print_first, lod_sum, lod2list, lod_average_ponderated
## El objetivo es crear un objeto list_dict que se almacenera en self.ld con funciones set
## set_from_db #Todo se carga desde base de datos con el minimo parametro posible
## set_from_db_and_variables #Preguntara a base datos aquellas variables que falten. Aunque no estén en los parámetros p.e. money_convert
## set_from_variables #Solo con variables
## set #El lod ya está hecho pero se necesita el objeto para operar con el
##class Do:
##    def __init__(self,d):
##        self.d=d
##        self.create_attributes()
##
##    def number_keys(self):
##        return len(self.d)
##
##    def has_key(self,key):
##        return key in self.d
##
##    def print(self):
##        lod_print(self.d)
##
##    ## Creates an attibute from a key
##    def create_attributes(self):
##        for key, value in self.d.items():
##            setattr(self, key, value)




## Class that return a object to manage lod
## El objetivo es crear un objeto list_dict que se almacenera en self.ld con funciones set
## set_from_db #Todo se carga desde base de datos con el minimo parametro posible
## set_from_db_and_variables #Preguntara a base datos aquellas variables que falten. Aunque no estén en los parámetros p.e. money_convert
## set_from_variables #Solo con variables
## set #El lod ya está hecho pero se necesita el objeto para operar con el
class LOD:
    def __init__(self, name=None):
        self.name=self.__class__.__name__ if name is None else name
        self.ld=[]

    def length(self):
        return len(self.ld)

    def has_key(self,key):
        return lod_has_key(self.ld,key)

    def print(self):
        lod_print(self.ld)

    def print_first(self):
        lod_print_first(self.ld)

    def sum(self, key, ignore_nones=True):
        return lod_sum(self.ld, key, ignore_nones)

    def list(self, key, sorted=True):
        return lod2list(self.ld, key, sorted)

    def average_ponderated(self, key_numbers, key_values):
        return lod_average_ponderated(self.ld, key_numbers, key_values)

    def set(self, ld):
        del self.ld
        self.ld=ld
        return self

    def is_set(self):
        if hasattr(self, "ld"):
            return True
        print(f"You must set your lod in {self.name}")
        return False

    def append(self,o):
        self.ld.append(o)

    def first(self):
        return self.ld[0] if self.length()>0 else None

    ## Return list keys of the first element[21~
    def first_keys(self):
        if self.length()>0:
            return self.first().keys()
        else:
            return "I can't show keys"
    
    def order_by(self, key, reverse=False):
        self.ld=sorted(self.ld,  key=lambda item: item[key], reverse=reverse)

from datetime import datetime, date
from decimal import Decimal
from pydicts import lod
from pytest import raises, fixture


if __name__ == "__main__":
    def print_lor(lor):
        print("")
        for row in lor:
            print(row)

    lor=[]
    column_to_add=[]
    for i in range(10):
        lor.append([1*i,2*i,3*i])
        column_to_add.append(-i)
    print_lor(lor)

    lor=lor_add_column(lor, 0, column_to_add)
    lor=lor_add_column(lor, 2, column_to_add)
    lor=lor_add_column(lor, 5, column_to_add)
    print_lor(lor)

    a=lor_remove_columns(lor,[2,3])
    print_lor(a)
    b=lor_remove_rows(a,[8,9])
    print_lor(b)

    c=lor_transposed(b)
    print_lor(c)

    d=Decimal("12.3")
    json_d=var2json(d)
    print (d, json_d, json_d.__class__)
    d=None
    json_d=var2json(d)
    print (d, json_d, json_d.__class__)
    d=True
    json_d=var2json(d)
    print (d, json_d, json_d.__class__)

from gettext import translation
from importlib.resources import files

try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str


def lod_xyv_transformation(ld, key_x, key_y, key_value, order=None):
    """
    Transforms a list of dictionaries (LoD) from a "long" format (x, y, value)
    into a "wide" format (x as rows, y as columns, and value at the intersection).

    Args:
        ld (list): The input list of dictionaries. Each dictionary should have
                   keys for x-axis, y-axis, and a value.
        key_x (str): The key in the input dictionaries that represents the x-axis (rows).
        key_y (str): The key in the input dictionaries that represents the y-axis (columns).
        key_value (str): The key in the input dictionaries that holds the value.
        order (list, optional): A list specifying the desired order of columns (y-axis keys).
                                If None, columns will appear in the order they are encountered.

    Returns:
        list: A new list of dictionaries, where each dictionary represents a row (x-axis item),
              and contains keys for each y-axis item with their corresponding values.
              Returns an empty list if input `ld` is empty, or None if specified keys are not found.
    """
    if len(ld)==0:
       return []

    if not key_x in ld[0] or not key_y in ld[0] or not key_value in ld[0]:
        print(_("Keys names are not correct in dictionary in lod_year_month_value_transposition function"))
        return None

    # Searches for all different keys for columns (y-axis) and rows (x-axis)
    columns=set()
    rows=set()
    for d in ld:
        columns.add(d[key_y])
        rows.add(d[key_x])
    columns=list(columns)
    rows=list(rows)
    
    # Initialize result with a dictionary of dictionaries (dd) for easier value assignment
    dd={}
    for row in rows:
        d={"title": row}
        for column in columns:
            d[column]=0
        dd[row]=d

    # Assign values from the input data to the corresponding cells in dd
    for d in ld:
        dd[d[key_x]][d[key_y]]=d[key_value]
    
    # Convert the dictionary of dictionaries (dd) back to a list of dictionaries (LoD)
    r=[]
    for k, v in dd.items():
        r.append(v)
    
    return r

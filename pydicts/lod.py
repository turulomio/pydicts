import shutil
from collections import OrderedDict
from tabulate import tabulate
from gettext import translation
from importlib.resources import files
        
try:
    t=translation('pydicts', files("pydicts") / 'locale')
    _=t.gettext
except:
    _=str

def _fit_maxcolwidths(data, headers, align, tablefmt, maxcolwidths=None, maxheadercolwidths=None):
    """
    Calculates maxcolwidths and maxheadercolwidths automatically according to the terminal width
    so that table lines fit nicely into the console (e.g. Konsole) without wrapping awkwardly.
    """
    if maxcolwidths is not None:
        return maxcolwidths, maxheadercolwidths

    term_width = shutil.get_terminal_size(fallback=(80, 24)).columns

    kwargs = {'tablefmt': tablefmt}
    if headers is not None:
        kwargs['headers'] = headers
    if align is not None:
        kwargs['colalign'] = align

    full_table = tabulate(data, **kwargs)
    first_line = full_table.split("\n", 1)[0]
    full_width = len(first_line)
    if full_width <= term_width:
        return None, None

    if isinstance(headers, (list, tuple)):
        header_names = [str(h) for h in headers]
    elif headers == 'keys' and len(data) > 0 and isinstance(data[0], dict):
        header_names = [str(k) for k in data[0].keys()]
    else:
        header_names = [str(i) for i in range(len(data[0]))] if len(data) > 0 else []

    num_cols = len(header_names)
    if num_cols == 0:
        return None, None

    min_header_lens = [len(h) if headers is not None else 3 for h in header_names]
    natural_widths = list(min_header_lens)
    for row in data:
        if isinstance(row, dict):
            for i, h in enumerate(header_names):
                val_len = len(str(row.get(h, '')))
                if val_len > natural_widths[i]:
                    natural_widths[i] = val_len
        elif isinstance(row, (list, tuple)):
            for i in range(min(num_cols, len(row))):
                val_len = len(str(row[i]))
                if val_len > natural_widths[i]:
                    natural_widths[i] = val_len

    current_widths = list(natural_widths)
    computed_maxheadercolwidths = None

    for _ in range(300):
        kw = dict(kwargs)
        kw['maxcolwidths'] = current_widths
        if computed_maxheadercolwidths is not None:
            kw['maxheadercolwidths'] = computed_maxheadercolwidths
        t = tabulate(data, **kw)
        cur_w = len(t.split("\n", 1)[0])
        if cur_w <= term_width:
            break
        excess = cur_w - term_width

        excesses = [current_widths[i] - min_header_lens[i] for i in range(num_cols)]
        max_ex = max(excesses)
        if max_ex <= 0:
            step = max(1, excess // num_cols)
            current_widths = [max(3, w - step) for w in current_widths]
            computed_maxheadercolwidths = list(current_widths)
            continue

        other_excesses = [ex for ex in excesses if ex < max_ex]
        second_ex = max(other_excesses) if other_excesses else 0
        candidates = [i for i, ex in enumerate(excesses) if ex == max_ex]

        step_to_second = max_ex - second_ex
        step_needed = (excess + len(candidates) - 1) // len(candidates)
        step = max(1, min(step_needed, step_to_second if step_to_second > 0 else step_needed))

        for c in candidates:
            current_widths[c] = max(min_header_lens[c], current_widths[c] - step)

    # After shrinking, expand any column whose content was restricted so it fills
    # up to the full terminal width without exceeding it.
    for _ in range(50):
        kw = dict(kwargs)
        kw['maxcolwidths'] = current_widths
        if computed_maxheadercolwidths is not None:
            kw['maxheadercolwidths'] = computed_maxheadercolwidths
        t = tabulate(data, **kw)
        cur_w = len(t.split("\n", 1)[0])
        deficit = term_width - cur_w
        if deficit <= 0:
            break
        expandable = [i for i in range(num_cols) if current_widths[i] < natural_widths[i]]
        if not expandable:
            break
        added = False
        for idx in expandable:
            current_widths[idx] += 1
            kw['maxcolwidths'] = current_widths
            t = tabulate(data, **kw)
            cur_w = len(t.split("\n", 1)[0])
            if cur_w > term_width:
                current_widths[idx] -= 1
            else:
                added = True
        if not added:
            break

    return current_widths, computed_maxheadercolwidths

def _stretch_table_to_terminal(table_str, target_width=None):
    """
    Expands table horizontal lines and columns proportionally to fill the full width
    of the terminal (e.g. Konsole in full screen or wide windows), preventing the table
    from falling short of the right side of the screen.
    """
    if target_width is None:
        target_width = shutil.get_terminal_size(fallback=(80, 24)).columns

    lines = table_str.splitlines()
    if not lines or len(lines[0]) >= target_width:
        return table_str

    diff = target_width - len(lines[0])

    # Find column boundary indices (supports grid, simple_grid, fancy_grid, etc.)
    boundaries = None
    for line in lines:
        if not line:
            continue
        first_char = line[0]
        if first_char in ('|', '│', ':') and line[-1] == first_char:
            indices = [i for i, ch in enumerate(line) if ch == first_char]
            if len(indices) >= 2:
                boundaries = indices
                break

    if not boundaries:
        first_line = lines[0]
        fill_types = {'-', '=', '─', '═', '━'}
        indices = [i for i, c in enumerate(first_line) if c not in fill_types]
        if len(indices) >= 2:
            boundaries = indices

    if not boundaries or len(boundaries) < 2:
        return table_str

    col_widths = [boundaries[i+1] - boundaries[i] - 1 for i in range(len(boundaries)-1)]
    num_cols = len(col_widths)
    total_w = sum(col_widths)
    if total_w == 0:
        return table_str

    extra = [int(diff * (w / total_w)) for w in col_widths]
    remainder = diff - sum(extra)
    for _ in range(remainder):
        largest_idx = max(range(num_cols), key=lambda i: (col_widths[i] + extra[i]))
        extra[largest_idx] += 1

    first_len = len(lines[0])
    new_lines = []
    for line in lines:
        if not line or len(line) != first_len:
            new_lines.append(line)
            continue
        new_parts = []
        for col_idx in range(num_cols):
            start = boundaries[col_idx]
            end = boundaries[col_idx+1]
            segment = line[start:end]
            border_char = segment[0]
            content = segment[1:]
            fill_char = content[-1] if content else ' '
            new_segment = border_char + content + (fill_char * extra[col_idx])
            new_parts.append(new_segment)
        new_parts.append(line[-1])
        new_lines.append(''.join(new_parts))
    return '\n'.join(new_lines)
def lod_aggregate_sum(lod_, key_to_sum):
    """
    Agrupa un List of Dictionaries (LOD) por todas las claves excepto una,
    sumando los valores de esa clave para los registros duplicados.

    Esta función es útil cuando se tienen datos desglosados que necesitan ser 
    consolidados sumando una métrica (como un contador o importe) mientras 
    se mantienen el resto de dimensiones.

    Args:
        lod_ (list[dict]): Lista de diccionarios a procesar.
        key_to_sum (str): El nombre de la clave cuyo valor se desea sumar.

    Returns:
        list[dict]: Una nueva lista de diccionarios donde no existen duplicados 
                    para la combinación de todas las claves excepto 'key_to_sum'.

    Ejemplo:
        >>> lod = [{'id': 1, 'v': 10}, {'id': 1, 'v': 5}, {'id': 2, 'v': 20}]
        >>> lod_aggregate_sum(lod, 'v')
        [{'id': 1, 'v': 15}, {'id': 2, 'v': 20}]
    """
    if not lod_:
        return []

    r = {}
    for d in lod_:
        # Creamos una clave basada en todos los campos excepto el que vamos a sumar
        group_keys = {k: v for k, v in d.items() if k != key_to_sum}
        k_tuple = tuple(sorted(group_keys.items(), key=lambda x: x[0]))
        
        if k_tuple in r:
            r[k_tuple][key_to_sum] += d.get(key_to_sum, 0)
        else:
            r[k_tuple] = d.copy()
            if key_to_sum not in r[k_tuple]:
                r[k_tuple][key_to_sum] = 0

    return list(r.values())

def lod_has_key(lod_, key):
    """
    Checks if a given key exists in the first dictionary of a list of dictionaries.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key to check for.

    Returns:
        bool: True if the key exists in the first dictionary, False otherwise or if the list is empty.
    """
    if len(lod_)==0:
        return False
    return key in lod_[0]

def lod_order_by(ld, key, reverse=False, none_at_top=True):
    """
    Orders a list of dictionaries by the value of a specified key.

    Args:
        ld (list): The list of dictionaries to sort.
        key (str): The key to sort by.
        reverse (bool, optional): If True, sort in descending order. Defaults to False.
        none_at_top (bool, optional): If True, None values are placed at the beginning of the list.
                                      If False, None values are placed at the end. Defaults to True.

    Returns:
        list: The sorted list of dictionaries.
    """
    nonull=[]
    null=[]
    for o in ld:
        com=o[key]
        if com is None:
            null.append(o)
        else:
            nonull.append(o)
    nonull=sorted(nonull, key=lambda item: item[key], reverse=reverse)
    if none_at_top==True:#Set None at top of the list
        return null+nonull
    else:
        return nonull+null

def lod_string(lod_, number=None, align=None, maxcolwidths=None, tablefmt="simple_grid", wordwrap=True, stretch=False):
    """
    Returns a string representation of a list of dictionaries with tabulate module.
    Optionally adapts column widths to the current console size (wordwrap)
    and stretches the table horizontally to fill the full terminal width (stretch).

        - lod_: List of dictionaries
        - number: Number of dictionaries in the list to print. If None uses all lod_. (defaults to None)
        - align: Cells alignment with tabulate syntax. (defaults to None). Possible column alignments are: 
                 right, center, left, decimal (only for numbers), and None (to disable alignment). Omitting an 
                 alignment uses the default.
        - maxcolwidths: Maximum column widths (int, list, or None).
        - tablefmt: Tabulate table format (defaults to "simple_grid").
        - wordwrap (bool): If True and maxcolwidths is None, calculates maxcolwidths automatically to prevent
                           lines from breaking across the console. Defaults to True.
        - stretch (bool): If True and maxcolwidths is None, expands table columns and horizontal lines
                          to fill the full terminal width. Defaults to False.

    Returns:
        str: Formatted table string or informative message if empty/zero rows.
    """
    number=len(lod_) if number is None else number
    if len(lod_)==0:
        return _("This list of dictionaries hasn't data to print")
    if number == 0:
        return _("No data was printed due to you selected 0 rows")

    data_slice = lod_[0:number]
    if wordwrap and maxcolwidths is None:
        cw, hw = _fit_maxcolwidths(data_slice, headers="keys", align=align, tablefmt=tablefmt, maxcolwidths=None)
    else:
        cw, hw = maxcolwidths, None

    kwargs = {"headers": "keys", "tablefmt": tablefmt, "colalign": align}
    if cw is not None:
        kwargs["maxcolwidths"] = cw
    if hw is not None:
        kwargs["maxheadercolwidths"] = hw

    rendered = tabulate(data_slice, **kwargs)
    if stretch and maxcolwidths is None:
        rendered = _stretch_table_to_terminal(rendered)
    return rendered

def lod_print(lod_, number=None, align=None, maxcolwidths=None, tablefmt="simple_grid", wordwrap=True, stretch=False):
    """
    Prints a list of dictionaries with tabulate module.
    Uses `lod_string` internally.

        - lod_: List of dictionaries
        - number: Number of dictionaries in the list to print. If None prints all lod_. (defaults to None)
        - align: Cells alignment with tabulate syntax. (defaults to None). Possible column alignments are: 
                 right, center, left, decimal (only for numbers), and None (to disable alignment). Omitting an 
                 alignment uses the default.
        - maxcolwidths: Maximum column widths (int, list, or None).
        - tablefmt: Tabulate table format (defaults to "simple_grid").
        - wordwrap (bool): If True and maxcolwidths is None, calculates maxcolwidths automatically. Defaults to True.
        - stretch (bool): If True and maxcolwidths is None, expands table columns to fill terminal width. Defaults to False.
    """
    print(lod_string(lod_, number=number, align=align, maxcolwidths=maxcolwidths, tablefmt=tablefmt, wordwrap=wordwrap, stretch=stretch))

def lod_sum(lod_, key, ignore_nones=True):
    """
    Calculates the sum of values for a specified key across all dictionaries in a list.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be summed.
        ignore_nones (bool, optional): If True, None values are skipped. If False, a TypeError will be raised if None is encountered. Defaults to True.

    Returns:
        (int, float, Decimal): The sum of the values.
    """
    r=0
    for d in lod_:
        if ignore_nones is True and d[key] is None:
            continue
        r=r+d[key]
    return r

def lod_sum_negatives(lod_, key):
    """
    Calculates the sum of negative values for a specified key across all dictionaries in a list.
    None and positive values are ignored.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be summed.
    Returns:
        (int, float, Decimal): The sum of the negative values."""
    r=0
    for d in lod_:
        if d[key] is None or d[key]>0:
            continue
        r=r+d[key]
    return r

def lod_sum_positives(lod_, key):
    """
    Calculates the sum of positive values for a specified key across all dictionaries in a list.
    None and negative values are ignored.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be summed.
    Returns:
        (int, float, Decimal): The sum of the positive values."""
    r=0
    for d in lod_:
        if d[key] is None or d[key]<0:
            continue
        r=r+d[key]
    return r

def lod_average(lod_, key):
    """
    Calculates the average of values for a specified key across all dictionaries in a list.
    This function uses `lod_sum` and divides by the total number of dictionaries.
    
    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be averaged.

    Returns:
        (int, float, Decimal): The average of the values.
    """
    return lod_sum(lod_,key)/len(lod_)

def lod_average_ponderated(lod_, key_numbers, key_values):
    """
    Calculates the weighted average of values for a specified key, using another key for weights.

    Args:
        lod_ (list): The list of dictionaries.
        key_numbers (str): The key representing the weights (numbers).
        key_values (str): The key representing the values to be averaged.
    """
    prods=0
    for d in lod_:
        prods=prods+d[key_numbers]*d[key_values]
    return prods/lod_sum(lod_, key_numbers)

def lod_count(lod_, lambdafunction):
    """
    Counts dictionaries in a list that satisfy a given lambda function condition.

    Args:
        lod_ (list): The list of dictionaries.
        lambdafunction (function): A lambda function that takes two arguments (d, index),
                                   where `d` is the dictionary and `index` is its position.
                                   It should return True for dictionaries to be counted.

    Returns:
        int: The number of dictionaries that satisfy the condition.
    """
    r=0   
    for index,  d in enumerate(lod_):
        if lambdafunction(d,index) is True:
            r+=1
    return r

def lod_median(lod_, key):
    from statistics import median
    """
    Calculates the median of values for a specified key across all dictionaries in a list.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be used for median calculation.

    Returns:
        (int, float, Decimal): The median of the values.
    """
    return median(lod2list(lod_, key, sorted=True))

def lod2dictkv(lod_, key, value):
    """
    Converts a list of dictionaries into a single dictionary where a specified key
    from each dictionary becomes the new dictionary's key, and another specified
    key's value becomes the new dictionary's value.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key in the original dictionaries to use as the new dictionary's key.
        value (str): The key in the original dictionaries whose value will be the new dictionary's value.

    Returns:
        dict: A dictionary with key-value pairs extracted from the input list.
    """
    d={}
    for ld in lod_:
        d[ld[key]]=ld[value]
    return d

def lod2dod(lod_, key):
    """
    Converts a list of dictionaries into a dictionary of dictionaries (DoD),
    where a specified key from each dictionary becomes the key in the new DoD,
    and the entire original dictionary becomes the value.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key in the original dictionaries to use as the new DoD's key.

    Returns:
        dict: A dictionary of dictionaries.
    """
    d={}
    for ld in lod_:
        d[ld[key]]=ld
    return d
    
def lod2odod(lod_, key):
    """
    Converts a list of dictionaries into an OrderedDict of dictionaries (ODoD),
    preserving insertion order.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key in the original dictionaries to use as the new ODoD's key.

    Returns:
        OrderedDict: An ordered dictionary of dictionaries.
    """
    d=OrderedDict()
    for ld in lod_:
        d[ld[key]]=ld
    return d
    
def lod2dod_tuple(lod_, key1, key2):
    """
    Converts a list of dictionaries into a dictionary of dictionaries (DoD),
    using a tuple of two specified keys from each dictionary as the new DoD's key.

    Args:
        lod_ (list): The list of dictionaries.
        key1 (str): The first key in the original dictionaries to use for the tuple key.
        key2 (str): The second key in the original dictionaries to use for the tuple key.

    Returns:
        dict: A dictionary of dictionaries with tuple keys.
    """
    d={}
    for ld in lod_:
        d[(ld[key1],ld[key2])]=ld
    return d

def dod2lod(d):
    """
    Converts a dictionary of dictionaries (DoD) back into a list of dictionaries.

    Args:
        d (dict): The dictionary of dictionaries.

    Returns:
        list: A list of dictionaries.
    """
    r=[]
    for k,v in d.items():
        r.append(v)
    return r

def lod2list(lod_, key, sorted=False, cast=None):
    """
    Extracts all values for a specified key from a list of dictionaries into a new list.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose values are to be extracted.
        sorted (bool, optional): If True, the resulting list will be sorted. Defaults to False.
        cast (str, optional): If specified ("str", "float"), attempts to cast the extracted values.
                              Defaults to None.

    Returns:
        list: A list containing the extracted values.
    """
    r=[]
    for ld in lod_:
        if cast is None:
            r.append(ld[key])
        elif cast == "str":
            r.append(str(ld[key]))
        elif cast == "float":
            r.append(float(ld[key]))
    if sorted is True:
        r.sort()
    return r

def lod2list_distinct(lod_, key, sorted=False, cast=None):
    """
    Extracts distinct values for a specified key from a list of dictionaries into a new list.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose distinct values are to be extracted.
        sorted (bool, optional): If True, the resulting list will be sorted. Defaults to False.
        cast (str, optional): If specified ("str", "float"), attempts to cast the extracted values.
                              Defaults to None.

    Returns:
        list: A list containing the distinct extracted values.
    """
    set_=set()
    for ld in lod_:
        if cast is None:
            set_.add(ld[key])
        elif cast == "str":
            set_.add(str(ld[key]))
        elif cast == "float":
            set_.add(float(ld[key]))
    r=list(set_)
    if sorted is True:
        r.sort()
    return r

def lod2lol(lod_,  keys=None):
    """
    Converts a list of dictionaries into a list of lists (List of Lists - LoL),
    extracting values for specified keys.

    Args:
        lod_ (list): The list of dictionaries.
        keys (list, optional): A list of keys to extract values for. If None,
                               it uses the keys from the first dictionary.

    Returns:
        list: A list of lists, where each inner list represents a row of values.
    """
    if len(lod_)==0:
        return []
        
    if keys is None:
        keys=lod_[0].keys()
        
    r=[]  
    for od in lod_:
        row_r=[]
        for key in keys:
            row_r.append(od[key])
        r.append(row_r)
    return r

def lod2lood(ld, keys):
    """
    Converts a list of dictionaries into a list of OrderedDicts (List of OrderedDicts - LoOD),
    containing only the specified keys.

    Args:
        ld (list): The list of dictionaries.
        keys (list): A list of keys to include in each OrderedDict.

    Returns:
        list: A list of OrderedDicts.
    """
    if len(ld)==0:
        return []
                
    r=[]  
    for d in ld:
        r_d=OrderedDict()
        for key in keys:
            r_d[key]=d[key]
        r.append(r_d)
    return r


def lod_max_value(ld, key):
    """
    Returns the maximum value for a specified key across all dictionaries in a list.
    None values are ignored.

    Args:
        ld (list): The list of dictionaries.
        key (str): The key whose maximum value is to be found.

    Returns:
        (int, float, Decimal) or None: The maximum value, or None if the list is empty or all values for the key are None.
    """
    non_none_values = [d[key] for d in ld if d[key] is not None]
    if not non_none_values:
        return None
    return max(non_none_values)

def lod_min_value(ld, key):
    """
    Returns the minimum value for a specified key across all dictionaries in a list.
    None values are ignored.

    Args:
        ld (list): The list of dictionaries.
        key (str): The key whose minimum value is to be found.

    Returns:
        (int, float, Decimal) or None: The minimum value, or None if the list is empty or all values for the key are None.
    """
    non_none_values = [d[key] for d in ld if d[key] is not None]
    if not non_none_values:
        return None
    return min(non_none_values)

def lod2list_distinct(lod_, key, sorted=False, cast=None):
    """
    Extracts distinct values for a specified key from a list of dictionaries into a new list.

    Args:
        lod_ (list): The list of dictionaries.
        key (str): The key whose distinct values are to be extracted.
        sorted (bool, optional): If True, the resulting list will be sorted. Defaults to False.
        cast (str, optional): If specified ("str", "float"), attempts to cast the extracted values.
                              Defaults to None.

    Returns:
        list: A list containing the distinct extracted values, with None values sorted first if `sorted` is True.
    """
    set_ = set()
    for ld in lod_:
        val = ld[key]
        if cast is None:
            set_.add(val)
        elif cast == "str":
            set_.add(str(val))
        elif cast == "float":
            set_.add(float(val))
    r = list(set_)
    if sorted is True:
        # Custom sort key to handle None values: None comes first (False < True)
        r.sort(key=lambda x: (x is not None, x))
    return r

def lod_remove_duplicates(lod_):
    """
    Removes duplicate dictionaries from a list. A dictionary is considered a duplicate
    if it has the same key-value pairs as another. The order of keys does not matter.

    Args:
        lod_ (list): The list of dictionaries to process.

    Returns:
        list: A new list containing only unique dictionaries.
    """
    seen = set()
    unique_dicts = []
    for d in lod_:
        # Convert dictionary to a tuple of its items for hashability
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            unique_dicts.append(d)
    return unique_dicts

def lod_rename_key(ld, from_, to_):
    """
    Renames a specified key in all dictionaries within a list.

    Args:
        ld (list): The list of dictionaries to modify.
        from_ (str): The current name of the key to be renamed.
        to_ (str): The new name for the key.

    Returns:
        list: The modified list of dictionaries.
    """
    for d in ld:
        d[to_]=d.pop(from_)
    return ld

def lod_remove_key(lod_, key):
    """
    Removes a specified key from all dictionaries within a list.

    Args:
        lod_ (list): The list of dictionaries to modify.
        key (str): The key to be removed.

    Returns:
        list: The modified list of dictionaries.
    """
    for d in lod_:
        del d[key]
    return lod_
    
def lod_keys(lod_):
    """
    Returns a list of keys from the first dictionary in a list of dictionaries.

    Args:
        lod_ (list): The list of dictionaries.

    Returns:
        list or None: A list of keys from the first dictionary, or None if the list is empty.
    """
    if len(lod_)>0:
        return list(lod_[0].keys())
    return None
    
def lod_clone(lod_):
    new_lod=[]
    """
    Creates a deep clone of a list of dictionaries.
    Each dictionary and its direct values are copied, but nested mutable objects
    within the dictionary values are not deep copied.

    Args:
        lod_ (list): The list of dictionaries to clone.

    Returns:
        list: A new list of dictionaries, which is a deep copy of the input.
    """
    for d in lod_:
        new_d={}
        for key, value in d.items():
            new_d[key]=value
        new_lod.append(new_d)
    return new_lod

def lod_filter_keys(lod_, keys):
    """
    Creates a new list of dictionaries, where each dictionary contains only
    the specified keys from the original dictionaries.

    Args:
        lod_ (list): The original list of dictionaries.
        keys (list): A list of strings representing the keys to keep.

    Returns:
        list: A new list of dictionaries with filtered keys.
    """
    new_lod=[]
    for d in lod_:
        new_d={}
        for key in keys:
            new_d[key]=d[key]
        new_lod.append(new_d)
    return new_lod


def lod_filter_dictionaries(lod_, lambda_function):
    """
    Filters a list of dictionaries, returning a new list containing only
    those dictionaries for which the `lambda_function` returns True.

    Args:
        lod_ (list): The list of dictionaries to filter.
        lambda_function (function): A lambda function that takes two arguments (d, index),
                                   where `d` is the dictionary and `index` is its position.
                                   It should return True for dictionaries to be included.

    Returns:
        list: A new list of dictionaries that satisfy the filter condition.
    """
    new_lod=[]
    for index,  d in enumerate(lod_):
        if lambda_function(d, index) is True:
            new_lod.append(d)
    return new_lod
    
def lod_calculate(lod_, key, lambda_function, clone=False):
    """
    Adds a new key-value pair or updates an existing one in each dictionary
    of a list, based on the result of a lambda function.

    Args:
        lod_ (list): The list of dictionaries to modify.
        key (str): The key where the `lambda_function` result will be stored.
        lambda_function (function): A lambda function that takes two arguments (d, index),
                                   where `d` is the dictionary and `index` is its position.
                                   Its return value will be assigned to `d[key]`.
        clone (bool, optional): If True, a clone of the input list is created and modified,
                                leaving the original list unchanged. Defaults to False.

    Returns:
        list: The modified list of dictionaries (either the original or a clone).
    """
    if clone is True:
        l_o_d=lod_clone(lod_)
    else:
        l_o_d=lod_
        
    for index,  d in enumerate(l_o_d):
        d[key]=lambda_function(d, index)
    return l_o_d

def lod_reorder_keys(lod_, keys):
    """
    Reorders the keys of all dictionaries in a list according to a specified list of keys.
    Keys not present in the `keys` list will be appended at the end of each dictionary.

    Args:
        lod_ (list): The list of dictionaries to modify.
        keys (list): A list of strings representing the desired order of keys.

    Returns:
        list: A new list of dictionaries with reordered keys.
    """
    new_lod = []
    for d in lod_:
        new_d = {}
        for key in keys:
            if key in d:
                new_d[key] = d[key]
        for key in d:
            if key not in new_d:
                new_d[key] = d[key]
        new_lod.append(new_d)
    return new_lod

def lod_join(lod1, lod2, calc_key, operation="+"):
    """
    Joins two lists of dictionaries (lod) by all keys except the calc_key, performing an arithmetic operation on the selected calc_key.
    The list maintains the order of elements in lod1, followed by any new elements from lod2.
    If the value of `calc_key` is None or missing in any dictionary, it is treated as 0 for the calculation.

    Args:
        lod1 (list): The first list of dictionaries.
        lod2 (list): The second list of dictionaries.
        calc_key (str): The key on which to perform the calculation.
        operation (str, optional): The operation to perform ("+" or "-"). Defaults to "+".

    Returns:
        list: A new list of dictionaries with the combined results.
    """
    def get_join_tuple(d):
        return tuple((k, d[k]) for k in sorted(k for k in d.keys() if k != calc_key))

    d2 = {get_join_tuple(d): d for d in lod2}

    new_lod = []
    seen = set()

    for d in lod1:
        join_val = get_join_tuple(d)
        seen.add(join_val)
        
        new_entry = d.copy()
        val1 = new_entry.get(calc_key, 0)
        val2 = d2.get(join_val, {}).get(calc_key, 0)
        
        val1 = 0 if val1 is None else val1
        val2 = 0 if val2 is None else val2
        
        if operation in ("+", "sum"):
            new_entry[calc_key] = val1 + val2
        elif operation in ("-", "rest", "sub", "subtract"):
            new_entry[calc_key] = val1 - val2
            
        new_lod.append(new_entry)

    for d in lod2:
        join_val = get_join_tuple(d)
        if join_val not in seen:
            new_entry = d.copy()
            val1 = 0
            val2 = new_entry.get(calc_key, 0)
            val2 = 0 if val2 is None else val2
            
            if operation in ("+", "sum"):
                new_entry[calc_key] = val1 + val2
            elif operation in ("-", "rest", "sub", "subtract"):
                new_entry[calc_key] = val1 - val2
                
            new_lod.append(new_entry)

    return new_lod

---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Object-Oriented Wrappers: LOD, LOL, and DOD

`pydicts` provides high-level, object-oriented wrappers around common data structures:

- **`LOD`**: List of Dictionaries (`list[dict]`)
- **`LOL`**: List of Lists (`list[list]`)
- **`DOD`**: Dictionary of Dictionaries (`dict[Any, dict]`)

These classes implement native Python container and mapping protocols (`len()`, slicing, iteration, `in`, item access, equality) and provide intuitive methods for chaining transformations, aggregations, formatting, and seamless cross-structure conversions.

---

## LOD (List of Dictionaries)

### Initialization and Container Protocols

You can initialize an `LOD` directly with a list of dictionaries, another `LOD`, or empty.

```{code-cell}
from pydicts import LOD
from decimal import Decimal

data = [
    {"id": 1, "name": "Alice", "dept": "IT", "salary": Decimal("3000")},
    {"id": 2, "name": "Bob", "dept": "HR", "salary": Decimal("2400")},
    {"id": 3, "name": "Charlie", "dept": "IT", "salary": Decimal("3500")},
    {"id": 4, "name": "David", "dept": "Finance", "salary": Decimal("2800")},
]

lod_employees = LOD(data, name="Employees")
print(lod_employees)
print(f"Total employees: {len(lod_employees)}")
print(f"First employee: {lod_employees[0]['name']}")
```

Slicing creates a new `LOD` instance preserving its name:

```{code-cell}
subset = lod_employees[1:3]
print(repr(subset))
```

### Aggregations

Compute sums, averages, medians, and min/max values across dictionaries:

```{code-cell}
print("Total salary:", lod_employees.sum("salary"))
print("Average salary:", lod_employees.average("salary"))
print("Median salary:", lod_employees.median("salary"))
print("Max salary:", lod_employees.max_value("salary"))
print("Min salary:", lod_employees.min_value("salary"))
```

Count matching items using custom predicates (accepts `lambda d: ...` or `lambda d, idx: ...`):

```{code-cell}
it_count = lod_employees.count(lambda d: d["dept"] == "IT")
print(f"IT employees count: {it_count}")
```

Extract lists of values or distinct values:

```{code-cell}
print("Departments:", lod_employees.list("dept"))
print("Distinct departments:", lod_employees.list_distinct("dept"))
```

### Transformations and Method Chaining

Transformations update the instance in place and return `self` to support method chaining, or create new instances where appropriate:

```{code-cell}
# Sort by salary descending
lod_employees.order_by("salary", reverse=True)
lod_employees.print()
```

```{code-cell}
# Calculate a new column with bonus
lod_employees.calculate("total_compensation", lambda d: d["salary"] * Decimal("1.10"))
lod_employees.print()
```

```{code-cell}
# Filter rows matching condition
it_employees = lod_employees.filter(lambda d: d["dept"] == "IT")
it_employees.print()
```

```{code-cell}
# Keep only selected keys
projected = lod_employees.filter_keys(["name", "salary"])
projected.print()
```

### Conversions to Other Structures

Convert effortlessly to `LOL`, `DOD`, or key-value dictionaries:

```{code-cell}
# Convert to DOD indexed by employee id
dod_emp = lod_employees.to_dod("id")
print(dod_emp)
print(dod_emp[1])
```

```{code-cell}
# Convert to LOL with header keys
lol_emp = lod_employees.to_lol(keys=["id", "name", "salary"])
print(lol_emp)
```

```{code-cell}
# Convert to plain key-value dictionary
id_to_name = lod_employees.to_dictkv("id", "name")
print(id_to_name)
```

### Subclassing `LOD` for Domain-Specific Logic

One of the greatest advantages of `LOD` is the ability to subclass it to build dedicated domain models, encapsulating business rules, custom aggregations, and domain validations directly into the collection:

```{code-cell}
class Payroll(LOD):
    """Domain-specific LOD representing company payroll records."""

    def total_budget(self) -> Decimal:
        """Calculates total gross payroll."""
        return self.sum("salary")

    def department_payroll(self, dept_name: str) -> "Payroll":
        """Returns a new Payroll instance filtered by department."""
        return self.filter(lambda emp: emp["dept"] == dept_name)

    def top_earners(self, count: int = 3) -> "Payroll":
        """Returns the top earners ordered by salary."""
        cloned = self.clone()
        cloned.order_by("salary", reverse=True)
        return cloned[:count]

    def add_standard_bonus(self, bonus_rate: Decimal = Decimal("0.10")) -> "Payroll":
        """Calculates and attaches the bonus field in place."""
        return self.calculate("bonus", lambda emp: emp["salary"] * bonus_rate)


# Instantiate domain model
payroll = Payroll(data, name="EngineeringPayroll")

print(f"Total budget: {payroll.total_budget()}")

# Filter by department returning another Payroll instance
it_payroll = payroll.department_payroll("IT")
print(f"IT Budget: {it_payroll.total_budget()}")

# Method chaining and domain transformation
payroll.add_standard_bonus(Decimal("0.15"))
top_employees = payroll.top_earners(2)
top_employees.print()
```

---

## LOL (List of Lists)

### Initialization and Access

`LOL` wraps matrices and 2D tabular data, implementing sequence protocols and column/row operations:

```{code-cell}
from pydicts import LOL

matrix_data = [
    ["Region", "Q1", "Q2", "Q3", "Q4"],
    ["North", 120, 140, 110, 160],
    ["South", 90, 105, 115, 120],
    ["East", 200, 210, 190, 220],
]

table = LOL(matrix_data, name="QuarterlySales")
table.print()
```

Access rows and columns directly:

```{code-cell}
print("Row 1:", table.get_row(1))
print("Column 0 (Regions):", table.get_column(0))
```

### Row and Column Sums

Sum row or column slices easily:

```{code-cell}
# Sum North sales (columns from index 1 to end)
north_total = table.sum_row(1, from_index=1)
print(f"Total North: {north_total}")

# Sum Q1 sales across regions (rows 1 to end)
q1_total = table.sum_column(1, from_index=1)
print(f"Total Q1: {q1_total}")
```

### Transposition and Sorting

```{code-cell}
# Transpose rows and columns
transposed = table.transposed()
transposed.print()
```

```{code-cell}
# Sort rows by column 1 (Q1) descending
data_only = LOL(matrix_data[1:])
data_only.order_by(1, reverse=True)
data_only.print()
```

---

## DOD (Dictionary of Dictionaries)

### Initialization and Mapping Protocols

`DOD` wraps dictionaries of dictionaries, offering key access, mutations, pretty printing, and round-trip conversion to `LOD`:

```{code-cell}
from pydicts import DOD

users = DOD({
    "usr_01": {"name": "Alice", "role": "admin", "active": True},
    "usr_02": {"name": "Bob", "role": "engineer", "active": True},
    "usr_03": {"name": "Charlie", "role": "viewer", "active": False},
}, name="UserCatalog")

print(f"Total users: {len(users)}")
print("User 01:", users["usr_01"]["name"])
```

Add or delete users using standard dictionary syntax:

```{code-cell}
users["usr_04"] = {"name": "David", "role": "editor", "active": True}
del users["usr_03"]

users.print()
```

### Conversion from DOD to LOD

Convert back to an `LOD` object for tabular display, sorting, or aggregation:

```{code-cell}
users_lod = users.to_lod()
users_lod.print()
```

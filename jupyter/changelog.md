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
# CHANGELOG

## 1.1.0 (2025-05-24)
- Added align parameter to lod_print and lol_print methods.
- Added decimals parameter to currency_color, percentage_color, value_color methods.

## 1.0.0 (2025-04-13)
- Migrated to poetry>2.0.0

## 0.17.0 (2024-11-03)
- Added colors module to fast color string programming using colorama
- Added lod_count method to count dictionaries using a lambda function
- Updated dependecies to fix several bugs

## 0.16.0 (2024-04-13)
- Added is_email method in casts

## 0.15.0 (2024-03-24)
- Added dod_print, lol_order_by, lod_add_row methods.
- Added automatic documentation to the whole project.

## 0.14.0 (2024-03-21)
- Add method lod_remove_duplicates
- Python>=3.9 is now required
- Github project pages is now updated with Github Actions

## 0.13.0 (2024-01-26)
- Removed ccy dependency due to slow python release updates

## 0.12.0 (2024-01-16)
- Improved percentage logic
- Integrated ccy module for currencies listing
- Added more test. Coverage is now 86%
- Added support to ISO 8601 durations casts. Added support to durations in MyJsonEncoder module
- Added jupyter-book support for documentation
- Added project logo
- Fixed jinja2 dependency security warnning

## 0.11.0 (2023-12-13)
- Added in casts ignore_exceptions parameter in all methods
- Added a lot of tests. Test coverage is now 73%.
- Added more stability to casts

### 0.10.0 (2023-12-08)
- Improving str2decimal conversions. Changed type parameter to decimal_separator.
- Added Percentage and Currency classes to manage this objects

## 0.9.0 (2023-12-04)
- Added gettext support
- Improved spanish translation
- Added custom exceptions for each module
- Improved documentation
- Added lol_print method
- myjsonencoder has been included to convert from json to dictionaries

## 0.8.0 (2023-11-26)
- Migrating casts and datetime_functions to pydicts.casts. Utils to make casting easy
- Create lol (List of lists) module

## 0.7.0 (2023-11-04)
- Improved documentation
- Removed duplicated lod_min and lod_max methods
- Added lod_filter_keys function
- Added lod_filter_dictionaries function
- Added lod_clone function
- Added lod_calculate function

## 0.6.0 (2023-07-02)
- Fixed a race condition bug in lod_ymv_transposition_with_percentages

## 0.5.0 (2023-05-04)
- Added support to latex tables from list of dictionaries

## 0.4.0 (2023-04-19)
- Added poetry support
- Added poethepoet support
- Added lod_remove_key

## 0.3.0 (2023-04-16)
- Added lod_ymv_transposition_with_porcentages

## 0.2.0 (2023-04-12)
- Added lod_print with tabulate module
- Improving documentation
- Refactorized modules to lod_xyv, lod_ymmv

### 0.1.0 (2023-04-10)
- First version addapting listdict_functions from reusingcode

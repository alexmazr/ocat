# Syntax of OCat

## Declaration, Assignment, and Expressions
OCat currently supports these types of variables: `int`, `uint`, `float`, and `bool`. All variables in OCat are immutable by default, once set, they never change. If a variable must be mutated, it
must be explicitly declared by tagging with `mut`:
```
int x = 2
mut float pi = 3.14
```
OCat can perform the following arithmetic operations: +, -, *, and /

Other supported operations include: `and`, `or`, `not`, `xor`, ~, ==, !=, >, <, <=, >=, **, %, &, |, ^, <<, >>







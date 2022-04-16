# Syntax of OCat
OCat, short for Open Command and Telemetry, is an open-source command and telemetry language compiler written in Python 3.10 using PLY. Python was chosen because of it's ability to
be distributable across machines without recompiling. It's also easy to read and understand. Many students and professionals that work in the space industry as non-software engineers
are probably more likely to know Python over more traditional languages. OCat attempts to create a programming language that compiles to a standardizes byte code that is very configurable.
Space missions take on many different shapes and sizes, and so does the hardware. This language is meant to compile to something low-level friendly, with customizable parameters, like 
variable count and register sizes. Below you can find a guide on how to write scripts in this language and customize it's compile settings.

## Declaration, Assignment, and Expressions
OCat currently supports these types of variables: `int`, `uint`, `float`, `bool`, `sci`, and `tlm`. All variables in OCat are immutable by default, once set, they never change. If a variable must be mutated, it
must be explicitly declared:
```
int x = 2
mut float pi = 3.14
```
OCat can perform the following arithmetic operations: +, -, *, and /

Other supported operations include: `and`, `or`, `not`, `xor`, ~, ==, !=, >, <, <=, >=, **, %, &, |, ^, <<, >>

## Commands and Telemetry
OCat has three built-in routines for sending commands and fetching telemetry. First let's look at the built-in for sending commands: `send`
```
# The first argument is the command, the next arguments belong to that command
send (cmd_with_arg, 5, 4)

# Arguments can be named as such
send (command => camera_settings, iso => 1000, f => 5.6, ss => 1)

# Send can also capture a response
int status = send (noop)
```
Next let's take a look at the two fetching telemetry built-ins: `fetch` and `fetch_new`
Note: The special `tlm` variable. It's value depends on `fetch` return, and could always hold a timeout flag
```
# Like send(), the first argument is the telemetry item, but unlike send(), the number of arguments is capped at 3. The second and third arguments
#  are guards, in english, this request might be read: "fetch the current speed only if it's greater or equal to 40, stop trying after 5 seconds"
#  The result is stored in the variable speed, which we also used in our second argument. 
tlm speed = fetch (current_speed, speed >= 40, for 5)

# A fetch can also block with no timeout, a compiler warning will be produced.
tlm speed = fetch (current_speed, speed >= 40, forever)
tlm speed = fetch (current_speed, speed >= 40)

# Another built-in, fetch_new, can be used to reject stale telemetry, newness requirements can be on individual telemetry items
tlm new_speed = fetch_new (current_speed, speed >= 40, until 112000)

# A fetch can also return immediately
tlm speed = fetch (current_speed)

# Fetch and fetch_new also has named arguments
fetch (telemetry => current_speed, condition => speed >= 40, wait => until 12379)
```
What happens if my telemetry times out??? Well, it depends! Let's look:
```
# This condition probably won't succeed, so this fetch will timeout
tlm speed = fetch (current_speed, speed > 299792458, for 5)
if speed.timeout then 
    send (too_slow)
else
    send (slow_down)
end if
# You can write timeout check/recovery anywhere that you have access to your tlm variable. If speed.timeout is set, then reading it's value will cause a runtime error.
```

## Conditionals
OCat supports chained and nested if/else if/else if/else blocks, as well as switch/case statements
```
if temp >= 45 and temp <= 65 then
    send (cmd_temp_nominal)
else
    send (cmd_not_chill)
end if
```

## Loops:
The following three loops are supported in OCat

### for loop
For loops repeat over some range, keeping track of said range in a special iterator variable. Iterators are size to fit the range specified in the for loop,
and they cannot be changed by the user. For loops are bidirectional, with a default step of either 1 or -1. Ranges can only be specified using integers.
Here are some examples:

1.  Increment from 0 to 10 (exclusive) with step 1
```
for itr in (0, 10) loop
    send (cmd_inc, itr)
end loop
```
2.  Decrement from 9 to -1 (exclusive) with step -1
```
for itr in (9, -1) loop
    send (cmd_dec, itr)
end loop
```
3. Increment from 0 to 21 (exclusive) with custom step
```
for itr in (0, 21, 2) loop
    send (cmd_step, itr)
end loop
```







dict = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}
nums = []
for key, value in dict.items():
    if type(value) == int:
        nums.append(value)

print(sum(nums))

array = [0, 1, 2, 3]

address = 2

print(array[address])
def ram_write(value, address):
    """Accept a value to write, and the address to write it to."""
    array[address] = value

ram_write(9, 0)
print(array)

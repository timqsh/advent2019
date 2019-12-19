import sys
import re
import math
import bisect


def parse_input(text):
    recipes = {}
    for line in text.splitlines():
        *materials_strings, product_string = re.findall(r"\d+\s\w+", line)
        product_num, product_name = get_count_and_name(product_string)
        materials_list = [get_count_and_name(s) for s in materials_strings]
        recipes[product_name] = product_num, materials_list
    return recipes


def get_count_and_name(string):
    count_str, name = string.split()
    count = int(count_str)
    return count, name


def get_ore_to_produce(product, amount):
    if product == "ORE":
        return amount
    product_num, materials = recipes[product]
    remaining_amount = amount - materials_count[product]
    batches = math.ceil(remaining_amount / product_num)
    produced = batches * product_num
    overhead = produced - amount
    materials_count[product] += overhead
    total = 0
    for mat in materials:
        mat_amount, mat_name = mat
        total += get_ore_to_produce(mat_name, batches * mat_amount)
    return total


input_text = sys.stdin.read()
recipes = parse_input(input_text)
materials_count = {mat: 0 for mat in recipes}

result = get_ore_to_produce("FUEL", 1)
print(result)


class OreToProduceGetter:
    def __getitem__(self, key):
        return get_ore_to_produce("FUEL", key)


ore_to_produce_getter = OreToProduceGetter()

res2 = bisect.bisect_left(ore_to_produce_getter, 10 ** 12, 1, 10 ** 12) - 1
print(res2)

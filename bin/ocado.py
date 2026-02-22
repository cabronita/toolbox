#!/usr/bin/env python3

from datetime import datetime, timedelta
from decimal import Decimal
from pprint import pprint

ocado = []
maximum = 0

def get_annual_cost(date):
    total = 0
    start_date = date - timedelta(days=365)
    for i in ocado:
        if start_date < i['date'] <= date:
            total += i['payment']
    print(date, total)
    return total


with open("i") as f:
    for line in f:
        d, p, _, _ = line.strip().split()
        d = datetime.strptime(d, "%d-%b-%y").date()
        p = Decimal(p.replace(",", ""))
        ocado.append({"date": d, "payment": p})
        ocado = sorted(ocado, key=lambda i: i['date'])

b = ocado[0]['date'] + timedelta(days=365)

for i in ocado:
    if i['date'] >= b:
        result = get_annual_cost(i['date'])
        if result > maximum:
            maximum = result

print(f"Maximum annual: {maximum}")
print(f"Maximum monthly: {maximum/12:.2f}")

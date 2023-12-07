import io
import numpy as np
import pandas as pd
import pathlib as pt
import matplotlib.pyplot as plt
from itertools import count, islice
from PIL import Image

ROOTS = 6
NUMS = 100000
MAXDOTS = 100

assert ROOTS > 0 and NUMS > 0

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def plot(A, i):
    plt.figure(i, figsize=(18, 6), dpi=80)
    plt.title('$f({0}, x)$'.format(i))
    plt.xlabel('Ряд составных чисел')
    plt.ylabel('Степень простого числа')

    a = A[i]
    for j in range(max(a)):
        if len(a[a==j]) > 100:
            a = a[a!=j]

    plt.scatter(a.index, a, s=15)
    fig = plt.gcf()
    img = fig2img(fig)
    dir = pt.Path(__file__).parent.resolve()
    name = '{0}_image.png'.format(i);
    path = pt.PurePath(dir, 'img', name)
    img.save(str(path))

def primaries(n):
    primes = (n for n in count(2) if all(n % d for d in range(2, n)))
    primes = islice(primes, 0, n)
    return np.fromiter(primes,dtype=int)

def primfacs(n, primes):
    i = 2
    primfac = []
    while i * i <= n and i <= primes[ROOTS-1]:
        while n % i == 0:
            primfac.append(int(i))
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(int(n))
    return primfac

def powers(primfac, primes):
    result = []
    for i in range(ROOTS):
        prim = primes[int(i)]
        powr = primfac.count(int(prim))
        result.append(int(powr))
    return result

primes = primaries(ROOTS)
row = powers(primfacs(1, primes), primes)
A = np.array(row)

for i in range(2, NUMS + 1):
    row = powers(primfacs(i, primes), primes)
    A = np.vstack([A, row])

idx = np.array([x for x in range(1, NUMS + 1)])
A = pd.DataFrame(A, idx, primes)

for i in primes:
    plot(A, i)

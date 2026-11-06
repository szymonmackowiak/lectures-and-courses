import numpy as np
from random import random, shuffle, seed
import matplotlib.pyplot as plt


class Perceptron:

    def __init__(self, n, c):
        self.eta = c
        self.n = n
        self.w = []
        self.error = []
        for i in range(self.n):
            self.w.append(2*np.random.rand(1)[0] - 1)

    def dotProduct(self, x):
        vsum = 0
        for i in range(self.n):
            vsum = vsum + x[i]*self.w[i]
        return vsum

    def activation(self, vsum):
        if vsum > 0:
            return 1
        else:
            return -1

    def predict(self, x):
        vsum = self.dotProduct(x)
        return self.activation(vsum)

    def fit(self, x, x_target):
        answer = self.predict(x)
        error = x_target - answer
        self.error.append(error)
        for i in range(self.n):
            self.w[i] = self.w[i] + self.eta*error*x[i]
        return error


def label(x1p, x2p):
    y_line = -x1p + 10
    if x2p - y_line > 0:
        return 1
    else:
        return -1


# Powtarzalne wyniki na kolejnych uruchomieniach
np.random.seed(1)
seed(1)

p = Perceptron(3, 0.0001)

# 1000 punktow zamiast miliona - wygodniej na zajeciach
m = 1000
x = []
y_target = []

for i in range(m):
    x1p = 20*random() - 10
    x2p = 20*random()
    x.append([x1p, x2p, 1])   # Ostatnia jedynka: bias
    y_target.append(label(x1p, x2p))

# Jedna epoka: prezentacja wszystkich punktow
n_epochs = 20
error_history = []

for epoch in range(n_epochs):
    order = list(range(m))
    shuffle(order)

    mistakes = 0
    for i in order:
        error = p.fit(x[i], y_target[i])
        if error != 0:
            mistakes = mistakes + 1

    error_history.append(mistakes)
    print("Epoka:", epoch + 1, "Bledy:", mistakes)

print("Wyuczone wagi:", p.w)

# Wykres 1: liczba pomylek w kazdej epoce
plt.figure(figsize=(8, 4))
plt.plot(range(1, n_epochs + 1), error_history, marker="o")
plt.xlabel("Epoka")
plt.ylabel("Liczba blednych klasyfikacji")
plt.title("Uczenie perceptronu")
plt.grid()
plt.tight_layout()
plt.savefig("perceptron_bledy.png", dpi=160)

# Wykres 2: punkty wedlug prawidlowych etykiet
x1_plus = []
x2_plus = []
x1_minus = []
x2_minus = []
x1_wrong = []
x2_wrong = []

for i in range(m):
    if y_target[i] == 1:
        x1_plus.append(x[i][0])
        x2_plus.append(x[i][1])
    else:
        x1_minus.append(x[i][0])
        x2_minus.append(x[i][1])

    if p.predict(x[i]) != y_target[i]:
        x1_wrong.append(x[i][0])
        x2_wrong.append(x[i][1])

plt.figure(figsize=(8, 6))
plt.scatter(x1_plus, x2_plus, s=10, label="Klasa +1")
plt.scatter(x1_minus, x2_minus, s=10, label="Klasa -1")

# Prawdziwa linia: x2 = -x1 + 10
xx = [-10, 10]
yy_true = [-xx[0] + 10, -xx[1] + 10]
plt.plot(xx, yy_true, "k--", label="Prosta wzorcowa")

# Granica perceptronu: w0*x1 + w1*x2 + w2 = 0
if abs(p.w[1]) > 1e-12:
    yy_perceptron = []
    for x1p in xx:
        yy_perceptron.append(-(p.w[0]*x1p + p.w[2])/p.w[1])
    plt.plot(xx, yy_perceptron, "r-", label="Prosta perceptronu")

if len(x1_wrong) > 0:
    plt.scatter(x1_wrong, x2_wrong, s=35, marker="x", c="black",
                label="Bledne klasyfikacje")

plt.xlim(-10, 10)
plt.ylim(0, 20)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Klasyfikacja punktow przez perceptron")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("perceptron_granica.png", dpi=160)
plt.show()

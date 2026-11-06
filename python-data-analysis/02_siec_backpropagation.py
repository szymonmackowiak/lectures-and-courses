from math import exp
from random import random, seed, shuffle
import matplotlib.pyplot as plt
import numpy as np


def sigmoid(vsum):
    return 1/(1 + exp(-vsum))


class Neuron:

    def __init__(self, n):
        self.n = n
        self.w = []
        for i in range(n + 1):  # n wag wejsc i jedna waga biasu
            self.w.append(2*random() - 1)
        self.x = []
        self.y = 0
        self.delta = 0

    def dotProduct(self, x):
        vsum = 0
        for i in range(self.n + 1):
            vsum = vsum + x[i]*self.w[i]
        return vsum

    def activation(self, vsum):
        return sigmoid(vsum)

    def predict(self, x):
        self.x = x + [1]       # Bias = dodatkowe wejscie o wartosci 1
        vsum = self.dotProduct(self.x)
        self.y = self.activation(vsum)
        return self.y


class Layer:

    def __init__(self, n_inputs, n_neurons):
        self.neurons = []
        for i in range(n_neurons):
            self.neurons.append(Neuron(n_inputs))

    def predict(self, x):
        y = []
        for neuron in self.neurons:
            y.append(neuron.predict(x))
        return y


class NeuralNetwork:

    def __init__(self, structure, c):
        self.eta = c
        self.layers = []
        for i in range(len(structure) - 1):
            self.layers.append(Layer(structure[i], structure[i+1]))

    def predict(self, x):
        y = x
        for layer in self.layers:
            y = layer.predict(y)
        return y

    def fit(self, x, y_target):
        # KROK 1. Propagacja w przod
        y = self.predict(x)

        # KROK 2. Delta neuronow warstwy wyjsciowej
        output_layer = self.layers[-1]
        for i in range(len(output_layer.neurons)):
            neuron = output_layer.neurons[i]
            error = y_target[i] - neuron.y
            neuron.delta = error*neuron.y*(1-neuron.y)

        # KROK 3. Delta neuronow warstw ukrytych (od konca)
        for k in range(len(self.layers) - 2, -1, -1):
            layer = self.layers[k]
            next_layer = self.layers[k+1]
            for i in range(len(layer.neurons)):
                neuron = layer.neurons[i]
                weighted_error = 0
                for next_neuron in next_layer.neurons:
                    weighted_error += next_neuron.w[i]*next_neuron.delta
                neuron.delta = weighted_error*neuron.y*(1-neuron.y)

        # KROK 4. Aktualizacja wag (dopiero po obliczeniu wszystkich delt)
        for layer in self.layers:
            for neuron in layer.neurons:
                for i in range(neuron.n + 1):
                    neuron.w[i] += self.eta*neuron.delta*neuron.x[i]

        # Blad sredniokwadratowy dla pojedynczego przykladu / 2
        loss = 0
        for i in range(len(y)):
            loss += 0.5*(y_target[i] - y[i])**2
        return loss


seed(3)

# Problem XOR: jedna prosta nie wystarczy
x = [[0, 0], [0, 1], [1, 0], [1, 1]]
y_target = [[0], [1], [1], [0]]

# 2 wejscia -> 4 neurony ukryte -> 1 wyjscie
net = NeuralNetwork([2, 4, 1], 0.5)

n_epochs = 12000
loss_history = []

for epoch in range(n_epochs):
    order = [0, 1, 2, 3]
    shuffle(order)

    loss = 0
    for i in order:
        loss += net.fit(x[i], y_target[i])
    loss_history.append(loss/len(x))

    if (epoch + 1) % 1000 == 0:
        print("Epoka:", epoch + 1, "Srednia strata:", loss_history[-1])

print("\nWyniki po uczeniu:")
for i in range(len(x)):
    answer = net.predict(x[i])[0]
    category = 1 if answer >= 0.5 else 0
    print("Wejscie:", x[i], "Oczekiwane:", y_target[i][0],
          "Wyjscie:", round(answer, 3), "Klasa:", category)

plt.figure(figsize=(8, 4))
plt.plot(range(1, n_epochs + 1), loss_history)
plt.xlabel("Epoka")
plt.ylabel("Srednia strata")
plt.title("Uczenie sieci [2, 4, 1] - XOR")
plt.grid()
plt.tight_layout()
plt.savefig("siec_xor_uczenie.png", dpi=160)

# Dodatkowa wizualizacja: granica decyzyjna sieci
xx = np.linspace(-0.25, 1.25, 90)
yy = np.linspace(-0.25, 1.25, 90)
xx_grid, yy_grid = np.meshgrid(xx, yy)
predictions = np.zeros_like(xx_grid)

for i in range(len(yy)):
    for j in range(len(xx)):
        predictions[i, j] = net.predict([xx_grid[i, j], yy_grid[i, j]])[0]

plt.figure(figsize=(6, 5))
plt.contourf(xx_grid, yy_grid, predictions, levels=[0, 0.5, 1], alpha=0.25)
plt.contour(xx_grid, yy_grid, predictions, levels=[0.5], colors="black")
for i in range(len(x)):
    plt.scatter(x[i][0], x[i][1], s=100, marker="o" if y_target[i][0] == 1 else "x",
                c="black")
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Nieliniowa granica decyzyjna - XOR")
plt.grid()
plt.tight_layout()
plt.savefig("siec_xor_granica.png", dpi=160)
plt.show()

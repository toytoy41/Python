import numpy as np
import matplotlib.pyplot as plt

t1 = False

if t1 :
    x = np.array([1.0,2.0,3.0])
    print(x)
    print(type(x))
else:
    x = np.arange(0, 6, 0.1)
    y1 = np.sin(x)
    y2 = np.cos(x)

    plt.plot(x, y1, label = "sin")
    plt.plot(x, y2, linestyle = "--", label="cos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title('sin & cos')
    plt.legend()
    plt.show()
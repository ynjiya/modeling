from prettytable import PrettyTable
import matplotlib.pyplot as plt

# Подбираем шаг:

# Euler:
# При 1e-1 y(1) = 0.2925421046
# При 1e-2 y(1) = 0.3331073593
# При 1e-3 y(1) = 0.3484859823
# При 1e-4 y(1) = 0.3501691515
# При 1e-5 y(1) = 0.3502255745
# Шаг ничего не меняет (между 1e-3 и 1e-4)
# Значит мы подобрали нужный нам шаг.

# Runge:
# При 1e-1 y(1) = 0.3485453439
# При 1e-2 y(1) = 0.3391265967
# При 1e-3 y(1) = 0.3491103993
# При 1e-4 y(1) = 0.3502318426
# При 1e-5 y(1) = 0.3502318443
# Аналогично.

MAX_X = 1
STEP = 1e-4
Y_0 = 0
X_0 = 0

def f(x, y):
    return x * x + y * y


def fp1(x):
    return pow(x, 3) / 3


def fp2(x):
    return fp1(x) + pow(x, 7) / 63


def fp3(x):
    return fp2(x) + \
           2 * pow(x, 11) / 2079 + \
           pow(x, 15) / 59535



def fp4(x):
    return fp2(x) + \
        2 * pow(x, 11) / 2079 + \
        13 * pow(x, 15) / 218295 + \
        82 * pow(x, 19) / 37328445 + \
        662 * pow(x, 23) / 10438212015 + \
        4 * pow(x, 27) / 3341878155 + \
        pow(x, 31) / 109876903905


def Picar(x_min, x_max, h, func, y_0):
    result = list()
    x, y = x_min, y_0

    while x < x_max:
        result.append(y)
        x += h
        y = y_0 + func(x)

    return result


def Euler(x_min, x_max, h, y_0):
    result = list()
    x, y = x_min, y_0

    while x < x_max:
        result.append(y)
        y = y + h * f(x, y)
        x += h

    return result


def Runge(x_min, x_max, h, y_0, alpha):
    # alpha = 1
    result = list()
    coeff = h / (2 * alpha)
    x, y = x_min, y_0

    while x < x_max:
        result.append(y)
        y = y + h * ((1 - alpha) * f(x, y) +
                      alpha * f(x + coeff, y + coeff * f(x, y)))
        x += h

    return result


def x_range(x_min, x_max, h):
    result = list()
    x = x_min
    while x < x_max:
        result.append(round(x, 4))
        # result.append(x)
        x += h
    return result


def main():
    tb = PrettyTable()
    fig, g = plt.subplots()

    tb.add_column("X", x_range(X_0, MAX_X, STEP))
    tb.add_column("Picard 1", Picar(X_0, MAX_X, STEP, fp1, Y_0))
    tb.add_column("Picard 2", Picar(X_0, MAX_X, STEP, fp2, Y_0))
    tb.add_column("Picard 3", Picar(X_0, MAX_X, STEP, fp3, Y_0))
    tb.add_column("Picard 4", Picar(X_0, MAX_X, STEP, fp4, Y_0))
    tb.add_column("Euler", Euler(X_0, MAX_X, STEP, Y_0))
    tb.add_column("Runge-Kutta", Runge(X_0, MAX_X, STEP, Y_0, 1))

    print(tb[::500])
    # print(tb[::100])
    # print(tb)


    g.plot(x_range(- MAX_X, MAX_X, STEP), Picar(- MAX_X, MAX_X, STEP, fp1, Y_0), label="Picar 1")
    g.plot(x_range(- MAX_X, MAX_X, STEP), Picar(- MAX_X, MAX_X, STEP, fp2, Y_0), label="Picar 2")
    g.plot(x_range(- MAX_X, MAX_X, STEP), Picar(- MAX_X, MAX_X, STEP, fp3, Y_0), label="Picar 3")
    g.plot(x_range(- MAX_X, MAX_X, STEP), Picar(- MAX_X, MAX_X, STEP, fp4, Y_0), label="Picar 4")
    g.plot(x_range(0, MAX_X, STEP), Euler(X_0, MAX_X, STEP, Y_0), label="Euler")
    g.plot(x_range(0, MAX_X, STEP), Runge(X_0, MAX_X, STEP, Y_0, 1), label="Runge Kutta")

    l1 = Euler(X_0, MAX_X, 1e-5, Y_0)
    l2 = Euler(X_0, MAX_X, 1e-6, Y_0)
    # l3 = Runge(X_0, MAX_X, STEP, Y_0, 1)

    print(l1[-1])
    print(l2[-1])


    g.legend()
    g.grid()
    plt.show()



if __name__ == "__main__":
    main()



from StateMachine import StateMachine
from Lehmer import Lehmer

startValue = 995053
multiplier = 550000
modulus = 1000002
startState = "000"
N = 1000000
T = 2

def main():
    inf = False
    try:
        po = float(input("po: "))
        p1 = float(input("p1: "))
        p2 = float(input("p2: "))
    except:
        po = 0.5
        p1 = 0.6
        p2 = 0.6
    if po == 1.0 or p2 == 1.0 or p1 == 1.0:
        inf = True

    generator = Lehmer(multiplier, startValue, modulus)
    stateMachine = StateMachine(startState, po, p1, p2)

    for i in range(N):
        po = generator.GetNext()
        p1 = generator.GetNext()
        p2 = generator.GetNext()
        stateMachine.SwitchState(po <= stateMachine.po, p1 <= stateMachine.p1, p2 <= stateMachine.p2)

    doneTime = 0
    for item in stateMachine.requests:
        if item.state == "Done":
            doneTime += item.time

    print("P000: {0:.5f}".format(stateMachine.P000 / N))
    print("P010: {0:.5f}".format(stateMachine.P010 / N))
    print("P001: {0:.5f}".format(stateMachine.P001 / N))
    print("P110: {0:.5f}".format(stateMachine.P110 / N))
    print("P011: {0:.5f}".format(stateMachine.P011 / N))
    print("P111: {0:.5f}".format(stateMachine.P111 / N))
    print("P211: {0:.5f}".format(stateMachine.P211 / N))
    print("P210: {0:.5f}".format(stateMachine.P210 / N))

    if inf:
        print("Channel blocked")
    else:
        print(f"Вероятность отказа (Potk): {stateMachine.dcl / stateMachine.ga}")
        print(f"Вероятность блокировки (Pbl): {0}")
        print(f"Средняя длина очереди (Loch): {stateMachine.Loch / N}")
        print(f"Среднее число заявок, находящихся в системе (Lc): {stateMachine.Lc / N }")
        print(f"Относительная пропускная способность (Q): {stateMachine.A / stateMachine.ga}")
        print(f"Абсолютная пропускная способность (A): {stateMachine.A / N}")
        print(f"Среднее время пребывания заявки в очереди (Woch): {stateMachine.Loch / stateMachine.en}")
        print(f"Среднее время пребывания заявки в системе (Wc): {doneTime / stateMachine.A}")
        print(f"Коэффициент загрузки канала (K1): {stateMachine.K1 / N}")
        print(f"Коэффициент загрузки канала (K2): {stateMachine.K2 / N}")

if __name__ == "__main__":
    main()
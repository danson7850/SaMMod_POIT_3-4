class Request:
    
    def __init__(self):
        self.time = 0
        self.state = "None"

class StateMachine:

    def __init__(self, startState, po, p1, p2):
        self.state = startState
        self.po = po
        self.p1 = p1
        self.p2 = p2

        self.P000 = 0
        self.P001 = 0
        self.P010 = 0
        self.P110 = 0
        self.P011 = 0
        self.P111 = 0
        self.P211 = 0
        self.P210 = 0

        self.ga = 0
        self.dcl = 0
        self.en = 0

        self.Pbl = 0
        self.Potk = 0
        self.Q = 0
        self.Loch = 0
        self.Lc = 0
        self.A = 0
        self.K1 = 0
        self.K2 = 0

        self.machine = [None, None, None, None]
        self.requests = []

    def __CalculateRequestsTime(self, po, p1, p2):
        if (self.machine[3] != None) and (not p2):
            self.machine[3].state = "Done"
            self.machine[3] = None
        
        if (self.machine[2] != None) and (not p1):
            if self.machine[3] != None:
                self.machine[2].state = "Declined"
            else:
                self.machine[3] = self.machine[2]

            self.machine[2] = None

            if self.machine[1] != None:
                self.machine[2] = self.machine[1]
                self.machine[1] = None
                if self.machine[0] != None:
                    self.machine[1] = self.machine[0]
                    self.machine[0] = None

        if not po:
            request = Request()
            self.requests.append(request)
            if self.machine[0] != None:
                request.state = "Declined"
            else:
                if self.machine[1] != None:
                    self.machine[0] = request
                else:
                    if self.machine[2] != None:
                        self.machine[1] = request
                    else:
                        self.machine[2] = request
                    
        for request in self.machine:
            if request != None:
                request.time += 1

    def SwitchState(self, po, p1, p2):
        self.__CalculateRequestsTime(po, p1, p2)

        if not po:
            self.ga += 1   
        if self.state[0] != "2" and not po:
            self.en += 1

        if self.state == "000":
            self.P000 += 1
            if po:
                self.state = "000"
            if not po:
                self.state = "010"

        elif self.state == "010":
            self.K1 += 1
            self.Lc += 1

            self.P010 += 1
            if po and p1:
                self.state = "010"
            if (not po) and p1:
                self.state = "110"
            if po and (not p1):
                self.state = "001"
            if (not po) and (not p1):
                self.state = "011"

        elif self.state == "001":
            if not p2:
                self.A += 1
            self.K2 += 1
            self.Lc += 1

            self.P001 += 1
            if po and (not p2):
                self.state = "000"
            if po and p2:
                self.state = "001"
            if (not po) and (not p2):
                self.state = "010"
            if (not po) and p2:
                self.state = "011"

        elif self.state == "110":
            self.K1 += 1
            self.Loch += 1
            self.Lc += 2

            self.P110 += 1
            if po and p1:
                self.state = "110"
            if po and (not p1):
                self.state = "011"
            if (not po) and p1:
                self.state = "210"
            if (not po) and (not p1):
                self.state = "111"

        elif self.state == "011":
            if not p2:
                self.A += 1
            elif not p1:
                self.dcl += 1
            self.K1 += 1
            self.K2 += 1
            self.Lc += 2

            self.P011 += 1
            if (po and p1 and p2) or ((not po) and (not p1)):
                self.state = "011"
            elif po and p1 and (not p2):
                self.state = "010"
            elif po and not p1:
                self.state = "001"
            elif (not po) and p1 and (not p2):
                self.state = "110"
            elif (not po) and p1 and p2:
                self.state = "111"

        elif self.state == "111":
            if not p2:
                self.A += 1
            elif not p1:
                self.dcl += 1
            self.Loch += 1
            self.K1 += 1
            self.K2 += 1
            self.Lc += 3

            self.P111 += 1
            if (po and p1 and p2) or ((not po) and (not p1)):
                self.state = "111"
            if po and (not p1):
                self.state = "011"
            if po and p1 and (not p2):
                self.state = "110"
            if (not po) and p1 and p2:
                self.state = "211"
            if (not po) and p1 and (not p2):
                self.state = "210"

        elif self.state == "211":
            if not p2:
                self.A += 1
            elif not p1:
                self.dcl += 1
            if not po and p1:
                self.dcl += 1
            self.Loch += 2
            self.K1 += 1
            self.K2 += 1
            self.Lc += 4

            self.P211 += 1 
            if (po and p1 and p2) or ((not po) and (not p1) and (not p2)) or (not po) and p2:
                self.state = "211"
            if po and (not p1):
                self.state = "111"
                self.en += 1
            if p1 and (not p2):
                self.state = "210"

        elif self.state == "210":
            if not po and p1:
                self.dcl += 1
            self.K1 += 1
            self.Loch += 2
            self.Lc += 3

            self.P210 += 1 
            if po and p1 or (not po) and p1:
                self.state = "210"
            if po and (not p1):
                self.state = "111"
                self.en += 1
            if (not po) and (not p1):
                self.state = "211"
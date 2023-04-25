import math
import random

class Process:
    def __init__(self):
        self.arrivalTime = 0
        self.serviceTime = 0
        self.startTime = 0
        self.endTime = 0
        self.responseRatio = 0
        self.remainingTime = 0

class CPU:
    def __init__(self):
        self.clock = 0
        self.busy = False
        self.current = Process()

class Event:
    def __init__(self):
        self.time = 0
        self.type = ""
        self.process = Process()

class Sim:
    def __init__(self, scheduler, valueOfLambda, serviceTime, finishOff):
        self.cpu = CPU()
        self.scheduler = scheduler
        self.valOfLambda = valueOfLambda
        self.avgServiceTime = serviceTime
        self.end_condition = finishOff
        self.completedProcesses = 0
        self.turnaroundTime = 0
        self.totalServiceTime = 0
        self.processesInReadyQ = 0
        self.readyQueue = []
        self.eventQueue = []

    # generates new event when function is called
    # function returns event
    def generateEvent(self, time, type, process):

        event = Event()
        event.time = time
        event.type = type
        event.process = process

        return event

    # generates a new process
    # function returns process
    def generateProcess(self):
        process = Process()
        process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.valOfLambda))
        process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1 / self.avgServiceTime))
        process.remaining_service_time = process.service_time
        process.end_time = process.arrival_time + process.service_time
        process.start_time = 0

        return process

    def FCFS(self):

        firstProcess = self.generateProcess()
        firstEvent = self.generateEvent(firstProcess.arrival_time, "ARR", firstProcess)
        self.eventQueue.append(firstEvent)

        # runs until all processes are completed
        while self.completedProcesses < self.end_condition:

            # poisson distribution
            self.eventQueue.sort(key=lambda x: x.time)
            # get the event
            event = self.eventQueue.pop(0)
            # set the clock
            self.cpu.clock = event.time
            # event type is arrival
            if event.type == "ARR":
                # ready queue is empty
                if self.cpu.busy is False:
                    self.cpu.busy = True
                    # event is now a departure
                    event.type = "DEP"
                    event.process.end = self.cpu.clock + event.process.service_time
                    event.time = event.process.end
                    self.eventQueue.append(event)

                elif self.cpu.busy is True:
                    self.readyQueue.append(event.process)
                else:
                    print("Something is wrong")

                # do it all over again
                newProcess = self.generateProcess()
                newArrivalEvent = self.generateEvent(newProcess.arrival_time, "ARR", newProcess)
                self.eventQueue.append(newArrivalEvent)

            elif event.type == "DEP":

                self.processesInReadyQ += len(self.readyQueue)
                self.completedProcesses += 1
                self.turnaroundTime += (self.cpu.clock - event.process.arrival_time)
                self.totalServiceTime += event.process.service_time

                #  cpu goes idle
                #  event is deleted
                if len(self.readyQueue) == 0:
                    self.cpu.busy = False
                # departure event is created
                else:
                    departing = self.readyQueue.pop(0)
                    departing.start = self.cpu.clock
                    departing.end = departing.start + departing.service_time
                    newDepartureEvent = self.generateEvent(departing.end, "DEP", departing)
                    self.eventQueue.append(newDepartureEvent)
            else:
                print("Invalid Event Type")

        self.readyQueue.clear()
        self.eventQueue.clear()
        self.completedProcesses = 0

    # this function runs the simulator
    def run(self):
        if self.scheduler == 1:
            self.FCFS()
        else:
            print("Invalid input.")

    # this function generates a report
    def generateReport(self):
        if self.scheduler == 1:
            label = "FCFS"

        # calculations
        avgTurnaroundTime = round((self.turnaroundTime / self.end_condition), 3)
        throughput = round((self.end_condition / self.cpu.clock), 3)
        utilization = round(self.totalServiceTime / self.cpu.clock, 3)
        avg_num_processes_in_readyQ = round(self.processesInReadyQ / self.end_condition, 3)

        # after calculations are complete
        # writes to a separate txt file named results.txt
        if self.scheduler == 1 and self.valOfLambda == 10:
            with open("results.txt", "w+") as results_file:
                results_file.write(
                    "Lambda\tTurnaround Time\t Throughput\t CPU Util\t   Avg#ProcReadyQ\n")
                results_file.write(
                    "--------------------------------------------------------------\n")
                results_file.write('{:>6}'.format(str(self.valOfLambda)) + str("\t"))
                results_file.write('{:>17}'.format(str(avgTurnaroundTime)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\n"))
                results_file.close()
        elif self.valOfLambda == 30:
            with open("results.txt", "a+") as results_file:
                results_file.write('{:>6}'.format(str(self.valOfLambda)) + str("\t"))
                results_file.write('{:>17}'.format(str(avgTurnaroundTime)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\n"))
                results_file.close()
        else:
            with open("results.txt", "a+") as results_file:
                results_file.write('{:>6}'.format(str(self.valOfLambda)) + str("\t"))
                results_file.write('{:>17}'.format(str(avgTurnaroundTime)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\n"))
                results_file.close()

if __name__ == "__main__":
    cntrLambda = 10
    for scheduler in range(1, 2):
        if scheduler == 1:
            print("Running FCFS Scheduler")
            while cntrLambda < 31:
                sim = Sim(scheduler, cntrLambda, .04, 10000)
                sim.run()
                sim.generateReport()
                cntrLambda += 1
            cntrLambda = 10

        else:
            print("Invalid input.")
        scheduler += 1

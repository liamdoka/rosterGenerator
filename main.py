import json
import datetime
from random import randint
from math import floor


class EmployeeList:
    def __init__(self):
        self.employees = []

    def add_employee(self, name, capability=0, availability=[], weekly_hours=0, weekly_shifts=0, wage=15, rank="TM"):
        new_employee = Employee(name, len(self.employees),capability, availability, weekly_hours, weekly_shifts, wage, rank)
        self.employees.append(new_employee)

    def remove_employee(self, name):
        for employee in self.employees:
            if employee.name == name:
                self.employees.remove(employee)


class Employee:
    def __init__(self, name, idx, capability=0, availability=[], weekly_hours=0, weekly_shifts=0, wage=15, rank="TM"):
        self.name = name
        self.id = idx
        self.capability = capability

        if availability == []:
            self.availability = 48*[True]
        else:
            self.availability = availability

        self.weekly_hours = weekly_hours
        self.weekly_shifts = weekly_shifts
        self.wage = wage
        self.rank = rank

    def is_available(self, start, end):
        return sum(self.availability[int(to_hours(start)*2) : int(to_hours(end*2))]) == 2*to_hours(start, end)


    def promote(self):
        if self.rank == "TM":
            self.rank = "TL"
        elif self.rank == "TL":
            self.rank = "ARM"
        else:
            raise ValueError("already the highest rank")

    def import_from(self, ex):
        self.name = ex["name"]
        self.id = ex["idx"]
        self.capability = ex["capability"]
        self.availability = ex["availability"]
        self.weekly_hours = ex["weekly_hours"]
        self.weekly_shifts = ex["weekly_shifts"]
        self.wage = ex["wage"]
        self.rank = ex["rank"]


class Shift:
    def __init__(self, Employee, start_time, end_time, station=""):
        self.employee = Employee

        self.start_time = start_time
        self.end_time = end_time
        
        span = [False] * 48
        for n in range(int(to_hours(self.start_time) * 2), int(to_hours(self.end_time) * 2)):
            span[n] = True

        self.span = span
        self.is_break = (to_hours(self.start_time, self.end_time) >= 5)
        self.cost = round((to_hours(self.start_time, self.end_time) - self.is_break * 0.5) * Employee.wage, 2)
        self.station = station


class Day:
    def __init__(self, ind, morning, night):
        today = datetime.date.today()
        self.date = today + datetime.timedelta(days= -today.weekday() + ind, weeks=1)
        self.extended = ind > 3 and ind < 6
        self.prediction = [morning, night]
        self.shifts = []
        self.ssdc = floor((self.extended * sum(self.prediction) / 6) + ((not self.extended) * sum(self.prediction) / 5.2))


class Week: 
    def __init__(self, start_date):
        self.start_date = start_date
        self.days = []


def get_random_employee(eligible, length):
    rand_employee = eligible[randint(0, len(eligible)-1)]
    rand_employee.weekly_hours -= length / 2
    rand_employee.weekly_shifts -= 1
    branch.employees[rand_employee.id] = rand_employee
    return rand_employee


def to_hours(start,end=datetime.timedelta(0)):
    return (abs(end-start)).total_seconds() / 3600




# CREATE EMPLOYEE LIST
branch = EmployeeList()
branch.add_employee("Sarah" , 4, [], 35, 5, 25, "ARM")
branch.add_employee("Em"    , 4, [], 35, 5, 25, "ARM")
branch.add_employee("Dylan" , 4, [], 35, 5, 25, "ARM")
branch.add_employee("Ben"   , 3, [], 30, 4, 22, "TL")
branch.add_employee("Haylie", 3, [], 25, 4, 22, "TL")
branch.add_employee("Bella" , 3, [], 25, 4, 22, "TL")
branch.add_employee("Chloe" , 3, [], 25, 4, 22, "TL")
branch.add_employee("Jack"  , 3, [], 25, 4, 22, "TL")
branch.add_employee("Beau"  , 2, [], 20, 3, 18, "TM")
branch.add_employee("Wren"  , 2, [], 20, 3, 18, "TM")
branch.add_employee("David" , 2, [], 20, 3, 18, "TM")
branch.add_employee("Pat"   , 2, [], 20, 3, 18, "TM")
branch.add_employee("Tia"   , 2, [], 20, 3, 18, "TM")
branch.add_employee("Jazz"  , 2, [], 20, 3, 18, "TM")
branch.add_employee("Zoe"   , 2, [], 20, 3, 18, "TM")
branch.add_employee("Taylor", 2, [], 20, 3, 18, "TM")
branch.add_employee("Liam"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Ryan"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Jake"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Tom"   , 1, [], 15, 3, 15, "TM")
branch.add_employee("Phoebe", 1, [], 15, 3, 15, "TM")
branch.add_employee("Lucy"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Charli", 1, [], 15, 3, 15, "TM")
branch.add_employee("Dane"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Sass"  , 1, [], 15, 3, 15, "TM")
branch.add_employee("Lachy" , 0, [], 10, 2, 15, "TM")

# CREATE UPCOMING WEEK
today = datetime.date.today()
monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
upcoming = Week(monday)

morning = [120,95,100,105,120,170,180]
night   = [180,185,220,245,400,325,215]

for idx in range(7):
    upcoming.days.append(Day(idx, morning[idx], night[idx]))


for day in upcoming.days:
    hours = 0

    #ADD AN EMPLOYEE >= TL For every hour.
    #ASSIGN AN OPENER
    start_time = datetime.timedelta(hours=randint(8,9))
    length = randint(12,16)
    end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)
    eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > 0 and employee.rank != "TM")]
    
    rand_employee = get_random_employee(eligible, length)
    period = Shift(rand_employee, start_time, end_time)
    day.shifts.append(period)
    hours += length / 2
    eligible.remove(rand_employee)

    #ASSIGN A CLOSING TL
    end_time = datetime.timedelta(hours=22 + day.extended)
    length = randint(12, 16)
    start_time = end_time - datetime.timedelta(hours=length//2, minutes=(length % 2) * 30)
    rand_employee = get_random_employee(eligible, length)

    period = Shift(rand_employee, start_time, end_time)
    day.shifts.append(period)
    hours += length / 2
    eligible.remove(rand_employee)

    #ASSIGN A SECOND OPENER
    start_time = datetime.timedelta(hours=9)
    length = randint(10,16)
    end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)
   
    n = 0
    eligible = []
    while len(eligible) == 0:
        eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
        for shift in day.shifts:
            if shift.employee in eligible:
                eligible.remove(shift.employee)
        n -= 1   

    rand_employee = get_random_employee(eligible, length)
    period = Shift(rand_employee, start_time, end_time)
    day.shifts.append(period)
    hours += length / 2
    eligible.remove(rand_employee)


    #ASSIGN 3 MORE CLOSERS
    for _ in range(3):
        n = 0
        eligible = []
        while len(eligible) == 0:
            eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
            for shift in day.shifts:
                if shift.employee in eligible:
                    eligible.remove(shift.employee)
            n -= 1

        # CREATE THE SHIFT LENGTH AND CORRESPONDING TIMES
        end_time = datetime.timedelta(hours=22 + day.extended)
        length = randint(8, 12)
        start_time = end_time - datetime.timedelta(hours=length//2, minutes=(length % 2) * 30)
        rand_employee = get_random_employee(eligible, length)

        #CREATE A SHIFT, AND Update HOURS
        period = Shift(rand_employee, start_time, end_time)
        day.shifts.append(period)
        hours += length / 2

    
    # ONE MORE OPENER TO START at 10:30am or 11am
    start_time = datetime.timedelta(minutes=(randint(21,22)*30))
    length = randint(8,9)
    end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)
    
    n = 0
    eligible = []
    while len(eligible) == 0:
        eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
        for shift in day.shifts:
            if shift.employee in eligible:
                eligible.remove(shift.employee)
        n -= 1

    rand_employee = get_random_employee(eligible, length)
    period = Shift(rand_employee, start_time, end_time)
    day.shifts.append(period)
    hours += length / 2




    # 4TH LUNCH PERSON
    start_time = datetime.timedelta(minutes=(randint(22,23)*30))
    length = randint(9,16)
    end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)

    n = 0
    eligible = []
    while len(eligible) == 0:
        eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
        for shift in day.shifts:
            if shift.employee in eligible:
                eligible.remove(shift.employee)
        n -= 1

    rand_employee = get_random_employee(eligible, length)
    period = Shift(rand_employee, start_time, end_time)
    day.shifts.append(period)
    hours += length / 2


    if day.prediction[0] > 125: # then we need 5 people over lunch
        start_time = datetime.timedelta(minutes=(randint(23,24)*30))
        length = randint(9,16)
        end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)

        n = 0
        eligible = []
        while len(eligible) == 0:
            eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
            for shift in day.shifts:
                if shift.employee in eligible:
                    eligible.remove(shift.employee)
            n -= 1

        rand_employee = get_random_employee(eligible, length)
        period = Shift(rand_employee, start_time, end_time)
        day.shifts.append(period)
        hours += length / 2

    # ASSIGN THE REST OF THE PEOPLE FOR THE DAY
    while hours < day.ssdc-4:
       
        # CREATE THE SHIFT LENGTH AND CORRESPONDING TIMES
        start_time = datetime.timedelta(hours=randint(13,18), minutes=(randint(0,1)*30))
        length = randint(6,16)
        end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)

        while end_time > datetime.timedelta(hours=21 + day.extended, minutes=30):
            length = randint(6,16)
            end_time = start_time + datetime.timedelta(hours=length // 2, minutes=(length % 2) * 30)

        #GET LIST OF eligible EMPLOYEES
        n = 0
        eligible = []
        while len(eligible) == 0:
            eligible = [employee for employee in branch.employees if (employee.is_available(start_time, end_time) and employee.weekly_shifts > n and employee.weekly_hours - (length/2) > -2)]
            for shift in day.shifts:
                if shift.employee in eligible:
                    eligible.remove(shift.employee)
            n -= 1

        rand_employee = get_random_employee(eligible, length)

        #CREATE A SHIFT, AND 
        period = Shift(rand_employee, start_time, end_time)
        day.shifts.append(period)
        hours += length / 2


for day in upcoming.days:
    count = 0
    output = []
    print(day.date)
    for idx in day.shifts:
        string = ""
        for x in idx.span[12:]:
            if not x: 
                string += "|"
            else:
                string += "_"
                count += 1
        output += [string + "\t" + idx.employee.name]

    for x in sorted(output):
        print(x)
    print(day.ssdc, ": ", count // 2)


#print([(person.name, person.weekly_shifts, person.weekly_hours) for person in branch.employees if person.weekly_shifts < 0])
print([person.name for person in branch.employees if person.weekly_shifts < 0])

#for idx in range(len(upcoming.days)):
#    print(upcoming.days[idx].date.weekday())
#    print([[shift.employee.name, to_hours(shift.start_time, shift.end_time)] for shift in upcoming.days[idx].shifts])

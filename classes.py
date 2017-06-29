#Craig O'Donnell
#Classes for Synchro program
#Last updated: 10/27/2016

class Intersection(object):
    #Intersection with the following properties:
        #name
        #number
        #control_type
        #overall_delay
        #overall_vc
        #approaches

    def __init__(self, name, number, control_type, overall_delay, overall_vc, approaches):
        #Return an intersection object with a name, number,
        #overall_delay, overall_vc, and approaches.

        self.name = name
        self.number = number
        self.control_type = control_type
        self.overall_delay = overall_delay
        self.overall_vc = overall_vc
        self.approaches = approaches #array
    
class Approach(object):
    #Approach with the following properties:
        #name (direction)
        #approach_delay
        #lanegroups

    def __init__(self, name, approach_delay, lanegroups):
        #Return an approach object with a name, approach_delay,
        #and lanegroups.

        self.name = name
        self.approach_delay = approach_delay
        self.lanegroups = lanegroups #array

class Lanegroup(object):
    #Lanegroup with the following properties:
        #name (movement)
        #vc_ratio
        #delay

    def __init__(self, name, vc_ratio, delay):
        #Return a lanegroup object with a name, vc_ratio, and delay.

        self.name = name
        self.vc_ratio = vc_ratio
        self.delay = delay

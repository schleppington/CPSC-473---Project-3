
########################################################################
#                         Constants                         #
########################################################################

#QUESTION: Would it be easier to store the string value inside the field?
#Answer - since we are programming for high traffic websites its faster
#           to compare ints then it is to compare strings. If we want to
#           take the easy way out we can just store the strings, but if
#           we want to do it the right way we leave it like this.
STATUS_NEEDS_ATTENTION = 0
STATUS_IN_PROGRESS = 1
STATUS_COMPLETED = 2

EVENT_TYPE_PUBLIC = 0
EVENT_TYPE_PRIVATE = 1

def getStatusStrFromInt(num):
    if num == 0:
        return 'Needs Attention'
    elif num == 1:
        return 'In Progress'
    elif num == 2:
        return 'Completed'
    else:
        return 'ERROR FETCHING STATUS STRING FOR: ' + num

def getEventTypeStrFromInt(num):
    if num == 0:
        return 'Public'
    elif num == 1:
        return 'Private'
    else:
        return 'ERROR FETCHING EVENT TYPE STRING FOR: ' + num

def getEventTypeFromStr(e):
    if e == "public":
        return EVENT_TYPE_PUBLIC
    elif e == "private":
        return EVENT_TYPE_PRIVATE
    else:
        return EVENT_TYPE_PRIVATE
    
def getStatusIntFromStr(s):
    if s == 'Needs Attention':
        return STATUS_NEEDS_ATTENTION
    elif s == 'In Progress':
        return STATUS_IN_PROGRESS
    elif s == 'Completed':
        return STATUS_COMPLETED
    else:
        return -1

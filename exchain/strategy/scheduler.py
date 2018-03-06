"""
Scheduler
"""

import sched
import time

SCHEDULER = sched.scheduler(time.time, time.sleep)

def run_schedule(interval, execute, argument=()):
    """
    Run schedule
    """
    SCHEDULER.enter(delay(interval), 1, schedule, (interval, execute, argument))
    SCHEDULER.run()

def schedule(interval, execute, argument):
    """
    Schedule
    """
    execute(*argument)
    SCHEDULER.enter(delay(interval), 1, schedule, (interval, execute, argument))

def delay(interval):
    """
    Delay
    """
    return interval - int(time.time()) % interval

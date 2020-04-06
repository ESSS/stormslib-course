"""
Exercise 01

Add a BHP target to an input deck
"""
from stormslib import InputDeck, Schedule, WellProductionTarget, Storms

storms = Storms('opm-docker.yml')

schedule = Schedule()
schedule.SetTimeSteps("monthly from 2015-01-31 to 2015-03-31")
schedule.SetWellTarget("2015-02-28", "PROD", WellProductionTarget.BHP, 200)

deck = InputDeck('../case/SPE1CASE1.DATA')
deck.SetSchedule(schedule)
deck.Save('tmp/exc01/SPE1CASE1-GENERATED.DATA')

storms.Run('tmp/exc01/SPE1CASE1-GENERATED.DATA')

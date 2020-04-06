"""
Exercise 02

Evaluate four BHP values (between 2000 and 2600) for PROD well
"""
import logging

import krakenlib
import numpy as np

from stormslib import InputDeck, Schedule, WellProductionTarget, Storms, ActivateLogging

ActivateLogging(logging.DEBUG)

storms = Storms('opm-docker.yml')

deck = InputDeck('../case/SPE1CASE1.DATA')
cases = []

for i, bhp in enumerate(np.linspace(2000, 2600, 4)):
    schedule = Schedule()
    schedule.SetTimeSteps("monthly from 2015-01-31 to 2015-06-30")
    schedule.SetWellTarget("2015-02-28", "PROD", WellProductionTarget.BHP, bhp)

    case_filename = f'../tmp/exc01/SPE1CASE1-{i}.DATA'
    cases.append(case_filename)
    deck.SetSchedule(schedule)
    deck.Save(case_filename)

res = storms.Run(cases)

for case_filename in cases:
    simulation = krakenlib.OpenResult(case_filename)
    time, values = simulation.GetCurve("Well", "PROD", "BHP")
    print(values[-1])
    simulation.close()

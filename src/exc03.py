"""
Exercise 03

Calculate new BHP values based on OPR values. Do it in an iterative form for MAX_ITERATIONS
"""
from contextlib import closing

import krakenlib

from stormslib import InputDeck, Schedule, WellProductionTarget, Storms

BASE_FILENAME = '../case/SPE1CASE1-2W.DATA'
MAX_ITERATIONS = 5
INITIAL_BHP = 4200

storms = Storms('opm-docker.yml')
case_idx = 0

with closing(krakenlib.Open(BASE_FILENAME)) as base_case:
    # https://realpython.com/list-comprehension-python/#using-list-comprehensions
    producer_names = [well.GetName() for well in base_case.GetWells() if well.GetType() == well.TYPE_PRODUCER]

initial_bhp_values = {}
for producer in producer_names:
    initial_bhp_values[producer] = INITIAL_BHP


def evaluate_bhps(well_bhp_values):
    global case_idx

    deck = InputDeck(BASE_FILENAME)
    schedule = Schedule()
    schedule.SetTimeSteps("monthly from 2015-01-31 to 2015-12-31")
    for well_name, bhp in well_bhp_values.items():
        schedule.SetWellTarget("2015-02-28", well_name, WellProductionTarget.BHP, bhp)

    generated_filename = f"../tmp/exc03/SPE1CASE1-2W_{case_idx:03d}.DATA"
    case_idx += 1
    deck.SetSchedule(schedule)
    deck.Save(generated_filename)
    storms.Run(generated_filename)
    results_opr_values = {}
    results_bhp_values = {}
    with closing(krakenlib.OpenResult(generated_filename)) as simulation:
        for well_name in well_bhp_values:
            times, opr = simulation.GetCurve("Well", well_name, "OPR")
            results_opr_values[well_name] = opr
            times, wpr = simulation.GetCurve("Well", well_name, "BHP")
            results_bhp_values[well_name] = wpr
    return results_opr_values, results_bhp_values


obtained_opr_values, obtained_bhp_values = evaluate_bhps(initial_bhp_values)

print(f"{'Well':6s} {'BHP':>8s}")
for well, bhp in obtained_bhp_values.items():
    print(f"{well:6s} {bhp[-1]:>8.2f}")

print(f"{'Well':6s} {'OPR':>8s}")
for well, opr_values in obtained_opr_values.items():
    print(f"{well:6s} {opr_values[-1]:>8.2f}")


def calculate_new_bhps(well_opr_values, well_bhp_values):
    new_bhp_values = {}
    print("Calculating new BHPs...")
    for well_name, opr_values in well_opr_values.items():
        current_bhp = well_bhp_values[well_name]
        new_bhp = current_bhp[-1] - current_bhp[-1] * (opr_values[-1] / opr_values[0] / 10)
        print(well_name, new_bhp)
        new_bhp_values[well_name] = new_bhp
    return new_bhp_values

# Main Loop
for i in range(MAX_ITERATIONS):
    new_bhps = calculate_new_bhps(obtained_opr_values, obtained_bhp_values)
    obtained_opr_values, obtained_bhp_values = evaluate_bhps(new_bhps)


print(f"{'Well':6s} {'BHP':>8s}")
for well, bhp in obtained_bhp_values.items():
    print(f"{well:6s} {bhp[-1]:>8.2f}")

print(f"{'Well':6s} {'OPR':>8s}")
for well, opr_values in obtained_opr_values.items():
    print(f"{well:6s} {opr_values[-1]:>8.2f}")

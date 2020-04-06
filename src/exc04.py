from stormslib import InputDeck, Schedule, WellProductionTarget, Storms

BASE_FILENAME = '../case/SPE1CASE1.DATA'

storms = Storms('opm-docker.yml')
case_idx = 0

schedule = Schedule()
schedule.SetTimeSteps("monthly from 2015-01-31 to 2015-03-31")
schedule.SetWellTarget("2015-02-28", "PROD", WellProductionTarget.BHP, 200)

generated_case1 = '../tmp/exc04/SPE1CASE1.DATA'
deck = InputDeck('../case/SPE1CASE1.DATA')
deck.SetSchedule(schedule)
deck.Save(generated_case1)

storms.Run(generated_case1)

generated_case2 = '../tmp/exc04/SPE1CASE2.DATA'
schedule.AppendTimeSteps(monthly=3)
deck.SetSchedule(schedule)
deck.SetRestart(generated_case1, 3)
deck.Save(generated_case2)


storms.Run(generated_case2)


from Utils import ScenarioReader
from Connection import rest_adapter as adapter


if __name__ == '__main__':
    scenario = ScenarioReader.get_scenario_file()
    adapter.send_scenarios(scenario)

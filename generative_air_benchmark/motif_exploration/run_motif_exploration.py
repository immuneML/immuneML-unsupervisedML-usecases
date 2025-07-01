from pathlib import Path
from immuneML.app.ImmuneMLApp import ImmuneMLApp
from immuneML.app.LigoApp import LigoApp


def main():
    app = LigoApp(specification_path=Path("simulation.yaml"), result_path=Path("simulation_output/"))
    app.run()

    app = ImmuneMLApp(specification_path=Path("specs.yaml"), result_path=Path("report_output/"))
    app.run()


if __name__ == "__main__":
    main()


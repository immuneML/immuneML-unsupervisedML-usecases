from pathlib import Path
from immuneML.app.ImmuneMLApp import ImmuneMLApp


# run training
app = ImmuneMLApp(specification_path=Path("01_train.yaml"), result_path=Path("01_train_output/"))
app.run()

# run reports
app = ImmuneMLApp(specification_path=Path("02_exploratory_analysis.yaml"), result_path=Path("02_reports_output/"))
app.run()



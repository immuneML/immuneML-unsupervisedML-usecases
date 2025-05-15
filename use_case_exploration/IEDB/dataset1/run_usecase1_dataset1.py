from pathlib import Path
from immuneML.app.ImmuneMLApp import ImmuneMLApp

# # run preprocessing
# app = ImmuneMLApp(specification_path=Path("00_preprocess.yaml"), result_path=Path("00_preprocessing_output/"))
# app.run()
#
# # run training
# app = ImmuneMLApp(specification_path=Path("01_train.yaml"), result_path=Path("01_train_output/"), logging_level="DEBUG")
# app.run()

# filter out train sequences
app = ImmuneMLApp(specification_path=Path("02_export_test_and_generated.yaml"),
                  result_path=Path("02_test_and_generated_output/"))
app.run()

# run reports
app = ImmuneMLApp(specification_path=Path("03_exploratory_analysis.yaml"), result_path=Path("03_reports_output/"))
app.run()

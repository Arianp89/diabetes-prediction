from pathlib import Path


project_root  =  Path(__file__).resolve().parent.parent
data_dir = project_root / 'data'
raw_data_dir = data_dir / 'raw'
processed_data_dir = data_dir / 'processed'
model_dir = project_root / 'models'
report_dir = project_root / 'reports'
figure_dir = report_dir / 'figures'


target_column = "Outcome"
random_state = 42
test_size = 0.2
from heart_disease_source_code.data.make_dataset import read_data, split_train_val_data
from omegaconf import OmegaConf
import pytest


def test_load_dataset(dataset_path):
    data = read_data(dataset_path)
    assert len(data) > 10
    assert "target" in data.keys()


@pytest.mark.parametrize(
    ["strategy"],
    [
        pytest.param("holdout", id="holdout"),
        pytest.param(None, id="None"),
    ]
)
def test_split_dataset(tmpdir, dataset_path, strategy):
    val_size = 0.3
    random_state = 123
    data = read_data(dataset_path)

    splitting_params = OmegaConf.create({'val_size': val_size, 'random_state': random_state})
    train, val = split_train_val_data(data, strategy, splitting_params)

    assert train.shape[0] > 5

    if strategy == 'holdout':
        assert val.shape[0] > 5
    else:
        assert val.shape[0] == 0



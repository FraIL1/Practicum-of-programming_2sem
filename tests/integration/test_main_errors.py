import pytest
from main import main


def test_no_data_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit):
        main()

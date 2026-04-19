import json
from main import main


def test_full_pipeline(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    file = data_dir / "test.csv"
    file.write_text(
        """id,amount,category,date
1,100,food,2024-01-01
2,-50,food,2024-01-01
3,abc,food,2024-01-01
"""
    )

    monkeypatch.chdir(tmp_path)

    main()

    result_file = tmp_path / "result.json"
    data = json.loads(result_file.read_text())

    assert data == {"food": 100}

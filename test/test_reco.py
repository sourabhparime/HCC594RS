# simple monkey unit tests
from flaskapp import recommender


def test_read_csv():
    dummy_str = "Place holder string"
    with open("dummy_text.csv", 'w') as f:
        f.write(dummy_str)

    df = recommender.read_csv("dummy_text.csv")
    print(df.columns)
    assert df.columns[0] == dummy_str


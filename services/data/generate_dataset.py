from pathlib import Path
import pandas as pd


def generate_dataset(output_path: str | None = None):
    output_path = Path(output_path or "uploads/sample_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=12, freq="ME"),
            "Revenue": [12000, 13500, 14000, 15500, 16000, 17000, 17500, 18200, 19000, 20500, 21500, 23000],
            "Profit": [3000, 3400, 3600, 3900, 4200, 4500, 4700, 5000, 5300, 5700, 6100, 6500],
            "Customers": [110, 115, 118, 122, 125, 130, 132, 138, 142, 148, 152, 160],
        }
    )
    df.to_csv(output_path, index=False)
    return str(output_path)


if __name__ == "__main__":
    print(generate_dataset())

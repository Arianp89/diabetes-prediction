
from src.data_loader import load_data


def main():
    data = load_data()

    print("Dataset loaded successfully!")
    print(f"Dataset shape: {data.shape}")

    print("\nFirst 5 rows:")
    print(data.head())

    print("\nColumn names:")
    print(data.columns.tolist())


if __name__ == "__main__":
    main()

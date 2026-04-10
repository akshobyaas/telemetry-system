import time
from analyzer import analyze
from data_collector import get_data
from logger import create_file, write_data


def main():
    create_file()

    print("Monitoring Started...\n")

    while True:
        data = get_data()

        result = analyze(data)

        write_data(data, result)

        print(f"{data} => {result}")

        time.sleep(2)


if __name__ == "__main__":
    main()
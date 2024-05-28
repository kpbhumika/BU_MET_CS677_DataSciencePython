def fair_cut_diamonds(filename):
    # Open the file and read all lines into diamonds_data list
    with open(filename, "r") as file:
        diamonds_data = file.readlines()

    fair_cut_diamonds = []
    total_weight = 0
    total_price = 0

    # Iterate through each line in diamonds_data
    for line in diamonds_data:
        parts = line.strip().split(",")

        # Check if the cut of the diamond is "Fair"
        if parts[2].strip() == '"Fair"':
            fair_cut_diamonds.append(line)  # Add line to fair_cut_diamonds list
            total_weight += float(parts[1].strip())  # Accumulate total weight
            total_price += float(parts[7].strip())  # Accumulate total price

    # Calculate number of fair cut diamonds
    fair_cut_diamonds_count = len(fair_cut_diamonds)

    # Calculate average weight of fair cut diamonds
    average_weight = round((total_weight / fair_cut_diamonds_count), 2)

    # Calculate average price of fair cut diamonds
    average_price = round((total_price / fair_cut_diamonds_count), 4)

    # Output results for Question 1
    print(f"2.There are {fair_cut_diamonds_count} number of Fair cut diamonds.")
    print(f"3.Average weight of Fair cut diamond is {average_weight} carat.")
    print(f"4.Average price of Fair cut diamond is ${average_price:.4f}.")


def main():
    filename = "diamonds.csv"
    fair_cut_diamonds(filename)

if __name__ == '__main__':
    main()

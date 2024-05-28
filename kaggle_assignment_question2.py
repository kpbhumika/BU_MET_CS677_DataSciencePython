def fair_cut_diamonds(filename):
    # Open the file and read all lines into diamonds_data list
    with open(filename, "r") as file:
        diamonds_data = file.readlines()

    fair_cut_diamonds = []
    total_weight = 0
    total_price = 0
    total_price_a = 0
    price_by_carat_list = []

    # Iterate through each line in diamonds_data
    for line in diamonds_data:
        parts = line.strip().split(",")

        # Check if the cut of the diamond is "Fair"
        if parts[2].strip() == '"Fair"':
            fair_cut_diamonds.append(line)  # Add line to fair_cut_diamonds list
            carat = float(parts[1].strip())
            price = float(parts[7].strip())
            price_by_carat_list.append(price/carat)
            total_price_a += price/carat
            total_weight += carat  # Accumulate total weight
            total_price += price  # Accumulate total price

    # Calculate number of fair cut diamonds
    fair_cut_diamonds_count = len(fair_cut_diamonds)

    # Calculate average price per carat using method A
    average_price_a = round((total_price_a / fair_cut_diamonds_count), 2)

    # Calculate average price per carat using method B
    average_price_b = round((total_price / total_weight), 2)

    # Output results for Question 2
    print(f"1.Average price per carat using method A  ${average_price_a:.2f}.")
    print(f"  Average price per carat using method B  ${average_price_b:.2f}.")

    # Lowest average price
    if(average_price_a < average_price_b):
        print(f"2.The lowest average price is from Method A: ${average_price_a}")
    else:
        print(f"2.The lowest average price is from Method B: ${average_price_b}")

    # Maximum price per carat
    print(f"3.Maximum price per carat is ${max(price_by_carat_list):.2f}.")

    # Minimum price per carat
    print(f"4.Minimum price per carat is ${min(price_by_carat_list):.2f}.")

    # Median price per carat
    sorted_price_data = sorted(price_by_carat_list)
    num_elements = len(sorted_price_data)
    middle_index = num_elements // 2
    if num_elements % 2 == 0:
        median = (sorted_price_data[middle_index - 1] + sorted_price_data[middle_index]) / 2
    else:
        median = sorted_price_data[middle_index]
    print(f"5.Median price per carat is ${median:.2f}.")


def main():
    filename = "diamonds.csv"
    fair_cut_diamonds(filename)

if __name__ == '__main__':
    main()

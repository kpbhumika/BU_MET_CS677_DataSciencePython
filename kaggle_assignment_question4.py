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
    print(f"Average price per carat using method A  ${average_price_a:.2f}.")
    print(f"Average price per carat using method B  ${average_price_b:.2f}.")

    # Question 4: Estimated price for a 102-carat diamond
    estimated_price_102_carat = average_price_a * 102  # Using method A for estimation

    # Print estimated price for 102-carat diamond
    print(f"Estimated price for a 102-carat diamond using method A: ${estimated_price_102_carat:.2f}")

    result = """

    Explanation:

    The estimated price calculated from my dataset for a 102-carat diamond is not close to the auction price set by Sotheby's.
    Below are the reasons:
    1. My dataset focuses exclusively on diamonds with a "Fair" cut.
    2. It's uncertain whether the price per carat increases steadily as carat size increases,
        especially since larger diamonds can be exceptionally rare.
    3. Given these uncertainties, calculating the price by multiplying the carat with the average price per carat
        from the dataset may not accurately reflect real-world prices.

    """
    print(result)

def main():
    filename = "diamonds.csv"
    fair_cut_diamonds(filename)

if __name__ == '__main__':
    main()

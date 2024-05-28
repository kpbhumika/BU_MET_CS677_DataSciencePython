def fair_cut_diamonds(filename):
    # Open the file and read all lines into diamonds_data list
    with open(filename, "r") as file:
        diamonds_data = file.readlines()

    fair_cut_diamonds = []

    # Iterate through each line in diamonds_data
    for line in diamonds_data:
        parts = line.strip().split(",")

        # Check if the cut of the diamond is "Fair"
        if parts[2].strip() == '"Fair"':
            # Create a dictionary for each diamond
            diamond = {
                "carat": float(parts[1].strip()),
                "cut": parts[2].strip().replace('"', ''),
                "color": parts[3].strip().replace('"', ''),
                "clarity": parts[4].strip().replace('"', ''),
                "depth": float(parts[5].strip()),
                "table": float(parts[6].strip()),
                "price": float(parts[7].strip()),
                "x": float(parts[8].strip()),
                "y": float(parts[9].strip()),
                "z": float(parts[10].strip())
            }
            fair_cut_diamonds.append(diamond)

    # Find max_index and min_index based on price per carat ratio
    if fair_cut_diamonds:
        max_price_value = 0
        min_price_value = float('inf')
        max_index = 0
        min_index = 0

        for idx, diamond in enumerate(fair_cut_diamonds, start=0):
            price_per_carat = diamond['price'] / diamond['carat']

            if price_per_carat > max_price_value:
                max_price_value = price_per_carat
                max_index = idx

            if price_per_carat < min_price_value:
                min_price_value = price_per_carat
                min_index = idx

        # Extract desired fields for max_index
            max_diamond = fair_cut_diamonds[max_index]
            max_diamond_fields = [
                max_diamond['color'],
                max_diamond['clarity'],
                max_diamond['depth'],
                max_diamond['table'],
                max_diamond['x'],
                max_diamond['y'],
                max_diamond['z']
            ]

        # Extract desired fields for min_index
            min_diamond = fair_cut_diamonds[min_index]
            min_diamond_fields = [
                min_diamond['color'],
                min_diamond['clarity'],
                min_diamond['depth'],
                min_diamond['table'],
                min_diamond['x'],
                min_diamond['y'],
                min_diamond['z']
            ]

        # Print results
        print(f"1. Combination of other parameters for the highest price/value are: {max_diamond_fields}")
        if min_diamond_fields:
            print(f"2. Combination of other parameters for the lowest price/value are: {min_diamond_fields}")
        else:
            print("2. No diamonds found with minimum price/value.")

    else:
        print("No diamonds found with 'Fair' cut.")

def main():
    filename = "diamonds.csv"
    fair_cut_diamonds(filename)

if __name__ == '__main__':
    main()

def besttime(prices):
    min_price = float('inf') #duong vo cung
    max_prophit = 0
    for price in prices :
        if price < min_price : min_price = price
        elif price - min_price > max_prophit: max_prophit = price - min_price
    return max_prophit
if __name__ == "__main__":
    prices = [7,1,2,3,6,1]
    print(besttime(prices))
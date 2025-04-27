from calculator import Calculator

def main():
    calc = Calculator()
    
    # Test addition
    print(f"5 + 3 = {calc.add(5, 3)}")
    
    # Test subtraction
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    
    # Test multiplication
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    
    # Test division
    try:
        print(f"20 / 5 = {calc.divide(20, 5)}")
        print(f"10 / 0 = {calc.divide(10, 0)}")  # This will raise an exception
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
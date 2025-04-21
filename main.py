class Shopkeeper:
    def __init__(self, shop_name, inventory):
        self.shop_name = shop_name
        self.inventory = inventory  # {item: {"price": float, "quantity": int}}

    def greet_customer(self):
        print(f"\nWelcome to {self.shop_name}!")
        print("How can I help you today?")

    def list_items(self):
        print("\nHere's what we have in stock:")
        for item, data in self.inventory.items():
            price = data["price"]
            quantity = data["quantity"]
            status = f"${price:.2f} - {quantity} in stock" if quantity > 0 else "OUT OF STOCK"
            print(f"- {item.title()}: {status}")

    def take_order(self):
        order = {}
        while True:
            item = input("\nEnter the item you want to buy (or type 'done' to finish): ").lower()
            if item == 'done':
                break
            if item in self.inventory:
                data = self.inventory[item]
                if data["quantity"] == 0:
                    print("Sorry, that's out of stock.")
                    continue
                try:
                    quantity = int(input(f"How many {item}s would you like? (In stock: {data['quantity']}): "))
                    if quantity <= 0:
                        print("Please enter a positive number.")
                    elif quantity > data["quantity"]:
                        print(f"Sorry, we only {data['quantity']} have in stock.")
                    else:
                        order[item] = order.get(item, 0) + quantity
                        self.inventory[item]["quantity"] -= quantity
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("We don't have that item.")
        return order

    def charge_customer(self, order, player):
        total = 0
        print("\nReceipt:")
        for item, quantity in order.items():
            price = self.inventory[item]["price"]
            subtotal = price * quantity
            total += subtotal
            print(f"{quantity} x {item.title()} ${price:.2f} = ${subtotal:.2f}")
        print(f"Total: {total:.2f}")

        if player.wallet >= total:
            player.wallet -= total
            print(f"Purchased! Remaining money: {player.wallet:.2f}")
            print("Thank's for shopping!\n")
        else:
            print("You don't have enough money.")
            # Refund the items back into inventory
            for item, quantity in order.items():
                self.inventory[item]["quantity"] += quantity

class Player:
    def __init__(self, name, wallet=100.00):
        self.name = name
        self.wallet = wallet

    def show_wallet(self):
        print(f"\n {self.name}'s Wallet: {self.wallet:.2f}")

def create_town():
    return {
        "toy store": Shopkeeper("Toy Store", {"rc car": {"price": 20, "quantity": 2}, "board game": {"price": 5.00, "quantity": 5},"toy figure": {"price": 2.50, "quantity": 10}}),

        "magic shop": Shopkeeper("Magic Shop", {"trick cards": {"price": 5.00, "quantity": 8},"magic wand": {"price": 7.50, "quantity": 3},"magic balls": {"price": 10.00, "quantity": 4}}),
        
        "video game store": Shopkeeper("Video Game Store", {"nintondo name": {"price": 25.00, "quantity": 10},"paystation Game": {"price": 25.00, "quantity": 6},"xboc game": {"price": 25.00, "quantity": 5}})
    }

def main():
    print("Welcome to the Game's and Toy's Central!")
    player_name = input("What's your name?")
    player = Player(player_name)
    town = create_town()

    while True:
        player.show_wallet()

        print("\n Shops in town:")
        for shop_key in town:
            print(f"- {shop_key.title()}")

        choice = input("\nWhich shop would you like to visit? (or type 'exit' to leave town, and type everything in lowercase with spaces): ").lower()
        if choice == 'exit':
            print(f"\n Goodbye, {player.name}!")
            break

        if choice in town:
            shop = town[choice]
            shop.greet_customer()
            shop.list_items()
            order = shop.take_order()
            if order:
                shop.charge_customer(order, player)
        else:
            print("That shop doesn't exist. Please choose a valid shop.")
if __name__ == "__main__":
    main()
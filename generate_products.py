import random

def generate_synthetic_products(count=200):
    categories = {
        "Footwear": {
            "brands": ["Nike", "Adidas", "Puma", "Reebok", "New Balance", "Asics", "Vans", "Converse", "Under Armour"],
            "adjectives": ["Pro", "Elite", "Max", "Ultra", "Zoom", "Cloud", "Boost", "Air", "Classic", "Premium"],
            "types": ["Running Shoes", "Sneakers", "Basketball Shoes", "Training Shoes", "High Tops", "Trail Runners"],
            "images": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80", # red nike
                "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&q=80", # shoe
                "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=500&q=80", # blue shoe
                "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&q=80", # air force 1
                "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&q=80"  # green nike
            ]
        },
        "Clothing": {
            "brands": ["Levi's", "The North Face", "Nike", "Adidas", "Patagonia", "Zara", "H&M", "Columbia"],
            "adjectives": ["Essential", "Tech", "Performance", "Classic", "Vintage", "Modern", "Fleece", "Lightweight"],
            "types": ["Jacket", "Hoodie", "T-Shirt", "Joggers", "Jeans", "Shorts", "Windbreaker"],
            "images": [
                "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80", # jacket
                "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&q=80", # jeans
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80", # tshirt
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80"  # hoodie
            ]
        },
        "Home Appliances": {
            "brands": ["Dyson", "Philips", "Bosch", "Samsung", "LG", "KitchenAid", "Breville", "Ninja"],
            "adjectives": ["Smart", "Pro", "Digital", "Automatic", "Compact", "Advanced", "Silent"],
            "types": ["Coffee Maker", "Air Purifier", "Vacuum Cleaner", "Blender", "Toaster Oven", "Microwave"],
            "images": [
                "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500&q=80", # blender/kitchen
                "https://images.unsplash.com/photo-1556910103-1c02745a872f?w=500&q=80", # coffee maker
                "https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?w=500&q=80" # clean kitchen
            ]
        },
        "Sports & Outdoors": {
            "brands": ["Yeti", "Coleman", "Gatorade", "Spalding", "Wilson", "CamelBak", "Hydro Flask"],
            "adjectives": ["Pro", "Heavy Duty", "Insulated", "Compact", "Lightweight", "Professional"],
            "types": ["Water Bottle", "Basketball", "Tent", "Cooler", "Yoga Mat", "Dumbbell Set"],
            "images": [
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=500&q=80", # sports gear
                "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=500&q=80", # outdoor/yoga
                "https://images.unsplash.com/photo-1603005901058-02e1afcda5fd?w=500&q=80"  # water bottle
            ]
        },
        "Beauty & Personal Care": {
            "brands": ["L'Oreal", "Neutrogena", "Clinique", "MAC", "Kiehl's", "Dior", "Chanel"],
            "adjectives": ["Hydrating", "Anti-Aging", "Radiant", "Pure", "Organic", "Essential"],
            "types": ["Face Cream", "Serum", "Perfume", "Cleanser", "Moisturizer", "Lip Balm"],
            "images": [
                "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500&q=80", # cosmetics
                "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=500&q=80", # cream
                "https://images.unsplash.com/photo-1571781526291-c477ebfd024b?w=500&q=80"  # skincare
            ]
        },
        "Books": {
            "brands": ["Penguin", "HarperCollins", "Macmillan", "Simon & Schuster", "Scholastic"],
            "adjectives": ["Bestselling", "Award-Winning", "Classic", "Modern", "Illustrated", "Essential"],
            "types": ["Novel", "Biography", "Cookbook", "History Book", "Sci-Fi Thriller", "Business Guide"],
            "images": [
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&q=80", # book
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&q=80", # open book
                "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=500&q=80"  # stacked books
            ]
        },
        "Automotive": {
            "brands": ["Michelin", "Bosch", "Meguiar's", "Rain-X", "Chemical Guys", "Armor All"],
            "adjectives": ["Premium", "Advanced", "Heavy Duty", "Pro", "Synthetic", "Ultimate"],
            "types": ["Car Wash Soap", "Wiper Blades", "Motor Oil", "Wax", "Tire Shine", "Interior Cleaner"],
            "images": [
                "https://images.unsplash.com/photo-1601362840469-51e4d8d58785?w=500&q=80", # car wash
                "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=500&q=80"  # automotive detail
            ]
        },
        "Toys & Games": {
            "brands": ["LEGO", "Hasbro", "Mattel", "Nerf", "Fisher-Price", "Hot Wheels", "Nintendo"],
            "adjectives": ["Classic", "Interactive", "Educational", "Deluxe", "Action", "Creative"],
            "types": ["Building Set", "Board Game", "Action Figure", "Puzzle", "RC Car", "Doll"],
            "images": [
                "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500&q=80", # lego
                "https://images.unsplash.com/photo-1558236714-d9a21dc33230?w=500&q=80", # toy car
                "https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?w=500&q=80"  # puzzle
            ]
        }
    }

    products = []
    
    # We want to distribute the 200 items somewhat evenly across these 8 categories
    # 200 / 8 = 25 items per category
    
    category_names = list(categories.keys())
    
    for i in range(count):
        cat = category_names[i % len(category_names)]
        c_data = categories[cat]
        
        brand = random.choice(c_data["brands"])
        adj = random.choice(c_data["adjectives"])
        ptype = random.choice(c_data["types"])
        
        name = f"{brand} {adj} {ptype}"
        price = round(random.uniform(19.99, 299.99), 2)
        
        desc = f"Experience the best with the {name}. Designed for quality and performance in the {cat} category."
        
        # specs
        specs = {
            "Brand": brand,
            "Quality": "Premium",
            "Model": adj
        }
        
        image_url = random.choice(c_data["images"])
        
        products.append({
            "name": name,
            "category": cat,
            "brand": brand,
            "price": price,
            "description": desc,
            "specifications": specs,
            "image_url": image_url
        })
        
    return products

if __name__ == "__main__":
    p = generate_synthetic_products(10)
    for x in p:
        print(x["name"], x["category"])

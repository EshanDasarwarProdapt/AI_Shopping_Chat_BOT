import json
from database import SessionLocal, init_db
from models import Product, User
from generate_products import generate_synthetic_products

def seed():
    init_db()
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Product).first():
        print("Data already seeded.")
        return

    products_data = [
        # ===== SMARTPHONES =====
        {
            "name": "iPhone 14 Pro",
            "category": "Smartphones",
            "brand": "Apple",
            "price": 999.00,
            "description": "A magical new way to interact with iPhone. Groundbreaking safety features designed to save lives. An innovative 48MP camera for mind-blowing detail.",
            "specifications": {"Screen": "6.1 inch OLED", "Storage": "256GB", "RAM": "6GB", "Battery": "3200 mAh", "Processor": "A16 Bionic"},
            "image_url": "https://images.unsplash.com/photo-1678685887225-3227620dded8?w=500&q=80"
        },
        {
            "name": "iPhone 14",
            "category": "Smartphones",
            "brand": "Apple",
            "price": 799.00,
            "description": "Awesome all day battery life. Emergency SOS via satellite. A huge leap in low-light photos.",
            "specifications": {"Screen": "6.1 inch OLED", "Storage": "128GB", "RAM": "6GB", "Battery": "3279 mAh", "Processor": "A15 Bionic"},
            "image_url": "https://images.unsplash.com/photo-1678685887225-3227620dded8?w=500&q=80"
        },
        {
            "name": "iPhone 15 Pro Max",
            "category": "Smartphones",
            "brand": "Apple",
            "price": 1199.00,
            "description": "Forged in titanium with the A17 Pro chip, a customizable Action button, and the most powerful iPhone camera system ever.",
            "specifications": {"Screen": "6.7 inch OLED", "Storage": "256GB", "RAM": "8GB", "Battery": "4422 mAh", "Processor": "A17 Pro"},
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500&q=80"
        },
        {
            "name": "Galaxy S23 Ultra",
            "category": "Smartphones",
            "brand": "Samsung",
            "price": 1199.99,
            "description": "More innovation, less footprint. Galaxy S23 Ultra's striking symmetrical design returns with recycled and eco-conscious materials.",
            "specifications": {"Screen": "6.8 inch AMOLED", "Storage": "512GB", "RAM": "12GB", "Battery": "5000 mAh", "Processor": "Snapdragon 8 Gen 2"},
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&q=80"
        },
        {
            "name": "Galaxy S24 Ultra",
            "category": "Smartphones",
            "brand": "Samsung",
            "price": 1299.99,
            "description": "Welcome to the era of mobile AI. With Galaxy AI, your phone is your interpreter, your editor, your search engine and so much more.",
            "specifications": {"Screen": "6.8 inch AMOLED", "Storage": "512GB", "RAM": "12GB", "Battery": "5000 mAh", "Processor": "Snapdragon 8 Gen 3"},
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500&q=80"
        },
        {
            "name": "Galaxy A54 5G",
            "category": "Smartphones",
            "brand": "Samsung",
            "price": 449.99,
            "description": "Awesome is for everyone. Galaxy A54 5G has a head-turning design, a long-lasting battery and an impressive camera.",
            "specifications": {"Screen": "6.4 inch AMOLED", "Storage": "128GB", "RAM": "6GB", "Battery": "5000 mAh", "Processor": "Exynos 1380"},
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351cb31b?w=500&q=80"
        },
        {
            "name": "Pixel 7 Pro",
            "category": "Smartphones",
            "brand": "Google",
            "price": 899.00,
            "description": "Google's pro-level phone. Powered by Google Tensor G2, it's fast and secure, with an immersive display and amazing battery life.",
            "specifications": {"Screen": "6.7 inch OLED", "Storage": "128GB", "RAM": "12GB", "Battery": "5000 mAh", "Processor": "Tensor G2"},
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351cb31b?w=500&q=80"
        },
        {
            "name": "Pixel 8",
            "category": "Smartphones",
            "brand": "Google",
            "price": 699.00,
            "description": "The helpful phone powered by Google AI. With the best photo quality on Pixel and 7 years of software updates.",
            "specifications": {"Screen": "6.2 inch OLED", "Storage": "128GB", "RAM": "8GB", "Battery": "4575 mAh", "Processor": "Tensor G3"},
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351cb31b?w=500&q=80"
        },
        {
            "name": "OnePlus 12",
            "category": "Smartphones",
            "brand": "OnePlus",
            "price": 799.99,
            "description": "The new OnePlus flagship brings a Hasselblad camera, 100W SUPERVOOC charging, and the latest Snapdragon processor.",
            "specifications": {"Screen": "6.82 inch AMOLED", "Storage": "256GB", "RAM": "12GB", "Battery": "5400 mAh", "Processor": "Snapdragon 8 Gen 3"},
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351cb31b?w=500&q=80"
        },

        # ===== LAPTOPS =====
        {
            "name": "MacBook Air M2",
            "category": "Laptops",
            "brand": "Apple",
            "price": 1199.00,
            "description": "Supercharged by M2. The incredibly thin and light MacBook Air features a 13.6-inch Liquid Retina display.",
            "specifications": {"Screen": "13.6 inch Retina", "Processor": "Apple M2", "RAM": "8GB", "Storage": "256GB SSD", "Battery": "18 Hours"},
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80"
        },
        {
            "name": "MacBook Pro 16 M3 Max",
            "category": "Laptops",
            "brand": "Apple",
            "price": 3499.00,
            "description": "The most powerful MacBook Pro ever. With M3 Max chip for extraordinary performance in demanding pro workflows.",
            "specifications": {"Screen": "16.2 inch Retina XDR", "Processor": "Apple M3 Max", "RAM": "36GB", "Storage": "1TB SSD", "Battery": "22 Hours"},
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80"
        },
        {
            "name": "Dell XPS 15",
            "category": "Laptops",
            "brand": "Dell",
            "price": 1749.00,
            "description": "Stunning 15.6-inch display, 13th Gen Intel Core processors and up to NVIDIA GeForce RTX 4070 graphics.",
            "specifications": {"Screen": "15.6 inch 4K OLED", "Processor": "Intel Core i7-13700H", "RAM": "16GB", "Storage": "1TB SSD", "GPU": "RTX 4070"},
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"
        },
        {
            "name": "ThinkPad X1 Carbon Gen 11",
            "category": "Laptops",
            "brand": "Lenovo",
            "price": 1649.00,
            "description": "Legendary business ultrabook. Ultra-lightweight carbon fiber construction with enterprise-grade security features.",
            "specifications": {"Screen": "14 inch 2.8K OLED", "Processor": "Intel Core i7-1365U", "RAM": "16GB", "Storage": "512GB SSD", "Weight": "1.12 kg"},
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"
        },
        {
            "name": "HP Spectre x360 14",
            "category": "Laptops",
            "brand": "HP",
            "price": 1399.99,
            "description": "A 2-in-1 laptop with gem-cut design, 360-degree hinge, and stunning 3:2 OLED display for creative professionals.",
            "specifications": {"Screen": "14 inch 3K2K OLED", "Processor": "Intel Core i7-1355U", "RAM": "16GB", "Storage": "1TB SSD", "Touch": "Yes"},
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"
        },
        {
            "name": "ASUS ROG Zephyrus G14",
            "category": "Laptops",
            "brand": "ASUS",
            "price": 1599.99,
            "description": "Compact 14-inch gaming powerhouse with AMD Ryzen 9 and NVIDIA RTX 4060 for serious gaming on the go.",
            "specifications": {"Screen": "14 inch QHD 165Hz", "Processor": "AMD Ryzen 9 7940HS", "RAM": "16GB", "Storage": "1TB SSD", "GPU": "RTX 4060"},
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"
        },
        {
            "name": "Acer Swift 5",
            "category": "Laptops",
            "brand": "Acer",
            "price": 999.99,
            "description": "Ultra-thin and lightweight laptop with antimicrobial coating. Perfect balance of performance and portability.",
            "specifications": {"Screen": "14 inch 2.5K IPS", "Processor": "Intel Core i7-1260P", "RAM": "16GB", "Storage": "512GB SSD", "Weight": "1.2 kg"},
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"
        },

        # ===== TABLETS =====
        {
            "name": "iPad Pro 12.9 M2",
            "category": "Tablets",
            "brand": "Apple",
            "price": 1099.00,
            "description": "Supercharged by the M2 chip. With a Liquid Retina XDR display, pro cameras, LiDAR, Thunderbolt, and Apple Pencil hover.",
            "specifications": {"Screen": "12.9 inch Liquid Retina XDR", "Processor": "Apple M2", "RAM": "8GB", "Storage": "128GB", "Connectivity": "Wi-Fi 6E"},
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&q=80"
        },
        {
            "name": "iPad Air M1",
            "category": "Tablets",
            "brand": "Apple",
            "price": 599.00,
            "description": "Light. Bright. Full of might. Powered by the M1 chip, the iPad Air is the perfect everyday tablet.",
            "specifications": {"Screen": "10.9 inch Liquid Retina", "Processor": "Apple M1", "RAM": "8GB", "Storage": "64GB", "Connectivity": "Wi-Fi 6"},
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&q=80"
        },
        {
            "name": "Samsung Galaxy Tab S9 Ultra",
            "category": "Tablets",
            "brand": "Samsung",
            "price": 1199.99,
            "description": "The biggest Galaxy Tab display ever. With Dynamic AMOLED 2X display, IP68 water resistance, and S Pen included.",
            "specifications": {"Screen": "14.6 inch AMOLED", "Processor": "Snapdragon 8 Gen 2", "RAM": "12GB", "Storage": "256GB", "S Pen": "Included"},
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&q=80"
        },

        # ===== AUDIO =====
        {
            "name": "Sony WH-1000XM5",
            "category": "Audio",
            "brand": "Sony",
            "price": 398.00,
            "description": "Industry Leading Noise Canceling Wireless Headphones with Auto NC Optimizer and crystal clear hands-free calling.",
            "specifications": {"Type": "Over-Ear", "Wireless": "Bluetooth 5.2", "Battery Life": "30 Hours", "ANC": "Yes", "Weight": "250g"},
            "image_url": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&q=80"
        },
        {
            "name": "AirPods Pro 2",
            "category": "Audio",
            "brand": "Apple",
            "price": 249.00,
            "description": "Rebuilt from the sound up with H2 chip. Active Noise Cancellation up to 2x more effective. Adaptive Transparency.",
            "specifications": {"Type": "In-Ear TWS", "Wireless": "Bluetooth 5.3", "Battery Life": "6 Hours (30 with case)", "ANC": "Yes", "Chip": "H2"},
            "image_url": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=500&q=80"
        },
        {
            "name": "AirPods Max",
            "category": "Audio",
            "brand": "Apple",
            "price": 549.00,
            "description": "Exquisitely crafted over-ear headphones with high-fidelity audio, Active Noise Cancellation, and spatial audio.",
            "specifications": {"Type": "Over-Ear", "Wireless": "Bluetooth 5.0", "Battery Life": "20 Hours", "ANC": "Yes", "Chip": "H1"},
            "image_url": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&q=80"
        },
        {
            "name": "Bose QuietComfort Ultra",
            "category": "Audio",
            "brand": "Bose",
            "price": 429.00,
            "description": "World-class noise cancellation with Bose Immersive Audio. Luxuriously comfortable with premium materials.",
            "specifications": {"Type": "Over-Ear", "Wireless": "Bluetooth 5.3", "Battery Life": "24 Hours", "ANC": "Yes", "Immersive Audio": "Yes"},
            "image_url": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&q=80"
        },
        {
            "name": "JBL Charge 5",
            "category": "Audio",
            "brand": "JBL",
            "price": 179.95,
            "description": "Portable Bluetooth speaker with powerful JBL Original Pro Sound, built-in powerbank, and IP67 waterproof design.",
            "specifications": {"Type": "Portable Speaker", "Wireless": "Bluetooth 5.1", "Battery Life": "20 Hours", "Waterproof": "IP67", "Power": "40W"},
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&q=80"
        },
        {
            "name": "Sony WF-1000XM5",
            "category": "Audio",
            "brand": "Sony",
            "price": 299.99,
            "description": "The best truly wireless noise canceling earbuds. Incredibly small and comfortable with world-class sound.",
            "specifications": {"Type": "In-Ear TWS", "Wireless": "Bluetooth 5.3", "Battery Life": "8 Hours (24 with case)", "ANC": "Yes", "LDAC": "Yes"},
            "image_url": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=500&q=80"
        },

        # ===== SMARTWATCHES =====
        {
            "name": "Apple Watch Ultra 2",
            "category": "Smartwatches",
            "brand": "Apple",
            "price": 799.00,
            "description": "The most rugged and capable Apple Watch ever. Titanium case, precision dual-frequency GPS, and up to 36 hours of battery.",
            "specifications": {"Display": "49mm Always-On Retina", "Chip": "S9 SiP", "Battery": "36 Hours", "Water Resistance": "100m", "Material": "Titanium"},
            "image_url": "https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=500&q=80"
        },
        {
            "name": "Apple Watch Series 9",
            "category": "Smartwatches",
            "brand": "Apple",
            "price": 399.00,
            "description": "Smarter. Brighter. Mightier. With S9 chip, double tap gesture, and the brightest Always-On display ever on Apple Watch.",
            "specifications": {"Display": "45mm Always-On Retina", "Chip": "S9 SiP", "Battery": "18 Hours", "Water Resistance": "50m", "Material": "Aluminum"},
            "image_url": "https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=500&q=80"
        },
        {
            "name": "Samsung Galaxy Watch 6 Classic",
            "category": "Smartwatches",
            "brand": "Samsung",
            "price": 429.99,
            "description": "Classic design meets modern tech. Rotating bezel, advanced health monitoring, and Wear OS by Google.",
            "specifications": {"Display": "47mm Super AMOLED", "Processor": "Exynos W930", "Battery": "425 mAh", "Water Resistance": "5ATM+IP68", "OS": "Wear OS"},
            "image_url": "https://images.unsplash.com/photo-1546868871-af0de0ae72be?w=500&q=80"
        },

        # ===== GAMING =====
        {
            "name": "PlayStation 5",
            "category": "Gaming",
            "brand": "Sony",
            "price": 499.99,
            "description": "Experience lightning-fast loading, deeper immersion with haptic feedback, adaptive triggers, and 3D Audio technology.",
            "specifications": {"Processor": "AMD Zen 2", "GPU": "AMD RDNA 2 10.28 TFLOPS", "RAM": "16GB GDDR6", "Storage": "825GB SSD", "Resolution": "4K 120fps"},
            "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500&q=80"
        },
        {
            "name": "Xbox Series X",
            "category": "Gaming",
            "brand": "Microsoft",
            "price": 499.99,
            "description": "The fastest, most powerful Xbox ever. Designed for a console generation that can deliver up to 120fps at 4K.",
            "specifications": {"Processor": "AMD Zen 2", "GPU": "AMD RDNA 2 12 TFLOPS", "RAM": "16GB GDDR6", "Storage": "1TB SSD", "Resolution": "4K 120fps"},
            "image_url": "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=500&q=80"
        },
        {
            "name": "Nintendo Switch OLED",
            "category": "Gaming",
            "brand": "Nintendo",
            "price": 349.99,
            "description": "Vibrant 7-inch OLED screen, wide adjustable stand, dock with wired LAN port, 64 GB internal storage, and enhanced audio.",
            "specifications": {"Screen": "7 inch OLED", "Storage": "64GB", "Battery Life": "4.5-9 Hours", "Modes": "TV/Tabletop/Handheld", "Resolution": "1080p (docked)"},
            "image_url": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=500&q=80"
        },
        {
            "name": "Steam Deck OLED",
            "category": "Gaming",
            "brand": "Valve",
            "price": 549.00,
            "description": "Play your Steam library on the go with a stunning 7.4 inch HDR OLED display, longer battery, and faster Wi-Fi.",
            "specifications": {"Screen": "7.4 inch HDR OLED", "Processor": "AMD APU Zen 2", "RAM": "16GB", "Storage": "512GB SSD", "Battery": "3-12 Hours"},
            "image_url": "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=500&q=80"
        },

        # ===== CAMERAS =====
        {
            "name": "Sony Alpha A7 IV",
            "category": "Cameras",
            "brand": "Sony",
            "price": 2498.00,
            "description": "Full-frame mirrorless camera with 33MP sensor, real-time Eye AF, 4K 60p video, and advanced autofocus system.",
            "specifications": {"Sensor": "33MP Full-Frame", "Video": "4K 60fps", "ISO": "100-51200", "AF Points": "759", "Weight": "658g"},
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&q=80"
        },
        {
            "name": "Canon EOS R6 Mark II",
            "category": "Cameras",
            "brand": "Canon",
            "price": 2499.00,
            "description": "24.2MP full-frame mirrorless with up to 40 fps shooting, 6K video oversampled to 4K, and next-gen autofocus.",
            "specifications": {"Sensor": "24.2MP Full-Frame", "Video": "4K 60fps / 6K RAW", "ISO": "100-102400", "AF Points": "1053", "Stabilization": "8 stops IBIS"},
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&q=80"
        },
        {
            "name": "GoPro HERO 12 Black",
            "category": "Cameras",
            "brand": "GoPro",
            "price": 399.99,
            "description": "The ultimate action camera with HyperSmooth 6.0 stabilization, 5.3K video, and improved battery life.",
            "specifications": {"Video": "5.3K 60fps", "Photo": "27MP", "Stabilization": "HyperSmooth 6.0", "Waterproof": "10m", "Battery": "Enduro"},
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&q=80"
        },

        # ===== ACCESSORIES =====
        {
            "name": "Logitech MX Master 3S",
            "category": "Accessories",
            "brand": "Logitech",
            "price": 99.99,
            "description": "Advanced wireless mouse with MagSpeed scroll, 8K DPI tracking, quiet clicks, and multi-device support.",
            "specifications": {"DPI": "8000", "Battery": "70 Days", "Connectivity": "Bluetooth + USB-C", "Buttons": "7", "Weight": "141g"},
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"
        },
        {
            "name": "Samsung T7 Shield 2TB",
            "category": "Accessories",
            "brand": "Samsung",
            "price": 189.99,
            "description": "Portable SSD with IP65 water and dust resistance, rugged design, and transfer speeds up to 1050 MB/s.",
            "specifications": {"Capacity": "2TB", "Speed": "1050 MB/s", "Interface": "USB 3.2 Gen 2", "Durability": "IP65", "Encryption": "AES 256-bit"},
            "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&q=80"
        },
        {
            "name": "Anker 737 Power Bank",
            "category": "Accessories",
            "brand": "Anker",
            "price": 109.99,
            "description": "24,000mAh portable charger with 140W output, smart digital display, and ultra-fast charging for laptops and phones.",
            "specifications": {"Capacity": "24000 mAh", "Output": "140W USB-C", "Ports": "2x USB-C, 1x USB-A", "Display": "Smart Digital", "Weight": "630g"},
            "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&q=80"
        },
        {
            "name": "Keychron Q1 Pro Keyboard",
            "category": "Accessories",
            "brand": "Keychron",
            "price": 199.00,
            "description": "Wireless custom mechanical keyboard with QMK/VIA support, gasket mount, and premium CNC aluminum body.",
            "specifications": {"Layout": "75% (84 keys)", "Switch": "Gateron Jupiter Brown", "Connectivity": "Bluetooth + USB-C", "Battery": "4000 mAh", "Hot-swap": "Yes"},
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80"
        },
        {
            "name": "Apple Magic Keyboard with Touch ID",
            "category": "Accessories",
            "brand": "Apple",
            "price": 199.00,
            "description": "Wireless keyboard with Touch ID for secure authentication, numeric keypad, and responsive low-profile keys.",
            "specifications": {"Layout": "Full Size", "Connectivity": "Bluetooth + Lightning", "Touch ID": "Yes", "Battery": "1 Month", "Compatible": "Apple Silicon Mac"},
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80"
        },

        # ===== MONITORS =====
        {
            "name": "LG UltraFine 27UN850-W",
            "category": "Monitors",
            "brand": "LG",
            "price": 449.99,
            "description": "27-inch 4K UHD IPS display with USB-C connectivity, HDR10, and 99% sRGB coverage for creative professionals.",
            "specifications": {"Size": "27 inch", "Resolution": "4K UHD 3840x2160", "Panel": "IPS", "HDR": "HDR10", "Ports": "USB-C 60W, HDMI, DP"},
            "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80"
        },
        {
            "name": "Samsung Odyssey G9",
            "category": "Monitors",
            "brand": "Samsung",
            "price": 1299.99,
            "description": "49-inch super ultrawide curved gaming monitor with Dual QHD, 240Hz, and 1ms response time.",
            "specifications": {"Size": "49 inch Curved", "Resolution": "5120x1440 Dual QHD", "Refresh Rate": "240Hz", "Response": "1ms", "Panel": "VA"},
            "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80"
        },
        {
            "name": "Dell UltraSharp U2723QE",
            "category": "Monitors",
            "brand": "Dell",
            "price": 619.99,
            "description": "27-inch 4K USB-C Hub monitor with IPS Black technology for deeper blacks and consistent color accuracy.",
            "specifications": {"Size": "27 inch", "Resolution": "4K UHD", "Panel": "IPS Black", "Color": "98% DCI-P3", "Ports": "USB-C 90W Hub"},
            "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80"
        },

        # ===== NETWORKING =====
        {
            "name": "ASUS RT-AX86U Pro",
            "category": "Networking",
            "brand": "ASUS",
            "price": 279.99,
            "description": "Wi-Fi 6 gaming router with AiMesh support, mobile game mode, and built-in security with AiProtection Pro.",
            "specifications": {"Wi-Fi": "Wi-Fi 6 AX5700", "Ports": "1x 2.5G WAN, 4x LAN", "Processor": "1.8GHz Quad-Core", "Coverage": "2500 sq ft", "Mesh": "AiMesh"},
            "image_url": "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=500&q=80"
        },
        {
            "name": "Google Nest WiFi Pro",
            "category": "Networking",
            "brand": "Google",
            "price": 199.99,
            "description": "Wi-Fi 6E mesh system with Matter smart home support. Fast, reliable coverage for the whole home.",
            "specifications": {"Wi-Fi": "Wi-Fi 6E Tri-band", "Coverage": "2200 sq ft", "Speed": "4.2 Gbps", "Smart Home": "Matter + Thread", "Devices": "100+"},
            "image_url": "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=500&q=80"
        },

        # ===== CLOTHING =====
        {
            "name": "Nike Sportswear Tech Fleece",
            "category": "Clothing",
            "brand": "Nike",
            "price": 130.00,
            "description": "Premium lightweight fleece hoodie that's smooth both inside and out.",
            "specifications": {"Material": "66% cotton/34% polyester", "Fit": "Standard", "Care": "Machine wash"},
            "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&q=80"
        },
        {
            "name": "Adidas Ultraboost 1.0",
            "category": "Footwear",
            "brand": "Adidas",
            "price": 190.00,
            "description": "High-performance running shoes featuring an adidas PRIMEKNIT upper and energy-returning BOOST midsole.",
            "specifications": {"Upper": "PRIMEKNIT", "Midsole": "BOOST", "Outsole": "Continental™ Rubber"},
            "image_url": "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=500&q=80"
        },
        {
            "name": "Levi's 501 Original Fit Jeans",
            "category": "Clothing",
            "brand": "Levi's",
            "price": 79.50,
            "description": "The original blue jean since 1873. Featuring a classic straight fit and signature button fly.",
            "specifications": {"Material": "100% Cotton", "Fit": "Straight", "Closure": "Button fly"},
            "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&q=80"
        },
        {
            "name": "The North Face Nuptse Jacket",
            "category": "Clothing",
            "brand": "The North Face",
            "price": 280.00,
            "description": "Iconic puffer jacket with original shiny ripstop fabric, oversize baffles and stowable hood.",
            "specifications": {"Insulation": "700 fill goose down", "Material": "Nylon ripstop with DWR", "Fit": "Relaxed"},
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&q=80"
        },
        {
            "name": "Nike Air Force 1 '07",
            "category": "Footwear",
            "brand": "Nike",
            "price": 110.00,
            "description": "The basketball original that puts a fresh spin on what you know best: crisp leather, bold details and the perfect amount of flash.",
            "specifications": {"Upper": "Leather", "Midsole": "Foam with Nike Air cushioning", "Outsole": "Rubber"},
            "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&q=80"
        },
    ]

    # Generate 200 more synthetic products
    synthetic_products = generate_synthetic_products(200)
    products_data.extend(synthetic_products)

    for p_data in products_data:
        product = Product(**p_data)
        db.add(product)

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Add a mock user
    user = User(
        username="demo_user",
        password_hash=pwd_context.hash("password123"),
        browsing_history=[1, 10, 20],
        purchase_history=[21, 30]
    )
    db.add(user)

    db.commit()
    db.close()
    print(f"Database seeded successfully with {len(products_data)} products.")

if __name__ == "__main__":
    seed()

import ManufacturerList
from ImageURL import ImageURL
from SpecSheetURL import SpecSheetURL
import sqlite3

# equipments = {"Equipment": ["EV Charger", "Electrical Panel", "Transformer", "Utility Meter", "AC Disconnect"],
#               "Communication Module": ["Switch", "Router", "Access Point", "Wireless Bridge", "Network Extender"],
#               "Accessory": ["Bollard", "Pedestal"]}
# equipmentSubType = {"EV Charger": ["Level 2", "Level 3"],
#                    "Electrical Panel": ["Main Breaker Pane", "Main Lug Only"],
#                    "Transformer": ["Dry-Type", "Liquid-Filled"],
#                    "Utility Meter": [],
#                    "AC Disconnect": ["Fused", "Non Fused"],
#                    "Wireless Bridge": ["Point-to-Point Bridge", "Point-to-Multipoint Bridge", "Mesh Bridge"],
#                    "Network Extender": ["WiFi Repeater", "Range Extender", "Powerline Adapter with WiFi"],
#                    "Access Point": ["Standalone Access Point", "Controller-Based Access Point", "PoE Access Point", "Dual-Band Access Point"],
#                    "Router": ["Wired Router", "Wireless Router", "Core Router", "Edge Router"],
#                    "Switch": ["Unmanaged Switch", "Managed Switch", "PoE Switch"],
#                    "Bollard": [],
#                    "Pedestal" :[]}

equipments = {"Equipment": ["EV Charger"]}
equipmentSubType = {"EV Charger": ["Level 2"]}

def debug_execute(cursor, query, description):
    try:
        cursor.execute(query)
        print(f"✅ Success: {description}")
    except sqlite3.Error as e:
        print(f"❌ Error in {description}: {e}")

print("🔌 Connecting to database...")
conn = sqlite3.connect("equipment.db")
cursor = conn.cursor()

def equipmentDBlistUpdater():
    global equipments, equipmentSubType
    conn = sqlite3.connect("equipment.db")
    cursor = conn.cursor()

    for category in equipments:
        debug_execute(cursor, f"""
            INSERT OR IGNORE INTO Categories (id, description)
            VALUES ('{category}', '{category}');
        """, f"Inserting Category: {category}")

        for equipmentType in equipments[category]:
            debug_execute(cursor, f"""
                INSERT OR IGNORE INTO EquipmentType (id, category, description)
                VALUES ('{equipmentType}', '{category}', '{equipmentType}');
            """, f"Inserting EquipmentType: {equipmentType}")

            manufacturersList = ManufacturerList.get_all_manufacturers(equipmentType)["manufacturers"]

            for manufacturer in manufacturersList:
                modelsList = ManufacturerList.get_models_by_manufacturer(
                    equipmentType, manufacturer, equipmentSubType.get(equipmentType, []))["models"]

                for subType in modelsList:
                    equipment_id = f"{equipmentType}_{manufacturer}_{subType}".replace(" ", "_")
                    debug_execute(cursor, f"""
                        INSERT OR IGNORE INTO Equipments (id, name, subtype, manufacturer_name, avail_models_count, equipmenttype)
                        VALUES ('{equipment_id}', '{manufacturer}', '{subType}', '{manufacturer}', {len(modelsList[subType])}, '{equipmentType}');
                    """, f"Inserting Equipment: {manufacturer} ({subType})")

                    for model in modelsList[subType]:
                        # Prepare data for image/spec lookup
                        data = {
                            "equipmentType": equipmentType,
                            "manufacturer": manufacturer,
                            "modelNo": model,
                            "voltageRating": ""
                        }
                        image_url = ImageURL(data).imageURLFinder() or "Not found"
                        spec_url = SpecSheetURL(data).specSheet(max_pages=3, delay=2) or "Not found"

                        model_id = f"{equipment_id}_{model}".replace(" ", "_")
                        debug_execute(cursor, f"""
                            INSERT OR IGNORE INTO Models (id, name, equipment, price, mounting_type, other_information)
                            VALUES ('{model_id}', '{model}', '{equipment_id}', NULL, NULL,
                            'ImageURL: {image_url} | SpecSheetURL: {spec_url}');
                        """, f"Inserting Model: {model}")

    conn.commit()
    conn.close()
    print("✅ Database updated successfully.")



cursor.execute("SELECT * FROM Models")
rows = cursor.fetchall()

# Print column names
columns = [description[0] for description in cursor.description]
print(" | ".join(columns))
print("-" * 80)

# Print each row
for row in rows:
    print(" | ".join(str(cell) if cell is not None else "NULL" for cell in row))

# Close the connection
conn.close()

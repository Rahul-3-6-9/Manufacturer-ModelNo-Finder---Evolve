import sqlite3

def debug_execute(cursor, query, description):
    try:
        cursor.execute(query)
        print(f"✅ Success: {description}")
    except sqlite3.Error as e:
        print(f"❌ Error in {description}: {e}")

print("🔌 Connecting to database...")
conn = sqlite3.connect("equipment.db")
cursor = conn.cursor()

debug_execute(cursor, "PRAGMA foreign_keys = ON;", "Enabling foreign key constraints")

debug_execute(cursor, """
CREATE TABLE IF NOT EXISTS Categories (
    id TEXT PRIMARY KEY,
    description TEXT
);
""", "Creating Categories table")

debug_execute(cursor, """
CREATE TABLE IF NOT EXISTS EquipmentType (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (category) REFERENCES Categories(id)
);
""", "Creating EquipmentType table")

debug_execute(cursor, """
CREATE TABLE IF NOT EXISTS Equipments (
    id TEXT PRIMARY KEY,
    name TEXT,
    subtype TEXT,
    manufacturer_name TEXT,
    avail_models_count INTEGER,
    equipmenttype TEXT NOT NULL,
    FOREIGN KEY (equipmenttype) REFERENCES EquipmentType(id)
);
""", "Creating Equipments table")

debug_execute(cursor, """
CREATE TABLE IF NOT EXISTS Models (
    id TEXT PRIMARY KEY,
    name TEXT,
    equipment TEXT NOT NULL,
    price INTEGER,
    mounting_type TEXT,
    other_information TEXT,
    FOREIGN KEY (equipment) REFERENCES Equipments(id)
);
""", "Creating Models table")

conn.commit()
conn.close()
print("✅ All tables created and connection closed.")


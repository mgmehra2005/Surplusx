from app import db
from datetime import datetime
import json
from sqlalchemy import event, inspect
from sqlalchemy.orm import attributes, PassiveFlag

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('DONOR', 'NGO', 'DELIVERY_PARTNER', 'ADMIN'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    food_listings = db.relationship('FoodListing', backref='donor', lazy=True)
    ngo_profile = db.relationship('NGO', backref='user', uselist=False)
    dp_profile = db.relationship('DeliveryPartner', backref='user', uselist=False)

    def __init__(self, username: str, name: str, email: str, phone: str, role: str, password_hash: str) -> None:
        self.username = username
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.password_hash = password_hash

class FoodListing(db.Model):
    __tablename__ = 'food_listings'
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    food_type = db.Column(db.Enum('prepared', 'raw', 'packaged', 'baked'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_unit = db.Column(db.Enum('kg', 'g', 'units', 'liters'), nullable=False)
    preparation_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime, nullable=False)
    
    # Location stored as JSON for production flexibility
    location = db.Column(db.JSON) # {latitude, longitude, address}
    status = db.Column(db.Enum('AVAILABLE', 'MATCHED', 'PICKED_UP', 'DELIVERED', 'EXPIRED'), default='AVAILABLE')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title:str, description:str, food_type:str, quantity:float, quantity_unit:str, expiry_date:datetime, location:dict) -> None:
        self.title = title
        self.description = description
        self.food_type = food_type
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.expiry_date = expiry_date
        self.location = location


class NGO(db.Model):
    __tablename__ = 'ngos'
    ngo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.JSON)
    max_capacity = db.Column(db.Integer)
    current_capacity = db.Column(db.Integer, default=0)
    food_preferences = db.Column(db.JSON) # Stores string array
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))

    def __init__(self, name:str, location:dict, max_capacity:int, food_preferences:list, contact_person:str, contact_phone:str) -> None:
        self.name = name
        self.location = location
        self.max_capacity = max_capacity
        self.food_preferences = food_preferences
        self.contact_person = contact_person
        self.contact_phone = contact_phone

class DeliveryPartner(db.Model):
    __tablename__ = 'delivery_partners'
    dp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    fullname = db.Column(db.String(100))
    address = db.Column(db.Text)
    vehicle_details = db.Column(db.JSON) # {number, license, rc}

    def __init__(self, fullname:str, address:str, vehicle_details:dict) -> None:
        self.fullname = fullname
        self.address = address
        self.vehicle_details = vehicle_details

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dp_id = db.Column(db.Integer, db.ForeignKey('delivery_partners.dp_id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_listings.fid'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.ngo_id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    pickup_time = db.Column(db.DateTime)
    delivery_time = db.Column(db.DateTime)
    time_taken = db.Column(db.String(50)) # Calculated duration
    location_pickup = db.Column(db.Text)
    location_drop = db.Column(db.Text)

    def __init__(self, dp_id:int, food_id:int, ngo_id:int, donor_id:int, pickup_time:datetime, delivery_time:datetime, location_pickup:str, location_drop:str) -> None:
        self.dp_id = dp_id
        self.food_id = food_id
        self.ngo_id = ngo_id
        self.donor_id = donor_id
        self.pickup_time = pickup_time
        self.delivery_time = delivery_time
        self.time_taken = str(delivery_time - pickup_time) if pickup_time and delivery_time else None
        self.location_pickup = location_pickup
        self.location_drop = location_drop

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(10), nullable=False) # INSERT, UPDATE, DELETE
    row_id = db.Column(db.String(36))
    # changed_data stores the actual diff (what changed from what)
    changed_data = db.Column(db.JSON) 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, table_name, action, row_id, changed_data) -> None:
        self.table_name = table_name
        self.action = action
        self.row_id = row_id
        self.changed_data = changed_data

# --- THE UNIVERSAL TRIGGER LOGIC ---
def capture_changes(mapper, connection, target):
    """
    Automatically detects which fields changed and logs them.
    """
    state = attributes.instance_state(target)
    changes = {}
    for attr in state.manager.attributes:
        history = state.get_history(attr.key, PassiveFlag.PASSIVE_OFF)
        if history.has_changes():
            # history.added contains the new value
            changes[attr.key] = str(history.added[0]) if history.added else None

    # Determine the unique ID of the row being changed
    # We check common ID names used in your schema
    inst = inspect(target)
    primary_key = ", ".join([str(x) for x in inst.identity]) if inst.identity else "unknown"
    
    # Prevent logging the log table itself (infinite loop)
    if target.__tablename__ == 'system_logs':
        return
    log = SystemLog(
        table_name=target.__tablename__,
        action="UPDATE",
        row_id=primary_key,
        changed_data=changes
    )
    # Use a new session to ensure the log is saved even if the main transaction fails
    db.session.add(log)

# This loop attaches the 'capture_changes' function to EVERY model in your app
for cls in db.Model.__subclasses__():
    tablename = getattr(cls, '__tablename__', None)
    if tablename and tablename != 'system_logs':
        event.listen(cls, 'after_update', capture_changes)
        event.listen(cls, 'after_insert', lambda m, c, t: log_event_simple(t, 'INSERT'))
        event.listen(cls, 'after_delete', lambda m, c, t: log_event_simple(t, 'DELETE'))

def log_event_simple(target, action):
    if target.__tablename__ == 'system_logs': return
    primary_key = str(getattr(target, 'uid', getattr(target, 'fid', getattr(target, 'id', 'unknown'))))
    log = SystemLog(table_name=target.__tablename__, action=action, row_id=primary_key, changed_data={"status": "event_triggered"})
    db.session.add(log)
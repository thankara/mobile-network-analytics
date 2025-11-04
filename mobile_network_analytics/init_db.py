from sqlalchemy import create_engine
from mobile_network_analytics.db import Base
from mobile_network_analytics.settings import get_db_settings
import mobile_network_analytics.models  # noqa


db_settings = get_db_settings()
engine = create_engine(db_settings.connection_string)

# Create all tables
Base.metadata.create_all(engine)
print("Tables created!")

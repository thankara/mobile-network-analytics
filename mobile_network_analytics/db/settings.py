from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    Configuration class for database settings.
    Reads the configuration from a .env file.
    """

    model_config = SettingsConfigDict(extra="ignore")

    db_name: str
    db_username: str
    db_password: str
    db_host: str
    db_port: str

    @property
    def connection_string(self) -> str:
        """
        Constructs and returns the connection string for the database.

        :return: str - The connection string.
        """
        return (
            f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}"
            f":{self.db_port}/{self.db_name}"
        )


def get_db_settings() -> DatabaseSettings:
    """
    Get database settings
    :return: DatabaseSettings
    """
    return DatabaseSettings()

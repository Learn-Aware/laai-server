from dal.mongodb_dal import MongoDBDAL
from dal.user_dal import UserDAL
from dal.health_dal import HealthDAL
from dal.conversation_dal import ConversationDAL

# Create instances of DALs for use throughout the application
user_dal = UserDAL()
health_dal = HealthDAL()
conversation_dal = ConversationDAL()

__all__ = [
    "MongoDBDAL",
    "UserDAL",
    "HealthDAL",
    "ConversationDAL",
    "user_dal",
    "health_dal",
    "conversation_dal",
] 
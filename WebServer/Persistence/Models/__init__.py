from sqlalchemy.orm import DeclarativeBase

from .Language import CODE as LENGUAGE_CODE
from .Language import DIFICULTY as LENGUAGE_DIFICULTY
from .Language import Language as Language
from .Prompt import Prompt as Prompt
from .Report import RATE as REPORT_RATE
from .Report import Report as Report
from .Subscription import TIER as SUBSCRIPTION_TIER
from .Subscription import Subscription as Subscription
from .User import Role as USER_ROLE
from .User import User as User
from .UserLanguage import PROFICIENCY_LEVELS as USER_PROFICIENCY_LEVELS
from .UserLanguage import UserLanguage as UserLanguage
from .UserMessage import UserMessage


class Base(DeclarativeBase):
    pass

from .core.security import RoleChecker
from .core.enums import RoleType


require_admin = RoleChecker([RoleType.ADMIN])

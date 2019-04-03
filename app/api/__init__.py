from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/python/report/api')

from . import team_recharge_data
from . import group_sales_data
from app.api.history_server import history_sales_server
from app.api.history_server import history_recharge_server
from app.api.same_day_service import same_day_sales
from app.api.same_day_service import same_day_recharge_server
from app.api.member_numbers_service import member_number
from app.api.userlogin_service import userLogin

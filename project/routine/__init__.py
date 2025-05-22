from flask import Blueprint


routine_bp = Blueprint('routine', __name__, template_folder='templates')
item_bp = Blueprint('item', __name__, template_folder='templates')
workout_bp = Blueprint('workout', __name__, template_folder='templates')

from .controllers import routine_controller, item_controller, workout_controller
from .models import Routine, RoutineItem
from .forms import NewRoutineForm, NewDietForm, NewWorkoutForm
from .services import RoutineService, ItemService
from .repositories import RoutineRepository, ItemRepository

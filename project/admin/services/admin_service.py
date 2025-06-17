from utils import db
from project.friendship import Friendship
from project.post import Post
from project.routine import Routine
from project.user import User


class AdminService:
    def get_overall_stats(self):
        all_routines = db.session.query(Routine).all()
        all_workouts = [r for r in all_routines if r.type == 'workout']
        all_diets = [r for r in all_routines if r.type == 'dietary']

        return {
            'total_users':db.session.query(User).count(),
            'total_posts':db.session.query(Post).count(),
            'total_friends':db.session.query(Friendship).count(),
            'total_workouts':len(all_workouts),
            'total_diets':len(all_diets),
            'diet_workout_ratio':len(all_diets)/len(all_workouts) if all_workouts else 0,
            'workout_diet_ratio':len(all_workouts)/len(all_diets) if all_diets else 0,
            'total_routines':len(all_routines),
        }


import math

from pathlib import Path

import json
from sqlalchemy.exc import SQLAlchemyError

from core import db
from project.major import Major


def populate_majors(app):
    json_path = Path(__file__).parent / 'majors.json'

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with app.app_context():
        for item in data:
            for i, field in item.items():
                if not isinstance(field, str) and math.isnan(float(field)):
                    item[i] = None

            major = Major(
                name=item['name'],
                level=item['level'],
                university=item['university'],
                uni_acronym=item['uni_acronym'],
                area_tag=item['area_tag']
            )
            found = db.session.query(Major).filter_by(
                    name=major.name,
                    level=major.level,
                    university=major.university,
                    uni_acronym=major.uni_acronym,
                    area_tag=major.area_tag
            ).first()
            if not found:
                db.session.add(major)
        try:
            db.session.commit()
            print('Majors populated.')
        except (SQLAlchemyError, TypeError, Exception) as _:
            db.session.rollback()
            print('Failed to populate Majors.')

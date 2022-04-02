import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.exc import NoResultFound

from bode.app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(80), nullable=False)

    def create(**kwargs):
        task = Task(**kwargs)

        db.session.add(task)
        db.session.commit()

        return task

    def delete(task_id):
        task = Task.query.filter_by(id=task_id).first()

        if (task==None):
            raise NoResultFound

        db.session.delete(task)
        db.session.commit()

        return task

    def __repr__(self):
        return f'<Task {self.id} \n  title="{self.title}">'

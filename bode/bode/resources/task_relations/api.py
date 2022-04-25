from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from bode.app import db
from bode.models.task import Task
from bode.models.task_relation import TaskRelation
from bode.resources.task_relations.schemas import (
    RelatedTaskSchema,
    RelationTypeRequestSchema,
    SimpleTaskRelationSchema,
    TaskRelationInputSchema,
)

blueprint = Blueprint("task-relations", "task-relations", url_prefix="/task-relations")


def map_to_related_task_schema(relation_task_pair):
    relation, task = relation_task_pair

    return {"task": task, "relation_type": relation.type, "relation_id": relation.id}


@blueprint.route("")
class TasksRelations(MethodView):
    @blueprint.arguments(TaskRelationInputSchema)
    @blueprint.response(201, SimpleTaskRelationSchema)
    def post(self, relation_data):
        try:
            return TaskRelation.create(**relation_data)
        except IntegrityError:
            abort(422, message="Relation already exists")


@blueprint.route("/<relation_id>")
class TasksRelationsById(MethodView):
    @blueprint.response(200, SimpleTaskRelationSchema)
    def delete(self, relation_id):
        return TaskRelation.delete(relation_id)


@blueprint.route("/<task_id>")
class TasksInRelationWith(MethodView):
    @blueprint.arguments(RelationTypeRequestSchema, location="query")
    @blueprint.response(200, RelatedTaskSchema(many=True))
    def get(self, relation_type_request, task_id):
        match relation_type_request:
            # TODO: all of the rest cases
            case _:
                # in this case returned are all tasks related with given
                # (from "both sides" so the result is concatenated)
                result = (
                    db.session.query(TaskRelation, Task)
                    .filter(TaskRelation.first_task_id == task_id)
                    .join(Task, TaskRelation.second_task_id == Task.id)
                    .all()
                    + db.session.query(TaskRelation, Task)
                    .filter(TaskRelation.second_task_id == task_id)
                    .join(Task, TaskRelation.first_task_id == Task.id)
                    .all()
                )

        # joined query result is a pair (relation, task) and need to be mapped to RelatedTaskSchema
        result = map(map_to_related_task_schema, result)

        return result

from bode.app import db
from bode.models.task import Task, TaskStatus
from bode.models.task_relation import RelationType, TaskRelation


def delete_task(task_id):
    """Function deletes task, all it's relations and all it's subtasks reursively."""

    def is_subtask_relation(relation):
        return relation.type == RelationType.Subtask.value and str(relation.first_task_id) == task_id

    relation_task_pairs = TaskRelation.get_related_tasks(task_id)

    for relation, related_task in relation_task_pairs:
        TaskRelation.delete(relation.id)
        if is_subtask_relation(relation):
            delete_task(str(related_task.id))

    task = Task.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return task


def edit_task(task_id, **task_data):
    """Function edit task. If task is checked, all interchangable tasks will be checked."""

    def is_interchangable_relation(relation):
        return relation.type == RelationType.Interchangable.value and str(relation.first_task_id) == task_id

    task = Task.get(task_id)

    for key, value in task_data.items():
        setattr(task, key, value)

    db.session.commit()

    if task_data["status"] != TaskStatus.TODO.value:
        for relation, related_task in TaskRelation.get_related_tasks(task_id):
            if is_interchangable_relation(relation):
                if related_task.status != TaskStatus.TODO:
                    continue
                inter_task_data = {
                    "title": related_task.title,
                    "description": related_task.description,
                    "due_date": related_task.due_date,
                    "status": TaskStatus.INDIRECTLY_DONE.value,
                }
                edit_task(str(related_task.id), **inter_task_data)

    return task

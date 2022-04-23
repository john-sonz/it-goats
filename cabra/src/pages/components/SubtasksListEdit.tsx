import {
  createRelation,
  createTask,
  getSubtasks,
  getTask,
  getTasks,
} from "../../api/tasks";
import tw, { styled } from "twin.macro";
import { useMutation, useQuery, useQueryClient } from "react-query";

import AddDependenceButton from "./AddDependenceButton";
import { FormEvent } from "react";
import { ITask } from "../../types/task";
import { ITaskRelation } from "../../types/taskRelation";
import MiniTaskDelete from "./MiniTaskDelete";

const Container = styled.div(tw`text-gray-50 w-full space-y-4`);
const fieldStyles = tw`w-full px-4 py-2 rounded-xl text-blue-800 placeholder:text-blue-800/60 font-size[small]`;

const emptyTask: Omit<ITask, "id"> = {
  description: "",
  dueDate: null,
  title: "",
  isDone: false,
};

interface Props {
  parentId: string;
}

export default function SubtasksListEdit({ parentId }: Props) {
  let subtask = "";
  const client = useQueryClient();

  const addRelation = useMutation(createRelation, {
    onSuccess: () => {
      client.invalidateQueries(getTasks.cacheKey);
      client.invalidateQueries(getTask.cacheKey(parentId));
    },
  });
  const addSubtask = useMutation(createTask, {
    onSuccess: (data) => {
      const relation: Omit<ITaskRelation, "id"> = {
        firstTaskId: parentId,
        secondTaskId: data.data.id,
        type: "SUBTASK",
      };
      addRelation.mutateAsync(relation);
    },
  });

  const handleSubmitSubtask = (event: FormEvent) => {
    event.preventDefault();
    const inputs = {
      ...emptyTask,
      title: subtask,
    };
    addSubtask.mutateAsync(inputs);
  };

  const { data, isLoading, error } = useQuery(
    getSubtasks.cacheKey(parentId),
    () => getSubtasks.run(parentId)
  );

  if (isLoading) return <Container>Loading</Container>;
  if (error) return <Container>Oops</Container>;
  if (!data?.data) return <Container />;

  const subtasks = data.data.slice().reverse();

  return (
    <div>
      <Container>
        {subtasks.map((task) => (
          <MiniTaskDelete key={task.id} title={task.title} />
        ))}
      </Container>
      <form onSubmit={handleSubmitSubtask}>
        <div tw="rounded-xl w-full text-blue-800  p-1.5">
          <p tw="flex items-center">
            <input
              css={[tw`form-input`, fieldStyles]}
              id="subtask"
              type="text"
              maxLength={80}
              required
              onChange={(event) => (subtask = event.target.value)}
            />
          </p>
          <p tw="flex items-center">
            <AddDependenceButton type="submit">+add</AddDependenceButton>
          </p>
        </div>
      </form>
    </div>
  );
}

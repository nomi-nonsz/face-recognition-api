#!/bin/bash

SESSION_NAME="recognition_service"

RUN_SESSION () {
  tmux new-session -d -s $SESSION_NAME
  tmux send-keys -t $SESSION_NAME 'cd python/ && python3 .' C-m
  tmux new-window -t $SESSION_NAME
  tmux send-keys -t $SESSION_NAME:1 'cd node/ && yarn dev' C-m
  tmux select-window -t $SESSION_NAME:0
  tmux attach -t $SESSION_NAME
}

tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? == 0 ]; then
  echo "ABORTED: session $SESSION_NAME is in use"
else
  RUN_SESSION
fi
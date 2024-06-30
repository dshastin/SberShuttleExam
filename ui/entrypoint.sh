#!/bin/sh

  if [ "$1" = 'alembic' ]; then
    shift 1
    alembic "$@"
  else
    alembic upgrade head
    sleep 2
    uvicorn main:app
  fi

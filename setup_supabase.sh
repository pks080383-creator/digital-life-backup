#!/usr/bin/env bash
# helper to run supabase migrations & functions deploy
set -e
if [ -z "$1" ]; then
  echo "Usage: setup_supabase.sh <project-ref>"
  exit 1
fi
PROJECT_REF="$1"
supabase link --project-ref ${PROJECT_REF}
supabase db push
supabase functions deploy

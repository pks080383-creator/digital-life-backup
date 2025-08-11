#!/usr/bin/env bash
set -e
echo "Bootstrapping local dev environment..."
command -v supabase >/dev/null 2>&1 || { echo >&2 "supabase CLI not found. Please install: https://supabase.com/docs/guides/cli"; exit 1; }
command -v vercel >/dev/null 2>&1 || { echo >&2 "vercel CLI not found. Please install: https://vercel.com/docs/cli"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo >&2 "docker not found. Please install Docker Desktop."; exit 1; }
echo "Logging into Supabase (you will be prompted)..."
supabase login
echo "Linking to Supabase project (provide project ref)..."
read -p "Supabase project ref: " PROJECT_REF
supabase link --project-ref ${PROJECT_REF}
echo "Applying DB migrations..."
supabase db push
echo "Done. Next: configure GitHub secrets and push to main."

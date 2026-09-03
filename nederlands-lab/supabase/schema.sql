-- Nederlands Lab — Supabase schema
--
-- Run this once in your Supabase project: SQL Editor -> New query -> paste -> Run.
-- It creates a single row per user holding that user's whole learning state and
-- locks it down so nobody can read or write anyone else's progress.

create table if not exists public.user_state (
  user_id     uuid primary key references auth.users (id) on delete cascade,
  state       jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now(),
  created_at  timestamptz not null default now()
);

comment on table public.user_state is
  'One row per learner: the full Nederlands Lab progress state (cards, flags, meta, settings).';

alter table public.user_state enable row level security;

-- Each policy is dropped first so re-running this file is safe.
drop policy if exists "read own state"   on public.user_state;
drop policy if exists "insert own state" on public.user_state;
drop policy if exists "update own state" on public.user_state;
drop policy if exists "delete own state" on public.user_state;

create policy "read own state"   on public.user_state
  for select using (auth.uid() = user_id);
create policy "insert own state" on public.user_state
  for insert with check (auth.uid() = user_id);
create policy "update own state" on public.user_state
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "delete own state" on public.user_state
  for delete using (auth.uid() = user_id);

-- Keep updated_at honest even if a client forgets to send it.
create or replace function public.touch_user_state()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists user_state_touch on public.user_state;
create trigger user_state_touch
  before update on public.user_state
  for each row execute function public.touch_user_state();

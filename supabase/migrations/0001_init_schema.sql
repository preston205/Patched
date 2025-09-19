-- 0001_init_schema.sql
-- Initial database structure for Patched on Supabase/PostgreSQL.

-- Ensure UUID generation helpers are available
create extension if not exists "pgcrypto";

-- Enumerations -------------------------------------------------------------
create type public.profile_role as enum ('artist', 'venue', 'admin');
create type public.booking_status as enum ('pending', 'confirmed', 'declined', 'completed', 'cancelled');

-- Helper function to keep updated_at fresh --------------------------------
create or replace function public.set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Core tables --------------------------------------------------------------
create table public.profiles (
    id uuid primary key references auth.users (id) on delete cascade,
    role public.profile_role not null default 'artist',
    display_name text not null,
    email text,
    phone text,
    city text,
    region text,
    country text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table public.artists (
    profile_id uuid primary key references public.profiles (id) on delete cascade,
    stage_name text,
    bio text,
    instagram_handle text,
    spotify_url text,
    website_url text,
    press_kit_url text,
    booking_contact text,
    hometown text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table public.venues (
    profile_id uuid primary key references public.profiles (id) on delete cascade,
    venue_name text not null,
    legal_name text,
    capacity integer check (capacity is null or capacity >= 0),
    address_line1 text,
    address_line2 text,
    city text,
    region text,
    postal_code text,
    country text,
    contact_email text,
    contact_phone text,
    website_url text,
    instagram_handle text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table public.genres (
    slug text primary key,
    name text not null unique,
    description text
);

create table public.artist_genres (
    artist_profile_id uuid not null references public.artists (profile_id) on delete cascade,
    genre_slug text not null references public.genres (slug) on delete cascade,
    weight integer not null default 1,
    primary key (artist_profile_id, genre_slug)
);

create table public.bookings (
    id uuid primary key default gen_random_uuid(),
    artist_profile_id uuid not null references public.artists (profile_id) on delete cascade,
    venue_profile_id uuid not null references public.venues (profile_id) on delete cascade,
    requested_by uuid references public.profiles (id) on delete set null,
    status public.booking_status not null default 'pending',
    show_date date,
    load_in_time timetz,
    notes text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- Triggers -----------------------------------------------------------------
create trigger profiles_set_updated_at
    before update on public.profiles
    for each row execute function public.set_updated_at();

create trigger artists_set_updated_at
    before update on public.artists
    for each row execute function public.set_updated_at();

create trigger venues_set_updated_at
    before update on public.venues
    for each row execute function public.set_updated_at();

create trigger bookings_set_updated_at
    before update on public.bookings
    for each row execute function public.set_updated_at();

-- Row Level Security -------------------------------------------------------
alter table public.profiles enable row level security;
alter table public.artists enable row level security;
alter table public.venues enable row level security;
alter table public.genres enable row level security;
alter table public.artist_genres enable row level security;
alter table public.bookings enable row level security;

-- Profiles policies
create policy "Public profiles are readable"
    on public.profiles for select
    using (true);

create policy "Users manage their profile"
    on public.profiles for all
    using (auth.uid() = id)
    with check (auth.uid() = id);

-- Artists policies
create policy "Artists readable"
    on public.artists for select
    using (true);

create policy "Artists manage their row"
    on public.artists for all
    using (auth.uid() = profile_id)
    with check (auth.uid() = profile_id);

-- Venues policies
create policy "Venues readable"
    on public.venues for select
    using (true);

create policy "Venues manage their row"
    on public.venues for all
    using (auth.uid() = profile_id)
    with check (auth.uid() = profile_id);

-- Genre tables: everyone can read, only admins should mutate via service role
create policy "Genres readable"
    on public.genres for select
    using (true);

-- artist_genres policies
create policy "Artist genre readable"
    on public.artist_genres for select
    using (true);

create policy "Artists manage their tags"
    on public.artist_genres for all
    using (auth.uid() = artist_profile_id)
    with check (auth.uid() = artist_profile_id);

-- Bookings policies
create policy "Participants can view bookings"
    on public.bookings for select
    using (auth.uid() = artist_profile_id or auth.uid() = venue_profile_id);

create policy "Participants manage bookings"
    on public.bookings for all
    using (auth.uid() = artist_profile_id or auth.uid() = venue_profile_id or auth.uid() = requested_by)
    with check (auth.uid() = artist_profile_id or auth.uid() = venue_profile_id or auth.uid() = requested_by);

commit;

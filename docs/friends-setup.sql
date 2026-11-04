-- Mathipelago online friends. Paste into Supabase > SQL Editor > Run (once).
-- Adds a private "mathipelago" schema plus nine mp_* functions. Touches nothing else in the project.
create schema mathipelago;
revoke all on schema mathipelago from public, anon, authenticated;

create table mathipelago.players (
  id uuid primary key default gen_random_uuid(),
  secret_hash text not null,
  code text not null unique,
  name text not null default '',
  avatar text not null default 'nimbo',
  stars int not null default 0,
  levels int not null default 0,
  pal jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table mathipelago.friendships (
  a uuid not null references mathipelago.players(id) on delete cascade,
  b uuid not null references mathipelago.players(id) on delete cascade,
  requester uuid not null,
  status text not null check (status in ('pending','accepted')),
  created_at timestamptz not null default now(),
  primary key (a, b), check (a < b)
);
create index on mathipelago.friendships (b);
create table mathipelago.cheers (
  from_id uuid not null references mathipelago.players(id) on delete cascade,
  to_id uuid not null references mathipelago.players(id) on delete cascade,
  day date not null default current_date,
  collected boolean not null default false,
  primary key (from_id, to_id, day)
);
create index on mathipelago.cheers (to_id) where not collected;
alter table mathipelago.players enable row level security;
alter table mathipelago.friendships enable row level security;
alter table mathipelago.cheers enable row level security;
revoke all on all tables in schema mathipelago from public, anon, authenticated;

create function mathipelago.who(p_id uuid, p_secret text) returns uuid
language sql stable security definer set search_path = '' as $$
  select id from mathipelago.players
  where id = p_id and length(p_secret) >= 20
    and secret_hash = encode(extensions.digest(p_secret, 'sha256'), 'hex');
$$;

create function public.mp_join(p_secret text, p_name text, p_avatar text) returns json
language plpgsql security definer set search_path = '' as $$
declare v_id uuid; v_code text; i int := 0;
begin
  if length(coalesce(p_secret,'')) < 20 or length(p_secret) > 80 then raise exception 'bad secret'; end if;
  loop
    v_code := (select string_agg(substr('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', 1 + floor(random()*32)::int, 1), '') from generate_series(1,6));
    begin
      insert into mathipelago.players(secret_hash, code, name, avatar)
      values (encode(extensions.digest(p_secret,'sha256'),'hex'), v_code,
              left(regexp_replace(coalesce(p_name,''), '[^[:alnum:] _-]', '', 'g'), 14),
              case when p_avatar ~ '^[a-z0-9_-]{1,48}$' then p_avatar else 'nimbo' end)
      returning id into v_id;
      exit;
    exception when unique_violation then
      i := i + 1; if i > 8 then raise exception 'try again'; end if;
    end;
  end loop;
  return json_build_object('id', v_id, 'code', v_code);
end $$;

create function public.mp_sync(p_id uuid, p_secret text, p_name text, p_avatar text, p_stars int, p_levels int, p_pal jsonb) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  update mathipelago.players set
    name = left(regexp_replace(coalesce(p_name,''), '[^[:alnum:] _-]', '', 'g'), 14),
    avatar = case when p_avatar ~ '^[a-z0-9_-]{1,48}$' then p_avatar else 'nimbo' end,
    stars = greatest(0, least(coalesce(p_stars,0), 100000)),
    levels = greatest(0, least(coalesce(p_levels,0), 1000)),
    pal = case when p_pal is not null and jsonb_typeof(p_pal) = 'object' and length(p_pal::text) < 500 then p_pal else null end,
    updated_at = now()
  where id = p_id;
  return true;
end $$;

create function public.mp_friends(p_id uuid, p_secret text) returns json
language plpgsql stable security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return null; end if;
  return coalesce((select json_agg(x order by x->>'rank', x->>'name') from (
    select json_build_object(
      'id', o.id, 'name', o.name, 'avatar', o.avatar, 'stars', o.stars, 'levels', o.levels, 'pal', o.pal,
      'status', case when f.status = 'accepted' then 'friend' when f.requester = p_id then 'outgoing' else 'incoming' end,
      'rank', case when f.status = 'accepted' then 'b' when f.requester = p_id then 'c' else 'a' end,
      'cheered', exists (select 1 from mathipelago.cheers c where c.from_id = p_id and c.to_id = o.id and c.day = current_date)
    ) as x
    from mathipelago.friendships f
    join mathipelago.players o on o.id = case when f.a = p_id then f.b else f.a end
    where p_id in (f.a, f.b)
  ) s), '[]'::json);
end $$;

create function public.mp_add(p_id uuid, p_secret text, p_code text) returns text
language plpgsql security definer set search_path = '' as $$
declare v_other uuid; v_a uuid; v_b uuid; v_f mathipelago.friendships;
begin
  if mathipelago.who(p_id, p_secret) is null then return 'auth'; end if;
  select id into v_other from mathipelago.players where code = upper(trim(coalesce(p_code,'')));
  if v_other is null then return 'notfound'; end if;
  if v_other = p_id then return 'self'; end if;
  if (select count(*) from mathipelago.friendships where p_id in (a, b)) >= 30 then return 'limit'; end if;
  v_a := least(p_id, v_other); v_b := greatest(p_id, v_other);
  select * into v_f from mathipelago.friendships where a = v_a and b = v_b;
  if found then
    if v_f.status = 'accepted' then return 'exists'; end if;
    if v_f.requester = p_id then return 'sent'; end if;
    update mathipelago.friendships set status = 'accepted' where a = v_a and b = v_b;
    return 'accepted';
  end if;
  insert into mathipelago.friendships(a, b, requester, status) values (v_a, v_b, p_id, 'pending');
  return 'sent';
end $$;

create function public.mp_respond(p_id uuid, p_secret text, p_friend uuid, p_accept boolean) returns boolean
language plpgsql security definer set search_path = '' as $$
declare v_a uuid := least(p_id, p_friend); v_b uuid := greatest(p_id, p_friend);
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  if p_accept then
    update mathipelago.friendships set status = 'accepted' where a = v_a and b = v_b and status = 'pending' and requester <> p_id;
  else
    delete from mathipelago.friendships where a = v_a and b = v_b and status = 'pending' and requester <> p_id;
  end if;
  return found;
end $$;

create function public.mp_remove(p_id uuid, p_secret text, p_friend uuid) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  delete from mathipelago.friendships where a = least(p_id, p_friend) and b = greatest(p_id, p_friend);
  return found;
end $$;

create function public.mp_cheer(p_id uuid, p_secret text, p_friend uuid) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  if not exists (select 1 from mathipelago.friendships where a = least(p_id, p_friend) and b = greatest(p_id, p_friend) and status = 'accepted') then return false; end if;
  insert into mathipelago.cheers(from_id, to_id) values (p_id, p_friend) on conflict do nothing;
  return found;
end $$;

create function public.mp_collect(p_id uuid, p_secret text) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  if mathipelago.who(p_id, p_secret) is null then return 0; end if;
  with c as (update mathipelago.cheers set collected = true where to_id = p_id and not collected returning 1)
  select count(*) into n from c;
  delete from mathipelago.cheers where day < current_date - 7;
  return least(n, 10);
end $$;

create function public.mp_delete_me(p_id uuid, p_secret text) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  delete from mathipelago.players where id = p_id;
  return true;
end $$;

revoke all on function mathipelago.who(uuid, text) from public, anon, authenticated;
do $$ declare f text; begin
  foreach f in array array[
    'mp_join(text,text,text)','mp_sync(uuid,text,text,text,int,int,jsonb)','mp_friends(uuid,text)','mp_add(uuid,text,text)',
    'mp_respond(uuid,text,uuid,boolean)','mp_remove(uuid,text,uuid)','mp_cheer(uuid,text,uuid)','mp_collect(uuid,text)','mp_delete_me(uuid,text)'] loop
    execute format('revoke all on function public.%s from public, anon, authenticated', f);
    execute format('grant execute on function public.%s to anon, authenticated', f);
  end loop;
end $$;

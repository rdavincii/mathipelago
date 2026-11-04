-- Run this ONCE in Supabase > SQL Editor. Adds: decline a request, remove a friend, delete my online data.
-- Safe to run again (create or replace). The rest of the friends setup is already installed.

create or replace function public.mp_respond(p_id uuid, p_secret text, p_friend uuid, p_accept boolean) returns boolean
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

create or replace function public.mp_remove(p_id uuid, p_secret text, p_friend uuid) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  delete from mathipelago.friendships where a = least(p_id, p_friend) and b = greatest(p_id, p_friend);
  return found;
end $$;

create or replace function public.mp_delete_me(p_id uuid, p_secret text) returns boolean
language plpgsql security definer set search_path = '' as $$
begin
  if mathipelago.who(p_id, p_secret) is null then return false; end if;
  delete from mathipelago.players where id = p_id;
  return true;
end $$;

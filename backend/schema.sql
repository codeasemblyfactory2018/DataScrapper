-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Products Table (The "Source of Truth" for what we track)
create table public.products (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    producer text,
    image_url text,
    ranking_score int default 0, -- 1 is best, 100 is worse. 0 means unranked.
    tags text[], -- e.g. ['wet', 'grain-free', 'monoprotein']
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Prices Table (Historical data of all scrapes)
create table public.prices (
    id uuid primary key default uuid_generate_v4(),
    product_id uuid references public.products(id) on delete cascade not null,
    shop_name text not null, -- 'Ceneo', 'Allegro', 'Zooplus'
    price numeric(10, 2) not null,
    currency text default 'PLN',
    url text, -- Deep link to the specific offer
    scraped_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Indexes for performance
create index idx_products_producer on public.products(producer);
create index idx_prices_product_id on public.prices(product_id);
create index idx_prices_scraped_at on public.prices(scraped_at);

-- 3. Helper View: Latest Best Prices per Product
-- This makes the Frontend query very simple/fast.
create or replace view public.latest_prices as
select distinct on (product_id, shop_name)
    p.id as product_id,
    p.name as product_name,
    p.producer,
    p.ranking_score,
    p.image_url,
    pr.shop_name,
    pr.price,
    pr.url as shop_url,
    pr.scraped_at
from public.products p
join public.prices pr on p.id = pr.product_id
order by product_id, shop_name, scraped_at desc;

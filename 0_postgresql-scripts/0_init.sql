CREATE TABLE IF NOT EXISTS public.sales (
  rank_game int, 
  name_game varchar(132), 
  platform varchar(4), 
  year_game varchar(4), 
  genre_game varchar(12), 
  publisher varchar(38), 
  NA_Sales decimal(4, 2), 
  EU_Sales decimal(4, 2), 
  JP_Sales decimal(4, 2), 
  Other_Sales decimal(4, 2), 
  Global_Sales decimal(4, 2), 
  load_date date
);
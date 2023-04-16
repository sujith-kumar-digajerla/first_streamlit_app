import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title('Diner app')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'] )

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruit_data(this_fruit_choice):
  streamlit.write('The user entered ', fruit_choice)
  response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  normalised_tbl = pandas.json_normalize(response.json())
  return streamlit.dataframe(normalised_tbl)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("select a fruit")
  else:
    get_fruit_data(fruit_choice)
    
except URLError as e:
  streamlit.error()

def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return  my_cur.fetchall()

if streamlit.button('Get Fruits list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  data_rows = get_fruit_list()
  my_cnx.close()
  streamlit.dataframe(data_rows)

def add_new_snow(this_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+this_fruit+"');")
    return "Thanks for adding " + this_fruit
  
add_fruit = streamlit.text_input("add your fruits:")
if streamlit.button('Add fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_func = add_new_snow(add_fruit)
  streamlit.text(insert_func)
  


import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 

#Adding a main title to page
streamlit.title("My Parents Healthy Diner")

#Adding finer details to page e.g., Header, meal options etc
streamlit.header('🥣 🥗Breakfast Menu🐔 🥑🍞')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')

#Adding a speciliased smoothie section to build your own smoothie
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple', 'Banana'])
fruits_to_show =my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New Section to display FruityVice API Response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
    streamlit.error ("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()
  
#DON'T RUN ANYTHING PAST HERE WHILE WE TROUBLESHOOT
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
# Allow the end user to add a fruit to the list 
add_my_fruit = streamlit.text_input('What fruit would you like to add to the list?','Pineapple')
streamlit.write('Thanks for adding:', add_my_fruit)

#This will not work corrrectly, but just go with it for now

my_cur.execute("Insert into fruit_load_ist values ('from streamlit')")

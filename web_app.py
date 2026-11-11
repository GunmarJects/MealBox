import streamlit as st
import requests

# 1. Page Configuration (Makes the tab look professional)
st.set_page_config(page_title="MealBot 3.0", page_icon="🍳", layout="wide")

# Custom CSS to make it look clean
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

st.title("🍳 MealBot 3.0")
st.write("Your ultimate kitchen companion. No more staring at the fridge.")

# --- SIDEBAR FOR CATEGORIES & AREAS ---
st.sidebar.header("Explore Modes")
search_mode = st.sidebar.radio("Choose a search mode:", 
    ("Search by Ingredient", "Search by Category", "Search by Country", "Surprise Me 🎲")
)

# --- SURPRISE ME ---
if search_mode == "Surprise Me 🎲":
    if st.sidebar.button("Roll the Dice 🎲"):
        with st.spinner("Finding a random meal..."):
            random_url = "https://www.themealdb.com/api/json/v1/1/random.php"
            random_data = requests.get(random_url).json()
            st.session_state['meal_details'] = random_data['meals'][0]

# --- SEARCH BY INGREDIENT ---
elif search_mode == "Search by Ingredient":
    ingredient = st.text_input("Type ONE main ingredient (e.g., chicken, rice, pasta):")
    if ingredient:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient.strip().replace(' ', '_')}"
        with st.spinner("Searching..."):
            data = requests.get(url).json()
            meals = data.get("meals")
            if meals:
                meal_names = [m['strMeal'] for m in meals]
                selected = st.selectbox("Select a meal:", meal_names)
                meal_id = next(m['idMeal'] for m in meals if m['strMeal'] == selected)
                st.session_state['meal_details'] = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}").json()['meals'][0]
            else:
                st.error("No meals found. Try another ingredient.")

# --- SEARCH BY CATEGORY ---
elif search_mode == "Search by Category":
    cats_data = requests.get("https://www.themealdb.com/api/json/v1/1/list.php?c=list").json()
    categories = [c['strCategory'] for c in cats_data['meals']]
    selected_cat = st.selectbox("Select a Category:", categories)
    
    if selected_cat:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={selected_cat}"
        with st.spinner(f"Loading {selected_cat} meals..."):
            data = requests.get(url).json()
            meals = data.get("meals")
            if meals:
                meal_names = [m['strMeal'] for m in meals]
                selected = st.selectbox("Select a meal:", meal_names)
                meal_id = next(m['idMeal'] for m in meals if m['strMeal'] == selected)
                st.session_state['meal_details'] = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}").json()['meals'][0]

# --- SEARCH BY COUNTRY (AREA) ---
elif search_mode == "Search by Country":
    areas_data = requests.get("https://www.themealdb.com/api/json/v1/1/list.php?a=list").json()
    areas = [a['strArea'] for a in areas_data['meals']]
    selected_area = st.selectbox("Select a Country/Area:", areas)
    
    if selected_area:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={selected_area}"
        with st.spinner(f"Loading {selected_area} meals..."):
            data = requests.get(url).json()
            meals = data.get("meals")
            if meals:
                meal_names = [m['strMeal'] for m in meals]
                selected = st.selectbox("Select a meal:", meal_names)
                meal_id = next(m['idMeal'] for m in meals if m['strMeal'] == selected)
                st.session_state['meal_details'] = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}").json()['meals'][0]

# --- DISPLAY THE SELECTED MEAL ---
if 'meal_details' in st.session_state:
    meal = st.session_state['meal_details']
    
    st.divider() 
    
    # Header Section with Image on the left and Details on the right
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        st.image(meal['strMealThumb'], use_container_width=True)
        
    with col_info:
        st.title(meal['strMeal'])
        st.markdown(f"**Category:** `{meal['strCategory']}` | **Origin:** `{meal['strArea']}`")
        
        youtube_link = meal.get('strYoutube')
        if youtube_link:
            st.markdown(f"### [▶️ Watch the Video Tutorial]({youtube_link})")
            
        # Tags/Instructions in Tabs
        tab1, tab2 = st.tabs(["🛒 Ingredients", "👨‍🍳 Instructions"])
        
        with tab1:
            for i in range(1, 21):
                ing = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ing and ing.strip():
                    st.markdown(f"- **{measure}** {ing}")
                    
        with tab2:
            st.write(meal['strInstructions'])

    st.divider()
    
    # Clear button
    if st.button("🔙 Search for another meal"):
        del st.session_state['meal_details']
        st.rerun()
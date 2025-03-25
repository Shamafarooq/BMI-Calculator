import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "warning"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight", "success"
    elif 25 <= bmi < 29.9:
        return "Overweight", "warning"
    else:
        return "Obese", "error"

def calculate_ideal_weight(height):
    lower_limit = round(18.5 * (height ** 2), 2)
    upper_limit = round(24.9 * (height ** 2), 2)
    return lower_limit, upper_limit

def calculate_daily_calories(weight, height, age, gender, activity_level):
    if gender == "Male":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height * 100) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height * 100) - (4.3 * age)
    
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Super active": 1.9
    }
    return round(bmr * activity_multipliers[activity_level], 2)

def main():
    st.set_page_config(page_title="Advanced BMI & Health Calculator", page_icon="📊", layout="wide")
    st.markdown("""
        <style>
            body { background-color: #f5f7fa; }
            .stButton>button {
                background-color: #007bff;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
            }
            .stNumberInput>div>input {
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Advanced BMI & Health Calculator")
    st.write("Calculate your Body Mass Index (BMI), ideal weight, and daily calorie needs!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Enter your weight (kg)", min_value=1.0, format="%.2f")
    with col2:
        height = st.number_input("Enter your height (m)", min_value=0.5, format="%.2f")
    with col3:
        age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    
    gender = st.radio("Select Gender", ("Male", "Female"))
    activity_level = st.selectbox("Select Activity Level", [
        "Sedentary", "Lightly active", "Moderately active", "Very active", "Super active"
    ])
    
    if st.button("Calculate Health Metrics"):
        if weight > 0 and height > 0 and age > 0:
            bmi = calculate_bmi(weight, height)
            category, status = get_bmi_category(bmi)
            ideal_weight_range = calculate_ideal_weight(height)
            daily_calories = calculate_daily_calories(weight, height, age, gender, activity_level)
            
            st.success(f"Your BMI is: {bmi}")
            st.markdown(f"**Category:** :{status}[{category}]")
            st.info(f"Your ideal weight range is between {ideal_weight_range[0]} kg and {ideal_weight_range[1]} kg.")
            st.success(f"Your estimated daily calorie needs: {daily_calories} kcal")
            
            # Show BMI distribution chart
            bmi_data = pd.DataFrame({
                "Category": ["Underweight", "Normal weight", "Overweight", "Obese"],
                "BMI Range": [18.5, 24.9, 29.9, 35]
            })
            fig = px.bar(bmi_data, x="Category", y="BMI Range", title="BMI Categories", color="Category", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional Advice
            if category == "Underweight":
                st.warning("Increase your calorie intake and include more protein in your diet.")
            elif category == "Overweight" or category == "Obese":
                st.warning("Incorporate more physical activities and a balanced diet into your routine.")
            else:
                st.success("Great job maintaining a healthy weight!")
        else:
            st.error("Please enter valid values.")

if __name__ == "__main__":
    main()

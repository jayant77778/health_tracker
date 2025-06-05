import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page config with icon & wide layout ---
st.set_page_config(page_title="HealthTracker", page_icon="🏃‍♂️", layout="wide")

# --- Custom CSS for theme ---
st.markdown("""
<style>
    /* Body font and background */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5f8fa;
    }
    /* Title style */
    .title {
        font-weight: 800;
        color: #0d3b66;
        margin-bottom: 0.5rem;
    }
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0d3b66;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #faa916;
        padding-bottom: 0.25rem;
    }
    /* Metric boxes styling */
    .stMetric {
        background-color: #e0f2f1 !important;
        border-radius: 12px;
        padding: 10px 15px;
        box-shadow: 0 2px 5px rgb(0 0 0 / 0.1);
    }
    /* Dataframe style override */
    .dataframe {
        border-radius: 12px;
        box-shadow: 0 3px 6px rgb(0 0 0 / 0.15);
        overflow-x: auto;
        background: white;
        padding: 15px;
    }
    /* Card style for diet plan */
    .diet-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 5px 15px rgb(0 0 0 / 0.1);
        margin-bottom: 2rem;
        transition: transform 0.2s ease-in-out;
    }
    .diet-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgb(0 0 0 / 0.15);
    }
    /* Colored badges */
    .badge {
        background-color: #faa916;
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 3px 12px;
        font-size: 0.9rem;
        margin-bottom: 10px;
        display: inline-block;
    }
    /* Icon spacing */
    .icon-img {
        margin-right: 8px;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar user profile inputs ---
st.sidebar.header("👤 Your Profile")
weight = st.sidebar.number_input("Weight (kg)", 30, 200, 70, step=1)
height = st.sidebar.number_input("Height (cm)", 100, 250, 170, step=1)
age = st.sidebar.number_input("Age", 10, 100, 25, step=1)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

# --- BMI & BMR calculations ---
bmi = weight / ((height / 100) ** 2)
if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# BMI status and targets
if bmi < 18.5:
    daily_steps_target = 7000
    water_intake = 2.5
    bmi_status = "Underweight"
elif 18.5 <= bmi <= 24.9:
    daily_steps_target = 10000
    water_intake = 3.0
    bmi_status = "Normal weight"
else:
    daily_steps_target = 12000
    water_intake = 3.5
    bmi_status = "Overweight"

# --- Header ---
st.markdown('<h1 class="title">🏃‍♂️ Personalized HealthTracker Dashboard</h1>', unsafe_allow_html=True)

# Metrics in 3 columns with spacing and background styling
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("BMI", f"{bmi:.2f}", bmi_status)
with col2:
    st.metric("BMR (cal/day)", f"{bmr:.0f}")
with col3:
    st.metric("Daily Steps Goal", f"{daily_steps_target} steps")

st.markdown("---")

# Days slider with explanation
days = st.slider("📅 How many days would you like to track?", 7, 30, 7)

# Show progress bar for input loading (animation feel)
progress = st.progress(0)
for i in range(0, 101, 20):
    progress.progress(i)
    import time; time.sleep(0.1)
progress.empty()

# --- Daily Inputs ---
steps, water, sleep = [], [], []

st.info("🔎 Please enter your daily data:")

for i in range(days):
    st.markdown(f"### Day {i+1}")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.image("https://img.icons8.com/ios-filled/50/1976d2/walking--v1.png", width=40)
        step = st.number_input(f"Steps", 0, 50000, daily_steps_target, key=f"steps_{i}")
        steps.append(step)

    with c2:
        st.image("https://img.icons8.com/ios-filled/50/0288d1/water.png", width=40)
        water_ml = st.number_input(f"Water intake (ml)", 0, 5000, int(water_intake * 1000), key=f"water_{i}")
        water.append(water_ml)

    with c3:
        st.image("https://img.icons8.com/ios-filled/50/1565c0/sleeping-in-bed.png", width=40)
        sleep_hr = st.number_input(f"Sleep hours", 0.0, 24.0, 7.0, key=f"sleep_{i}")
        sleep.append(sleep_hr)

df = pd.DataFrame({"Steps": steps, "Water (ml)": water, "Sleep (hours)": sleep})

st.markdown("---")

# --- Data Summary ---
st.markdown('<h2 class="section-header">📊 Your Health Data Summary</h2>', unsafe_allow_html=True)
st.dataframe(df.style.format({"Water (ml)": "{:.0f}", "Sleep (hours)": "{:.1f}", "Steps": "{:.0f}"}))

# --- Trends Plot ---
st.markdown('<h2 class="section-header">📈 Trends Over Days</h2>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 5))
df.plot(ax=ax, marker='o', linewidth=2, markersize=6, color=['#1976d2', '#4caf50', '#ff9800'])  # Updated colors
plt.title("Health Data Trends", fontsize=16, color='#0d3b66')
plt.xticks(range(days), [f"Day {i+1}" for i in range(days)], rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
st.pyplot(fig)


# --- Averages and Feedback ---
avg_steps = df["Steps"].mean()
avg_water = df["Water (ml)"].mean() / 1000  # liters
avg_sleep = df["Sleep (hours)"].mean()

st.markdown("---")
st.markdown('<h2 class="section-header">📝 Personalized Feedback</h2>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.write("🚶 **Steps**")
    if avg_steps < daily_steps_target:
        st.warning(f"Try to increase your steps! Target is {daily_steps_target} steps/day.")
    else:
        st.success("Great job on your steps! 🎉")

with c2:
    st.write("💧 **Water Intake**")
    if avg_water < water_intake:
        st.warning(f"Drink more water! Target is {water_intake} liters/day.")
    else:
        st.success("Good hydration level! 💧")

with c3:
    st.write("🛌 **Sleep**")
    if avg_sleep < 7:
        st.warning("Try to get at least 7 hours of sleep.")
    else:
        st.success("You have healthy sleep habits! 😴")

# --- Diet Plan Recommendations Section ---
st.markdown("---")
st.markdown('<h2 class="section-header">🥗 Detailed Full-Day Diet Plan Recommendations</h2>', unsafe_allow_html=True)

if bmi < 18.5:
    st.markdown("""
    <div class="diet-card">
        <span class="badge">Underweight</span>
        <h3>High-Calorie Nutrient-Dense Diet</h3>
        <ul>
            <li><strong>Morning:</strong> Glass of warm milk with honey and nuts, Oats porridge with fruits and seeds</li>
            <li><strong>Mid-Morning Snack:</strong> Banana smoothie with peanut butter or protein powder</li>
            <li><strong>Lunch:</strong> Brown rice or chapati with dal, paneer or chicken curry, Vegetable salad with olive oil dressing</li>
            <li><strong>Afternoon Snack:</strong> Handful of mixed nuts and dried fruits</li>
            <li><strong>Evening:</strong> Whole wheat sandwich with avocado, cheese, and veggies</li>
            <li><strong>Dinner:</strong> Quinoa or whole wheat pasta with grilled vegetables and fish or tofu, A bowl of yogurt or raita</li>
            <li><strong>Before Bed:</strong> Warm milk with turmeric or a small protein shake</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif 18.5 <= bmi <= 24.9:
    st.markdown("""
    <div class="diet-card" style="border-left: 6px solid #1976d2;">
        <span class="badge" style="background-color:#1976d2;">Normal Weight</span>
        <h3>Balanced Healthy Diet</h3>
        <ul>
            <li><strong>Morning:</strong> A glass of water with lemon, Multigrain toast with avocado and boiled eggs</li>
            <li><strong>Mid-Morning Snack:</strong> Fresh fruit or a handful of nuts</li>
            <li><strong>Lunch:</strong> Grilled chicken or tofu with brown rice and steamed vegetables, Mixed green salad</li>
            <li><strong>Afternoon Snack:</strong> Greek yogurt with honey and berries</li>
            <li><strong>Evening:</strong> Vegetable soup or sprouts salad</li>
            <li><strong>Dinner:</strong> Whole grain chapati or millet with dal and a vegetable stir fry, Small bowl of curd</li>
            <li><strong>Before Bed:</strong> Herbal tea or warm milk</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="diet-card" style="border-left: 6px solid #388e3c;">
        <span class="badge" style="background-color:#388e3c;">Overweight</span>
        <h3>Weight Loss Focused Diet</h3>
        <ul>
            <li><strong>Morning:</strong> Warm lemon water, Green smoothie (spinach, cucumber, apple, ginger)</li>
            <li><strong>Mid-Morning Snack:</strong> Fresh fruit (apple, orange) or nuts (almonds, walnuts)</li>
            <li><strong>Lunch:</strong> Grilled lean protein (chicken/fish/tofu) with quinoa or salad, Steamed or roasted vegetables</li>
            <li><strong>Afternoon Snack:</strong> Carrot and cucumber sticks or sprouts salad</li>
            <li><strong>Evening:</strong> Green tea with roasted chickpeas</li>
            <li><strong>Dinner:</strong> Mixed vegetable soup or stir fry with minimal oil, Small portion of whole grains (brown rice, millet)</li>
            <li><strong>Before Bed:</strong> Herbal tea or warm water</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Yoga & Exercise Recommendations by BMI ---
st.markdown("---")
st.markdown('<h2 class="section-header">🧘‍♂️ Yoga & Exercise Recommendations</h2>', unsafe_allow_html=True)

def yoga_exercise_by_bmi(bmi):
    # Precise ranges with specific advice for key BMI values + ranges
    if bmi < 16:
        return """
        <div class="diet-card" style="border-left: 6px solid #d32f2f;">
            <span class="badge" style="background-color:#d32f2f;">Severe Underweight</span>
            <h3>Gentle Yoga & Light Exercise</h3>
            <ul>
                <li>Focus on breathing exercises (Pranayama) to improve lung capacity.</li>
                <li>Try gentle stretching and beginner yoga poses like Child's Pose and Cat-Cow.</li>
                <li>Avoid heavy cardio; prioritize strength-building under supervision.</li>
                <li>Consult a healthcare provider before starting any intense exercise.</li>
            </ul>
        </div>
        """
    elif 16 <= bmi < 18.5:
        return """
        <div class="diet-card" style="border-left: 6px solid #f57c00;">
            <span class="badge" style="background-color:#f57c00;">Underweight</span>
            <h3>Moderate Yoga & Strength Exercises</h3>
            <ul>
                <li>Incorporate gentle yoga flows including Warrior Poses and Downward Dog.</li>
                <li>Add bodyweight strength exercises like squats and wall push-ups.</li>
                <li>Include light cardio like walking or cycling 3-4 times/week.</li>
                <li>Focus on muscle building and flexibility.</li>
            </ul>
        </div>
        """
    elif 18.5 <= bmi < 25:
        return """
        <div class="diet-card" style="border-left: 6px solid #1976d2;">
            <span class="badge" style="background-color:#1976d2;">Normal Weight</span>
            <h3>Balanced Yoga & Cardio</h3>
            <ul>
                <li>Practice Vinyasa or Hatha yoga 3-5 times per week.</li>
                <li>Incorporate moderate cardio such as jogging, swimming, or cycling.</li>
                <li>Include strength training 2-3 times a week for muscle tone.</li>
                <li>Focus on overall fitness and flexibility.</li>
            </ul>
        </div>
        """
    elif 25 <= bmi < 30:
        return """
        <div class="diet-card" style="border-left: 6px solid #388e3c;">
            <span class="badge" style="background-color:#388e3c;">Overweight</span>
            <h3>Weight Loss Focused Yoga & Exercise</h3>
            <ul>
                <li>Start with low-impact cardio: brisk walking, swimming, cycling.</li>
                <li>Incorporate yoga styles like Power Yoga or Yin Yoga for flexibility and strength.</li>
                <li>Include resistance training twice weekly.</li>
                <li>Gradually increase intensity to avoid injury.</li>
            </ul>
        </div>
        """
    elif bmi >= 30:
        return """
        <div class="diet-card" style="border-left: 6px solid #2e7d32;">
            <span class="badge" style="background-color:#2e7d32;">Obese</span>
            <h3>Careful Low-Impact Exercise & Therapeutic Yoga</h3>
            <ul>
                <li>Consult a doctor before starting any exercise routine.</li>
                <li>Focus on gentle, low-impact exercises like water aerobics or chair yoga.</li>
                <li>Practice restorative and therapeutic yoga poses to reduce stress.</li>
                <li>Work with a trainer or physiotherapist if possible.</li>
            </ul>
        </div>
        """
    else:
        return "<p>No specific recommendations available.</p>"

# Display yoga & exercise recommendations based on BMI
st.markdown(yoga_exercise_by_bmi(bmi), unsafe_allow_html=True)

st.markdown("---")

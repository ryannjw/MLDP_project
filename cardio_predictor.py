import streamlit as st
import pandas as pd
import joblib
from streamlit_extras.colored_header import colored_header

# Load model
model = joblib.load("modal_ready.pkl")

# Page Configuration
st.set_page_config(
    page_title="Cardiovascular Disease Risk Prediction",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Montserrat:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Lato', sans-serif;
    }
    .stApp {
        background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20240419/pngtree-stethoscope-with-red-heart-on-gray-background-heart-health-care-concept-image_15663980.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }        
    
    .header-text {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .card {
        background-color: rgba(255, 255, 255, 1);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 25px;
        border-left: 4px solid #e74c3c;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%);
        border-left: 4px solid #c62828;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
        border-left: 4px solid #2e7d32;
    }
    
    .stSlider > div > div > div > div {
        background: #e74c3c !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s;
        width: 100%;
        margin-top: 15px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(231, 76, 60, 0.25);
    }
    
    .disclaimer {
        font-size: 0.85rem;
        color: #7f8c8d;
        text-align: center;
        margin-top: 30px;
        border-top: 1px solid #ecf0f1;
        padding-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
colored_header(
    label="🫀  Cardiovascular Disease Risk Prediction",
    description="Predict your cardiovascular disease risk",
    color_name="red-70"
)

st.markdown("""
<div class="disclaimer">
    This tool provides a preliminary risk assessment only.
</div>
""", unsafe_allow_html=True)

# Medical Credibility Section
with st.expander("🔬 Clinical Basis of This Assessment"):
    st.markdown("""
    This predictive model utilizes established clinical parameters validated by cardiovascular research:
    
    - **Blood Pressure Parameters**: Based on AHA hypertension guidelines
    - **Cholesterol/Glucose Levels**: Using ATP III classification standards
    - **BMI Calculation**: Derived from height/weight inputs
    - **Lifestyle Factors**: Smoking/alcohol risks aligned with WHO recommendations
    
    """)

# Input Form in Card Layout
with st.container():
    
    with st.form("cardio_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Biometric Data")
            age = st.slider("Age (years)", 20, 80, 50, help="Cardiovascular risk increases significantly after 50")
            height = st.slider("Height (cm)", 140, 210, 170)
            weight = st.slider("Weight (kg)", 40, 150, 70)
            
            st.subheader("Blood Pressure")
            col_bp1, col_bp2 = st.columns(2)
            with col_bp1:
                ap_hi = st.number_input("Systolic (mmHg)", 80, 200, 120,help="Normal: <120 mmHg")
            with col_bp2:
                ap_lo = st.number_input("Diastolic (mmHg)", 50, 150, 80, help="Normal: <80 mmHg")
        
        with col2:
            st.subheader("Clinical Markers")
            gender = st.selectbox("Gender", ["Male", "Female"])
            cholesterol = st.selectbox("Cholesterol Level", ["Normal", "Above Normal", "Well Above Normal"])
            glucose = st.selectbox("Glucose Level", ["Normal", "Above Normal", "Well Above Normal"])
            
            st.subheader("Lifestyle Factors")
            smoke = st.radio("Smoking Status", ["No", "Yes"], horizontal=True,help="Smoking increases risk by 2-4x")
            alco = st.radio("Alcohol Consumption", ["No", "Yes"], horizontal=True,help="Heavy drinking increases risk")
            active = st.radio("Physical Activity", ["Yes", "No"], horizontal=True,help="150+ mins/week ")
        
        submitted = st.form_submit_button("🔍 Assess Cardiovascular Risk")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction Logic
if submitted:
    # Encode inputs
    gender_val = 1 if gender == "Male" else 2
    chol_val = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}[cholesterol]
    gluc_val = {"Normal": 1, "Above Normal": 2, "Well Above Normal": 3}[glucose]
    smoke_val = 1 if smoke == "Yes" else 0
    alco_val = 1 if alco == "Yes" else 0
    active_val = 1 if active == "Yes" else 0
    
    # Calculate BMI
    bmi = weight / ((height/100) ** 2)
    
    # Create input DataFrame
    input_df = pd.DataFrame([[
        gender_val, height, weight, ap_hi, ap_lo,
        chol_val, gluc_val, smoke_val, alco_val, active_val, age
    ]], columns=[
        "gender", "height", "weight", "ap_hi", "ap_lo",
        "cholesterol", "gluc", "smoke", "alco", "active", "age_years"
    ])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][prediction]
    
    # Display results with enhanced visualization
    st.markdown(f'<div class="card {"risk-high" if prediction == 1 else "risk-low"}">', 
                unsafe_allow_html=True)
    
    if prediction == 1:
        # list for saving risk factors
        risk_factors = []
        if age >= 45:
            risk_factors.append("Age ≥45")
        if bmi >= 30:
            risk_factors.append("BMI ≥30")
        if ap_hi >= 140 or ap_lo >= 90:
            risk_factors.append("Hypertension")
        if smoke_val == 1:
            risk_factors.append("Tobacco use")
        
        risk_message = """
        ## ⚠️ Elevated Cardiovascular Risk
        **Clinical Assessment Prediction**: High probability of cardiovascular disease
        """
        
        if risk_factors:
            risk_message += "\n### Risk Factors Identified:"
            for factor in risk_factors:
                risk_message += f"\n- {factor}"
        else:
            risk_message += "\n### No significant risk factors identified"
        
        risk_message += f"\n\n**Confidence Level**: {prob:.1%}"
        st.error(risk_message)
        
        st.progress(float(prob))
        st.warning("**Clinical Recommendation**: Consult a cardiologist immediately. Consider lifestyle modifications and diagnostic testing.")
    else:
        # list for saving risk factors
        protective_factors = []
        if active_val == 1:
            protective_factors.append("Physical activity")
        if smoke_val == 0:
            protective_factors.append("Non-smoker")
        if bmi < 25:
            protective_factors.append("Healthy weight")
        
        success_message = """
        ## ✅ Low Cardiovascular Risk
        **Clinical Assessment Prediction**: No significant risk factors detected
        """
        
        if protective_factors:
            success_message += "\n### Protective Factors:"
            for factor in protective_factors:
                success_message += f"\n- {factor}"
        else:
            success_message += "\n### No significant protective factors identified"
        
        success_message += f"\n\n**Confidence Level**: {prob:.1%}"
        st.success(success_message)
        
        st.progress(float(prob))
        st.info("**Health Maintenance**: Continue preventive care. Annual screenings recommended.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional health metrics
    with st.expander("📊 Health Metrics Analysis"):
        bmi_status = "Obese" if bmi >= 30 else "Overweight" if bmi >= 25 else "Normal"
        bp_status = "Hypertensive" if ap_hi >= 140 or ap_lo >= 90 else "Normal"
        
        st.metric("BMI", f"{bmi:.1f}", bmi_status)
        st.metric("Blood Pressure", f"{ap_hi}/{ap_lo} mmHg", bp_status)
        st.metric("Age Risk Factor", "Elevated" if age >= 45 else "Normal")
        st.metric("Lifestyle Risk", "Elevated" if smoke_val or alco_val or not active_val else "Optimal")


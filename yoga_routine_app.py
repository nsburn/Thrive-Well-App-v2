import streamlit as st
import random
from datetime import datetime

# Yoga pose database
POSES = {
    "beginner": {
        "warm_up": [
            {"name": "Cat-Cow Stretch", "duration": "1 min", "benefits": "Spine mobility"},
            {"name": "Child's Pose", "duration": "1 min", "benefits": "Relaxation, hip opener"},
            {"name": "Neck Rolls", "duration": "30 sec", "benefits": "Release neck tension"}
        ],
        "standing": [
            {"name": "Mountain Pose", "duration": "1 min", "benefits": "Grounding, posture"},
            {"name": "Standing Forward Fold", "duration": "1 min", "benefits": "Hamstring stretch"},
            {"name": "Warrior I", "duration": "1 min each side", "benefits": "Strength, balance"}
        ],
        "floor": [
            {"name": "Cobra Pose", "duration": "45 sec", "benefits": "Back strength"},
            {"name": "Bridge Pose", "duration": "1 min", "benefits": "Glutes, spine"},
            {"name": "Supine Twist", "duration": "1 min each side", "benefits": "Spine mobility"}
        ],
        "cooldown": [
            {"name": "Legs Up the Wall", "duration": "2 min", "benefits": "Circulation, relaxation"},
            {"name": "Corpse Pose", "duration": "3 min", "benefits": "Deep relaxation"}
        ]
    },
    "intermediate": {
        "warm_up": [
            {"name": "Sun Salutation A", "duration": "3 rounds", "benefits": "Full body warm-up"},
            {"name": "Downward Dog", "duration": "1 min", "benefits": "Shoulder, hamstring stretch"}
        ],
        "standing": [
            {"name": "Warrior II", "duration": "1 min each side", "benefits": "Hip opener, strength"},
            {"name": "Triangle Pose", "duration": "1 min each side", "benefits": "Side body stretch"},
            {"name": "Tree Pose", "duration": "1 min each side", "benefits": "Balance, focus"}
        ],
        "floor": [
            {"name": "Boat Pose", "duration": "45 sec", "benefits": "Core strength"},
            {"name": "Pigeon Pose", "duration": "2 min each side", "benefits": "Hip flexibility"},
            {"name": "Seated Forward Fold", "duration": "2 min", "benefits": "Hamstrings, calm"}
        ],
        "cooldown": [
            {"name": "Reclined Butterfly", "duration": "2 min", "benefits": "Hip opener"},
            {"name": "Corpse Pose", "duration": "5 min", "benefits": "Integration, rest"}
        ]
    },
    "advanced": {
        "warm_up": [
            {"name": "Sun Salutation B", "duration": "5 rounds", "benefits": "Dynamic warm-up"},
            {"name": "Three-Legged Dog", "duration": "30 sec each side", "benefits": "Hip mobility"}
        ],
        "standing": [
            {"name": "Warrior III", "duration": "1 min each side", "benefits": "Balance, core"},
            {"name": "Half Moon Pose", "duration": "1 min each side", "benefits": "Balance, strength"},
            {"name": "Eagle Pose", "duration": "1 min each side", "benefits": "Focus, hip/shoulder"}
        ],
        "floor": [
            {"name": "Wheel Pose", "duration": "45 sec, 2 rounds", "benefits": "Full back bend"},
            {"name": "Crow Pose", "duration": "30 sec, 3 attempts", "benefits": "Arm balance"},
            {"name": "King Pigeon", "duration": "2 min each side", "benefits": "Deep hip opener"}
        ],
        "cooldown": [
            {"name": "Shoulderstand", "duration": "2 min", "benefits": "Inversions, thyroid"},
            {"name": "Corpse Pose", "duration": "5-10 min", "benefits": "Deep integration"}
        ]
    }
}

FOCUS_AREAS = {
    "flexibility": ["Standing Forward Fold", "Pigeon Pose", "Seated Forward Fold", "King Pigeon", "Supine Twist"],
    "strength": ["Warrior I", "Warrior II", "Warrior III", "Boat Pose", "Crow Pose", "Bridge Pose"],
    "balance": ["Tree Pose", "Warrior III", "Half Moon Pose", "Eagle Pose"],
    "relaxation": ["Child's Pose", "Legs Up the Wall", "Corpse Pose", "Reclined Butterfly"]
}

# App configuration
st.set_page_config(page_title="Yoga Routine Generator", page_icon="🧘", layout="centered")

# Header
st.title("🧘 Personalized Yoga Routine")
st.markdown("*Generate a custom yoga practice for your home routine*")

# Sidebar inputs
st.sidebar.header("Customize Your Practice")

level = st.sidebar.selectbox(
    "Experience Level",
    ["beginner", "intermediate", "advanced"],
    format_func=lambda x: x.capitalize()
)

duration = st.sidebar.slider("Practice Duration (minutes)", 10, 60, 30, 5)

focus = st.sidebar.multiselect(
    "Focus Areas (optional)",
    ["flexibility", "strength", "balance", "relaxation"],
    default=[]
)

time_of_day = st.sidebar.radio(
    "Time of Day",
    ["Morning", "Midday", "Evening"]
)

# Generate button
if st.sidebar.button("Generate Routine", type="primary"):
    st.session_state.routine_generated = True
    st.session_state.timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

# Display routine
if st.session_state.get('routine_generated', False):
    st.markdown(f"### Your Routine for {time_of_day}")
    st.caption(f"Generated on {st.session_state.timestamp}")
    
    # Calculate time allocation
    poses_data = POSES[level]
    total_sections = 4  # warm_up, standing, floor, cooldown
    time_per_section = duration / total_sections
    
    # Add time-of-day specific note
    if time_of_day == "Morning":
        st.info("☀️ Morning practice: Focus on energizing poses and gentle stretches to wake up the body")
    elif time_of_day == "Evening":
        st.info("🌙 Evening practice: Emphasize relaxation and gentle movements to wind down")
    else:
        st.info("🌤️ Midday practice: Balance energy with grounding poses")
    
    # Generate routine sections
    for section_name, section_poses in poses_data.items():
        st.markdown(f"#### {section_name.replace('_', ' ').title()}")
        
        # Select poses based on focus areas
        if focus:
            # Filter poses that match focus areas
            focused_poses = [p for p in section_poses if any(p["name"] in FOCUS_AREAS[f] for f in focus)]
            selected_poses = focused_poses if focused_poses else section_poses
        else:
            selected_poses = section_poses
        
        # Randomly select 2-3 poses per section
        num_poses = min(len(selected_poses), 2 if duration < 25 else 3)
        chosen_poses = random.sample(selected_poses, num_poses)
        
        for pose in chosen_poses:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{pose['name']}**")
                st.caption(f"Benefits: {pose['benefits']}")
            with col2:
                st.markdown(f"*{pose['duration']}*")
        
        st.markdown("---")
    
    # Summary
    st.success(f"✨ Total Practice Time: ~{duration} minutes")
    
    # Tips section
    with st.expander("💡 Practice Tips"):
        st.markdown("""
        - **Breathe deeply** through your nose throughout the practice
        - **Listen to your body** and modify poses as needed
        - **Use props** like blocks, straps, or blankets for support
        - **Stay hydrated** before and after practice
        - **Create space** with minimal distractions
        """)
    
    # Download option
    st.download_button(
        label="📄 Download Routine as Text",
        data=f"Yoga Routine - {level.capitalize()} - {duration} min\nGenerated: {st.session_state.timestamp}\n\n" +
             "\n".join([f"{s.replace('_', ' ').title()}: " + ", ".join([p['name'] for p in POSES[level][s]]) 
                       for s in poses_data.keys()]),
        file_name=f"yoga_routine_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

else:
    st.info("👈 Customize your practice in the sidebar and click 'Generate Routine' to begin")
    
    # Feature showcase
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Features")
        st.markdown("""
        - 3 difficulty levels
        - Custom duration
        - Focus area targeting
        - Time-of-day optimization
        """)
    with col2:
        st.markdown("### 🌟 Benefits")
        st.markdown("""
        - Daily variety
        - Personalized flow
        - Balanced practice
        - Easy to follow
        """)
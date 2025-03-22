import streamlit as st
import time
from datetime import datetime

# Responsive CSS with media queries
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

body {
  background-color: #1a1a1a;
  color: #fff;
  margin: 0;
  padding: 0;
}

.header {
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-size: 2.5rem;
  margin: 1rem 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  line-height: 1.2;
}

.subheader {
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-size: 1.2rem;
  margin: 1rem 0 2rem;
  color: #cccccc;
  padding: 0 1rem;
  line-height: 1.4;
}

.timer {
  text-align: center;
  font-family: 'Courier New', monospace;
  font-size: 3.5rem;
  margin: 2rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.flip-container {
  display: inline-flex;
  perspective: 1000px;
}

.flip-card {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 1.5rem;
  background: linear-gradient(145deg, #3a3a3a, #4a4a4a);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  transform-style: preserve-3d;
  animation: flip 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  color: #ffffff;
  min-width: 4.5rem;
  margin: 0.25rem;
}

.colon {
  color: #ff6b6b;
  font-weight: bold;
  transform: translateY(-2px);
  font-size: 0.8em;
}

@keyframes flip {
  0% { transform: rotateX(0deg); }
  50% { transform: rotateX(90deg); }
  100% { transform: rotateX(0deg); }
}

/* Mobile Responsive Adjustments */
@media (max-width: 768px) {
  .header {
    font-size: 2rem;
    padding: 0 1rem;
  }
  
  .subheader {
    font-size: 1rem;
    margin: 0.5rem 0 1.5rem;
  }
  
  .timer {
    font-size: 2.5rem;
    gap: 0.25rem;
  }
  
  .flip-card {
    padding: 0.75rem 1rem;
    min-width: 3.5rem;
    font-size: 0.9em;
  }
  
  .colon {
    font-size: 0.7em;
  }
}

@media (max-width: 480px) {
  .header {
    font-size: 1.75rem;
  }
  
  .subheader {
    font-size: 0.9rem;
  }
  
  .timer {
    font-size: 2rem;
  }
  
  .flip-card {
    padding: 0.5rem 0.75rem;
    min-width: 3rem;
    font-size: 0.8em;
  }
}
</style>
"""

# Inject CSS into the app
st.markdown(css, unsafe_allow_html=True)

# Header for the countdown app
st.markdown("<div class='header'> 🎉 Dare's Sent Forth Countdown 🎉</div>", unsafe_allow_html=True)

# Target datetime
target_datetime = datetime(2025, 3, 13, 16, 00, 00)
st.markdown(f"<div class='subheader'>Countdown to: {target_datetime.strftime('%B %d, %Y at %H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='venue' style='text-align: center; font-family: "Inter", sans-serif; font-size: 1.2rem; margin: 0.5rem 0 1.5rem; color: #cccccc;'>
     🏢 Venue: The Kulture Yard <br>
     📍 Address: 2b Abba Johnson Crescent, Adeniyi Jones, Ikeja, Nigeria 
    </div>
    """, 
    unsafe_allow_html=True
)


# Create a placeholder for the countdown display
timer_placeholder = st.empty()

# Automatically start the countdown
while True:
    now = datetime.now()
    remaining = target_datetime - now

    if remaining.total_seconds() <= 0:
        timer_placeholder.markdown("""
            <div class='timer'>
                <div class='flip-container'>
                    <div class='flip-card'>00</div>
                </div>
                <div class='colon'>:</div>
                <div class='flip-container'>
                    <div class='flip-card'>00</div>
                </div>
                <div class='colon'>:</div>
                <div class='flip-container'>
                    <div class='flip-card'>00</div>
                </div>
            </div>
            <div style='text-align: center; font-size: 2em; margin-top: 20px;'>
                🎉 Time's up! 🎉
            </div>
        """, unsafe_allow_html=True)
        break

    total_seconds = int(remaining.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    countdown_html = f"""
    <div class='timer'>
        <div class='flip-container'>
            <div class='flip-card'>{hours:02d}</div>
        </div>
        <div class='colon'>:</div>
        <div class='flip-container'>
            <div class='flip-card'>{minutes:02d}</div>
        </div>
        <div class='colon'>:</div>
        <div class='flip-container'>
            <div class='flip-card'>{seconds:02d}</div>
        </div>
    </div>
    """
    
    timer_placeholder.markdown(countdown_html, unsafe_allow_html=True)
    time.sleep(1)

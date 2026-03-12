# 🛰️ Orbital Conjunction Tracker

A real-time Space Situational Awareness (SSA) tool that identifies potential collision risks between active satellites.

## 🚀 Live Demo
https://debris-dashboard.streamlit.app

## 🛠️ Technical Highlights
* **Live Data Pipeline:** Fetches real-time Two-Line Element (TLE) data from CelesTrak APIs.
* **Physics Engine:** Propagates orbital positions using the **SGP4 model** via the Skyfield library.
* **Risk Logic:** Implements a 3D Euclidean distance calculation engine to detect conjunctions (near-misses).
* **Performance Optimization:** Managed $O(N^2)$ computational complexity and browser-side rendering constraints using DataFrame slicing and Streamlit caching.

## 📦 Installation
1. `pip install streamlit skyfield pandas folium streamlit-folium`
2. `streamlit run app.py`

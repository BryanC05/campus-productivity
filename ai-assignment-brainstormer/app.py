"""
AI Assignment Brainstormer - Streamlit App
Helps Indonesian university students generate assignment outlines, code snippets, and essay structures.
Powered by Kimi K2 via Ollama Cloud
"""

import streamlit as st
from database import init_db, save_prompt, get_prompt_history
from kimi_api import generate_content
from file_processor import process_uploaded_file

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="AI Assignment Brainstormer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme toggle in session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

# Theme colors based on mode
if st.session_state.dark_mode:
    # DARK MODE: CSS Overrides needed
    bg_color = "#0e1117"
    card_bg = "#262730"
    border_color = "#333333"
    text_color = "#ffffff"
    text_secondary = "#bbbbbb"
    
    accent_primary = "#DC143C"  # Crimson
    accent_hover = "#b01030"
    highlight_color = "#DC143C"
    
else:
    # LIGHT MODE: Matches config.toml defaults
    bg_color = "#ffffff"
    card_bg = "#f0f4ff"
    border_color = "#e0e0e0"
    text_color = "#000000"
    text_secondary = "#333333"
    
    accent_primary = "#0056b3"
    accent_hover = "#004494"
    highlight_color = "#FFD700" # Gold


# Custom CSS for clean, flat UI
st.markdown(f"""
<style>
    /* v1.5 Force Refresh */
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base App Styling */
    .stApp {{
        background-color: {bg_color};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {text_color} !important;
    }}
    
    /* Header Bar - must match background */
    header[data-testid="stHeader"] {{
        background-color: {bg_color} !important;
    }}
    
    /* Top toolbar/decoration bar */
    .stDeployButton, [data-testid="stToolbar"] {{
        background-color: {bg_color} !important;
    }}
    
    h1, h2, h3, h4, h5, h6, span, div, p, label, .stMarkdown, .stText {{
        font-family: 'Inter', sans-serif;
        color: {text_color} !important;
    }}
    
    /* Input Fields (Text Area, Inputs, Selectbox) */

    /* Input Fields (Text Area, Inputs, Selectbox) */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }}
    
    /* Force textarea text color */
    textarea {{
        color: {text_color} !important;
        caret-color: {text_color} !important;
    }}
    
    /* Placeholder text */
    textarea::placeholder {{
        color: {text_secondary} !important;
        opacity: 0.7;
    }}
    
    /* Selectbox dropdown styling */
    .st-cp, .st-cq, .st-cr, .st-cs {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Stronger Label Selectors */
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] span,
    label[data-testid="stWidgetLabel"] p {{
        color: {text_color} !important;
        font-weight: 500;
    }}
    
    .stTextArea textarea:focus, .stTextInput input:focus {{
        border-color: {accent_primary} !important;
        box-shadow: 0 0 0 1px {accent_primary} !important;
    }}

    /* Tabs - Explicit coloring */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {{
        color: {text_secondary} !important;
    }}
    
    button[data-baseweb="tab"][aria-selected="true"] div[data-testid="stMarkdownContainer"] p {{
        color: {accent_primary} !important;
        font-weight: 600;
    }}
    
    /* Force Tab Underline Color - hide default, show only theme color */
    button[data-baseweb="tab"][aria-selected="true"] {{
        border-bottom: 3px solid {accent_primary} !important;
    }}
    
    /* Hide Streamlit's default blue highlight bar */
    .stTabs [data-baseweb="tab-highlight"] {{
        background-color: {accent_primary} !important;
    }}
    
    /* Tabs Container underline */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: transparent;
        border-bottom: 1px solid {border_color};
        padding-bottom: 0;
    }}
    
    /* File Uploader Dropzone - Theme-aware Background */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {card_bg} !important;
        border: 1px dashed {border_color} !important;
        border-radius: 8px;
    }}
    
    .st-emotion-cache-12izz8t {{
        background-color: {card_bg} !important;
    }}
    
    /* Expander Summary - Theme-aware Background */
    .st-emotion-cache-gsdrzw, summary {{
        background-color: {card_bg} !important;
        border-radius: 8px;
        padding: 0.5rem;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {bg_color};
        border-right: 1px solid {border_color};
    }}
    
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
        color: {text_color} !important;
    }}
    
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] li {{
        color: {text_secondary} !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background-color: transparent;
        border-bottom: 1px solid {border_color};
        padding-bottom: 0;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border: none;
        color: {text_secondary};
        padding-bottom: 10px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: transparent !important;
        color: {accent_primary} !important;
        font-weight: 600;
        border-bottom: 2px solid {accent_primary};
    }}
    
    /* Main Header - Clean & Simple */
    .main-header {{
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid {border_color};
    }}
    
    .main-header h1 {{
        color: {accent_primary};
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }}
    
    .main-header p {{
        color: {text_secondary};
        font-size: 1.1rem;
    }}
    
    /* Primary Buttons */
    .stButton > button {{
        background-color: {accent_primary} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        transition: background-color 0.2s;
    }}
    
    .stButton > button:hover {{
        background-color: {accent_hover} !important;
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background-color: {card_bg};
        border: 1px dashed {border_color};
        border-radius: 8px;
        padding: 20px;
    }}
    
    /* Result Container */
    .result-container {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-left: 6px solid {highlight_color}; /* Gold in Light Mode */
        border-radius: 8px;
        padding: 2rem;
        margin-top: 1.5rem;
    }}
    
    .result-container * {{
        color: {text_color} !important;
    }}
    
    .result-container code {{
        background-color: {bg_color} !important;
        border: 1px solid {border_color};
        color: {accent_primary} !important;
        border-radius: 4px;
        padding: 2px 5px;
    }}
    
    /* Donation Box - Outline Style */
    .donation-box {{
        border: 2px solid {highlight_color}; /* Gold Border */
        background-color: {card_bg};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 2rem;
    }}
    
    .donation-box h3 {{
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: {text_color};
    }}
    
    .donation-box p {{
        font-size: 0.85rem;
        color: {text_secondary};
        margin-bottom: 1rem;
    }}
    
    .donation-btn {{
        display: inline-block;
        background-color: transparent;
        color: {accent_primary} !important;
        border: 1px solid {accent_primary};
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s;
    }}
    
    .donation-btn:hover {{
        background-color: {accent_primary};
        color: white !important;
    }}
    
    /* History Items */
    .history-item {{
        padding: 0.8rem;
        border-bottom: 1px solid {border_color};
    }}
    
    .history-item:last-child {{
        border-bottom: none;
    }}
    
    .history-item strong {{
        display: block;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
        color: {text_color};
    }}
    
    .history-item small {{
        font-size: 0.75rem;
        color: {text_secondary};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: transparent !important;
        color: {text_color} !important;
        border: 1px solid {border_color};
        border-radius: 8px;
    }}
    
    /* Alerts/Success */
    .stAlert {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        color: {text_color};
    }}
    
    /* Hide Default Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Theme toggle
    st.markdown("### 🎨 Theme")
    if st.button("🌓 Toggle Dark/Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    
    current_theme = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
    st.caption(f"Current: {current_theme}")
    
    st.markdown("---")
    
    st.markdown("### 📚 About")
    st.markdown("""
    **AI Assignment Brainstormer** helps you:
    - Generate assignment outlines
    - Create code snippets with explanations
    - Structure essays and papers
    
    Powered by **Kimi K2** AI model via Ollama Cloud.
    """)
    
    st.markdown("---")
    
    # Saweria donation box
    st.markdown("""
    <div class="donation-box">
        <h3>☕ Support Development</h3>
        <p>Help keep this free study aid running!</p>
        <a href="https://saweria.co/bryanchan" target="_blank" class="donation-btn">
            🎁 Donate via Saweria
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # History section
    st.markdown("### 📜 Recent History")
    history = get_prompt_history(10)
    if history:
        for i, item in enumerate(history):
            type_emoji = {
                "outline": "📋", "code": "💻", "essay": "📝",
                "summary": "📄", "notes": "📝", "quiz": "❓"
            }.get(item["generation_type"], "📄")
            
            # Truncate topic for display
            display_topic = item["topic"][:25] + "..." if len(item["topic"]) > 25 else item["topic"]
            
            # Create a button for each history item
            if st.button(f"{type_emoji} {display_topic}", key=f"history_{item['id']}", use_container_width=True):
                st.session_state.selected_history = item
                st.rerun()
    else:
        st.info("No history yet. Start generating!")

# Main content
st.markdown("""
<div class="main-header">
    <h1>🎓 AI Assignment Brainstormer</h1>
    <p>Dapatkan outline, code snippet, atau struktur essay untuk tugas kuliahmu dengan AI!</p>
</div>
""", unsafe_allow_html=True)

# Show selected history item as a modal-like popup in main area
if "selected_history" in st.session_state and st.session_state.selected_history:
    selected = st.session_state.selected_history
    
    # Create a prominent container for history view
    st.markdown(f"""
    <div style="
        background-color: {card_bg};
        border: 2px solid {highlight_color};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; color: {text_color};">📖 Viewing History</h3>
        </div>
        <p style="color: {text_color};"><strong>Topic:</strong> {selected['topic']}</p>
        <p style="color: {text_secondary}; font-size: 0.85rem;">Type: {selected['generation_type']} | {selected['created_at']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if selected.get("response"):
        st.markdown(f"""
        <div class="result-container">
            {selected["response"]}
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("� Lihat dalam format Markdown", expanded=False):
            st.markdown(selected["response"])
    else:
        st.warning("No saved response for this item.")
    
    if st.button("✖️ Close History View", use_container_width=True):
        del st.session_state.selected_history
        st.rerun()
    
    st.markdown("---")

# Tabs for different input methods
tab1, tab2 = st.tabs(["📝 Text Input", "📁 Upload File"])

with tab1:
    # Text input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_area(
            "📝 Masukkan topik tugas (Enter your assignment topic)",
            placeholder="Contoh: Analisis algoritma sorting dalam Python...",
            height=100
        )
    
    with col2:
        generation_type = st.selectbox(
            "🎯 Tipe output",
            options=["outline", "code", "essay"],
            format_func=lambda x: {
                "outline": "📋 Assignment Outline",
                "code": "💻 Code Snippets",
                "essay": "📝 Essay Structure"
            }[x],
            key="text_gen_type"
        )

with tab2:
    # File upload section
    st.markdown("### 📁 Upload File untuk Dianalisis")
    st.caption("Mendukung: PDF, PowerPoint (PPTX), Gambar (PNG, JPG), Screenshot, dan tulisan tangan")
    
    uploaded_file = st.file_uploader(
        "Pilih file",
        type=["pdf", "pptx", "ppt", "png", "jpg", "jpeg", "gif", "bmp", "webp"],
        help="Upload dokumen PDF, presentasi PPT, atau gambar untuk dianalisis"
    )
    
    file_generation_type = st.selectbox(
        "🎯 Tipe output untuk file",
        options=["summary", "outline", "notes", "quiz"],
        format_func=lambda x: {
            "summary": "📄 Ringkasan (Summary)",
            "outline": "📋 Outline Materi",
            "notes": "📝 Catatan Belajar",
            "quiz": "❓ Buat Soal Latihan"
        }[x],
        key="file_gen_type"
    )
    
    if uploaded_file is not None:
        # Show file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        # Preview for images
        if uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            st.image(uploaded_file, caption="Preview", width=300)
        
        if st.button("📖 Proses & Generate", use_container_width=True):
            with st.spinner("📄 Mengekstrak teks dari file..."):
                extracted_text, file_type = process_uploaded_file(uploaded_file)
                
                if extracted_text and not extracted_text.startswith("Error"):
                    st.info(f"📋 Teks dari {file_type} berhasil diekstrak ({len(extracted_text)} karakter)")
                    
                    with st.expander("👁️ Preview Teks yang Diekstrak"):
                        st.text_area("Extracted Text", extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""), height=200)
                    
                    # Generate based on extracted text
                    with st.spinner("🔮 AI sedang menganalisis..."):
                        try:
                            # Create prompt based on generation type
                            prompts = {
                                "summary": f"Buatkan ringkasan singkat dan jelas dari materi berikut dalam Bahasa Indonesia:\n\n{extracted_text}",
                                "outline": f"Buatkan outline/kerangka materi dari dokumen berikut untuk memudahkan belajar:\n\n{extracted_text}",
                                "notes": f"Buatkan catatan belajar yang terstruktur dari materi berikut, dengan poin-poin penting:\n\n{extracted_text}",
                                "quiz": f"Buatkan 5-10 soal latihan beserta jawabannya berdasarkan materi berikut:\n\n{extracted_text}"
                            }
                            
                            result = generate_content(prompts[file_generation_type], "outline")
                            
                            # Save to database
                            save_prompt(f"[{file_type}] {uploaded_file.name}", file_generation_type, result)
                            
                            # Display result
                            st.markdown("### 🎉 Hasil Analisis")
                            st.markdown(f"""
                            <div class="result-container">
                                {result}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            with st.expander("📖 Lihat dalam format Markdown", expanded=True):
                                st.markdown(result)
                            
                            st.success("✅ Hasil disimpan ke database!")
                            
                        except Exception as e:
                            st.error(f"⚠️ Error: {str(e)}")
                else:
                    st.error(f"⚠️ {extracted_text}")

# Generate button
if st.button("✨ Generate dengan Kimi K2", use_container_width=True):
    if not topic.strip():
        st.error("⚠️ Masukkan topik terlebih dahulu!")
    else:
        with st.spinner("🔮 AI sedang membuat konten untukmu..."):
            try:
                result = generate_content(topic, generation_type)
                
                # Save to database
                save_prompt(topic, generation_type, result)
                
                # Display result with proper styling
                st.markdown("### 🎉 Hasil Generate")
                st.markdown(f"""
                <div class="result-container">
                    {result}
                </div>
                """, unsafe_allow_html=True)
                
                # Also show in proper markdown format
                with st.expander("📖 Lihat dalam format Markdown", expanded=True):
                    st.markdown(result)
                
                st.success("✅ Hasil disimpan ke database!")
                
            except ValueError as e:
                st.error(f"⚠️ Error: {str(e)}")
                st.info("💡 Pastikan Ollama sudah berjalan dan terhubung ke cloud")
            except Exception as e:
                st.error(f"⚠️ Terjadi kesalahan: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {text_secondary}; padding: 1rem;">
    <p>Built with ❤️ for Indonesian students | Powered by Kimi K2 AI via Ollama Cloud</p>
    <p style="font-size: 0.8rem;">© 2026 Campus Productivity MVPs</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>

        /* =====================================================
           BUDGET VARIANCE ANALYZER
           GLOBAL DESIGN SYSTEM
        ===================================================== */

        :root {
            --page-bg: #F7F8FC;
            --surface: #FFFFFF;
            --surface-soft: #FBFBFE;

            --text-primary: #172033;
            --text-secondary: #667085;
            --text-muted: #98A2B3;

            --border: #E7EAF1;

            --indigo: #6875E8;
            --indigo-dark: #5563D8;
            --indigo-soft: #EEF0FF;

            --mint: #5BAE91;
            --mint-soft: #EAF7F2;

            --lavender: #F2F0FF;
            --blue-soft: #EEF5FF;

            --shadow-card:
                0 8px 28px rgba(31, 41, 55, 0.055);

            --shadow-button:
                0 5px 14px rgba(104, 117, 232, 0.18);

            --radius-card: 18px;
            --radius-small: 10px;
        }


        /* =====================================================
           PAGE
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 85% 5%,
                    rgba(104, 117, 232, 0.055),
                    transparent 25%
                ),
                var(--page-bg);
        }

        .main {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;

            padding-top: 2rem;
            padding-bottom: 3rem;

            padding-left: 3.5rem;
            padding-right: 3.5rem;
        }


        /* =====================================================
           TYPOGRAPHY
        ===================================================== */

        html,
        body,
        [class*="css"] {
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        h1,
        h2,
        h3,
        h4 {
            color: var(--text-primary) !important;
        }

        h1 {
            font-size: 2.55rem !important;
            line-height: 1.15 !important;

            font-weight: 720 !important;

            letter-spacing: -0.035em !important;

            margin-top: 0.4rem !important;
            margin-bottom: 0.8rem !important;
        }

        h3 {
            font-size: 1.05rem !important;
            font-weight: 680 !important;

            margin-bottom: 0.35rem !important;
        }

        h5 {
            color: var(--indigo) !important;

            font-size: 0.72rem !important;
            font-weight: 750 !important;

            letter-spacing: 0.12em !important;
        }

        p {
            color: var(--text-secondary) !important;

            line-height: 1.65 !important;
        }


        /* =====================================================
           HEADER
        ===================================================== */

        .app-header {
            padding-bottom: 1.8rem;
        }

        .app-header [data-testid="column"] {
            display: flex;
            align-items: center;
        }

        .app-header h3 {
            margin-bottom: 0.15rem !important;
        }

        .app-header .stCaption {
            color: var(--text-muted) !important;
        }


        /* =====================================================
           BRAND MARK
        ===================================================== */

        .brand-mark {
            display: inline-flex;

            width: 42px;
            height: 42px;

            align-items: center;
            justify-content: center;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #6875E8,
                    #8C96F2
                );

            color: white;

            font-size: 0.76rem;
            font-weight: 800;

            box-shadow:
                0 7px 18px
                rgba(104, 117, 232, 0.20);
        }


        /* =====================================================
           READY STATUS
        ===================================================== */

        .status-pill {
            display: inline-flex;

            align-items: center;
            justify-content: center;

            gap: 0.4rem;

            padding:
                0.38rem
                0.72rem;

            border-radius: 999px;

            background: var(--mint-soft);

            color: #397963;

            font-size: 0.75rem;

            font-weight: 650;

            white-space: nowrap;
        }


        /* =====================================================
           HERO SECTION
        ===================================================== */

        .hero-section {
            background:
                radial-gradient(
                    circle at 92% 8%,
                    rgba(104, 117, 232, 0.13),
                    transparent 32%
                ),
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #F8F8FF 100%
                );

            border:
                1px solid
                #E6E8F4;

            border-radius:
                var(--radius-card);

            padding:
                2.4rem
                2.5rem;

            margin:
                1rem 0
                1.4rem 0;

            box-shadow:
                var(--shadow-card);
        }


        /* =====================================================
           SECTION LABEL
        ===================================================== */

        .section-label {
            color: var(--indigo);

            font-size: 0.7rem;

            font-weight: 760;

            letter-spacing: 0.12em;

            text-transform: uppercase;

            margin-bottom: 0.65rem;
        }


        /* =====================================================
           HERO DESCRIPTION
        ===================================================== */

        .hero-description {
            max-width: 760px;

            color:
                var(--text-secondary);

            font-size:
                0.98rem;

            line-height:
                1.7;
        }


        /* =====================================================
           UPLOAD CARD
        ===================================================== */

        .upload-card {
            background:
                var(--surface);

            border:
                1px solid
                var(--border);

            border-radius:
                var(--radius-card);

            padding:
                1.55rem 1.6rem;

            box-shadow:
                var(--shadow-card);
        }


        /* =====================================================
           STREAMLIT FILE UPLOADER
        ===================================================== */

        [data-testid="stFileUploader"] {
            margin-top: 0.85rem;

            background:
                var(--surface-soft);

            border:
                1.5px dashed
                #C9CEE0;

            border-radius:
                14px;

            padding:
                0.65rem;

            transition:
                border-color
                0.2s ease,
                background
                0.2s ease,
                box-shadow
                0.2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color:
                var(--indigo);

            background:
                #FCFCFF;

            box-shadow:
                0 6px 20px
                rgba(104, 117, 232, 0.07);
        }

        [data-testid="stFileUploaderDropzone"] {
            background:
                transparent !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            border-radius:
                var(--radius-small);

            border:
                1px solid
                var(--border);

            background:
                var(--surface);

            color:
                var(--text-primary);

            font-weight:
                650;

            min-height:
                40px;

            transition:
                all
                0.18s
                ease;
        }

        .stButton > button:hover {
            border-color:
                var(--indigo);

            color:
                var(--indigo);

            box-shadow:
                var(--shadow-button);
        }


        /* =====================================================
           SUCCESS MESSAGE
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius:
                12px;

            border:
                1px solid
                #D7ECE3;

            background:
                var(--mint-soft);
        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {
            border:
                none !important;

            border-top:
                1px solid
                var(--border) !important;

            margin:
                2.2rem 0
                1.2rem 0 !important;
        }


        /* =====================================================
           FOOTER
        ===================================================== */

        .footer-text {
            color:
                var(--text-muted);

            font-size:
                0.72rem;

            text-align:
                center;
        }


        /* =====================================================
           STREAMLIT CHROME
        ===================================================== */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background:
                transparent;
        }


        /* =====================================================
           LINK / ANCHOR ICON CLEANUP
        ===================================================== */

        h1 a,
        h2 a,
        h3 a,
        h4 a,
        h5 a {
            display: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
def load_styles():
    pass

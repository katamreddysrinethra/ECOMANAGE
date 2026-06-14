import streamlit as st


# ==========================================
# EDUCATION HUB PAGE
# ==========================================

def education_hub_page():

    st.title("📚 Education Hub")

    st.info(
        """
        Learn how proper waste management helps
        protect the environment and create a
        cleaner, healthier community.
        """
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "♻️ Recycling",
            "🗂 Waste Segregation",
            "🌱 Composting",
            "💡 Sustainability Tips",
            "🎥 Learning Resources"
        ]
    )

    # ======================================
    # RECYCLING
    # ======================================

    with tab1:

        st.header("♻️ Recycling Basics")

        st.write(
            """
            Recycling is the process of converting
            waste materials into reusable materials.

            Benefits of Recycling:

            • Reduces landfill waste

            • Conserves natural resources

            • Saves energy

            • Reduces pollution

            • Creates employment opportunities

            • Protects ecosystems
            """
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                """
                Recyclable Items

                ✔ Plastic Bottles

                ✔ Paper

                ✔ Cardboard

                ✔ Glass Bottles

                ✔ Aluminum Cans

                ✔ Metal Containers
                """
            )

        with col2:

            st.warning(
                """
                Non-Recyclable Items

                ✖ Food-Contaminated Paper

                ✖ Medical Waste

                ✖ Hazardous Chemicals

                ✖ Used Tissues

                ✖ Sanitary Waste
                """
            )

    # ======================================
    # WASTE SEGREGATION
    # ======================================

    with tab2:

        st.header("🗂 Waste Segregation Guide")

        st.write(
            """
            Proper segregation ensures that waste
            is processed efficiently and safely.
            """
        )

        st.subheader("Green Bin - Wet Waste")

        st.success(
            """
            Food Waste

            Vegetable Peels

            Fruit Waste

            Leftover Food

            Garden Waste
            """
        )

        st.subheader("Blue Bin - Dry Waste")

        st.info(
            """
            Paper

            Plastic

            Cardboard

            Glass

            Metal
            """
        )

        st.subheader("Red Bin - Hazardous Waste")

        st.error(
            """
            Batteries

            Electronic Waste

            Chemicals

            Paint Containers

            Medical Waste
            """
        )

        st.divider()

        st.subheader("Common Waste Categories")

        waste_data = {
            "Plastic":
                "Water bottles, containers, packaging materials",

            "Paper":
                "Newspapers, books, cardboard, office paper",

            "Glass":
                "Glass bottles and jars",

            "Metal":
                "Aluminum cans and metal scraps",

            "Food":
                "Kitchen waste and leftovers",

            "E-Waste":
                "Computers, chargers, batteries, electronics"
        }

        for category, details in waste_data.items():

            with st.expander(category):

                st.write(details)

    # ======================================
    # COMPOSTING
    # ======================================

    with tab3:

        st.header("🌱 Composting at Home")

        st.write(
            """
            Composting converts organic waste into
            nutrient-rich fertilizer for plants.
            """
        )

        st.subheader("Items Suitable for Composting")

        st.success(
            """
            ✔ Vegetable Peels

            ✔ Fruit Waste

            ✔ Coffee Grounds

            ✔ Tea Leaves

            ✔ Dry Leaves

            ✔ Garden Waste
            """
        )

        st.subheader("Avoid Composting")

        st.error(
            """
            ✖ Meat

            ✖ Dairy Products

            ✖ Oily Food

            ✖ Plastic

            ✖ Glass

            ✖ Chemicals
            """
        )

        st.subheader("Composting Steps")

        st.write(
            """
            Step 1: Collect organic waste.

            Step 2: Create a compost bin.

            Step 3: Add dry leaves and kitchen waste.

            Step 4: Mix regularly.

            Step 5: Wait several weeks for decomposition.

            Step 6: Use compost in gardens and plants.
            """
        )

    # ======================================
    # SUSTAINABILITY TIPS
    # ======================================

    with tab4:

        st.header("💡 Sustainable Living Tips")

        tips = [

            "Carry reusable shopping bags.",

            "Avoid single-use plastics.",

            "Use reusable water bottles.",

            "Switch off electrical devices when not in use.",

            "Choose eco-friendly packaging.",

            "Repair items instead of replacing them.",

            "Donate usable items.",

            "Compost food waste.",

            "Reduce paper usage.",

            "Recycle whenever possible."
        ]

        for tip in tips:

            st.success(f"✔ {tip}")

        st.divider()

        st.subheader("The 3Rs Principle")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Reduce",
                "Waste Generation"
            )

        with col2:

            st.metric(
                "Reuse",
                "Extend Product Life"
            )

        with col3:

            st.metric(
                "Recycle",
                "Recover Resources"
            )

    # ======================================
    # LEARNING RESOURCES
    # ======================================

    with tab5:

        st.header("🎥 Learning Resources")

        st.write(
            """
            Watch educational videos and learn
            more about environmental sustainability.
            """
        )

        st.subheader("Waste Management Awareness")

        st.video(
            "https://www.youtube.com/watch?v=OasbYWF4_S8"
        )

        st.subheader("Recycling Process")

        st.video(
            "https://www.youtube.com/watch?v=gC9E2jG6lZg"
        )

        st.subheader("Why Waste Segregation Matters")

        st.video(
            "https://www.youtube.com/watch?v=YbYWhdLO43Q"
        )

        st.info(
            """
            Learning about waste management is the
            first step toward building a sustainable future.
            """
        )

    st.divider()

    st.success(
        """
        🌍 Small actions create big environmental impact.

        Reduce • Reuse • Recycle
        """
    )
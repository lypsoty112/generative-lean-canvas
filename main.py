import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

from src.main import generate

def create_lean_canvas_image(data):
    # Create a new image with a white background
    img = Image.new('RGB', (1600, 1200), color='white')
    d = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Define sections and their positions with subcategories
    sections = [
        ("Problem", (50, 100, 550, 250), "Existing Alternatives", (50, 250, 550, 350)),
        ("Solution", (550, 100, 1050, 350), None, None),
        ("Customer Segments", (1050, 100, 1550, 250), "Early Adopters", (1050, 250, 1550, 350)),
        ("Unique Value Proposition", (550, 350, 1050, 500), "High-level Concept", (550, 500, 1050, 600)),
        ("Channels", (1050, 350, 1550, 600), None, None),
        ("Cost Structure", (50, 600, 800, 800), None, None),
        ("Revenue Streams", (800, 600, 1550, 800), None, None),
        ("Key Metrics", (50, 800, 800, 1000), None, None),
        ("Unfair Advantage", (800, 800, 1550, 1000), None, None)
    ]

    # Draw the main and subcategories
    for section, (left, top, right, bottom), sub, sub_bounds in sections:
        # Draw the section box
        d.rectangle([left, top, right, bottom], outline="black", width=3)
        # Draw the section title
        d.text((left+10, top+10), section, font=title_font, fill="black")
        text = data.get(section, "")
        lines = text.split('\n')
        y = top + 40
        for line in lines:
            d.text((left+10, y), line, font=font, fill="black")
            y += 25

        # Draw the subcategory box if available
        if sub:
            d.rectangle([sub_bounds[0], sub_bounds[1], sub_bounds[2], sub_bounds[3]], outline="black", width=3)
            d.text((sub_bounds[0]+10, sub_bounds[1]+10), sub, font=title_font, fill="black")
            sub_text = data.get(sub, "")
            sub_lines = sub_text.split('\n')
            y = sub_bounds[1] + 40
            for line in sub_lines:
                d.text((sub_bounds[0]+10, y), line, font=font, fill="black")
                y += 25

    return img

def main():
    st.title("Lean Canvas Generator")

    # Initialize session state for form inputs
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "Problem": "",
            "Existing Alternatives": "",
            "Customer Segments": "",
            "Early Adopters": "",
            "Unique Value Proposition": "",
            "High-level Concept": "",
            "Solution": "",
            "Channels": "",
            "Revenue Streams": "",
            "Cost Structure": "",
            "Key Metrics": "",
            "Unfair Advantage": ""
        }

    # Create input fields for each section and subcategories
    st.header("Fill in your Lean Canvas")

    sections = [
        "Problem", "Existing Alternatives", "Customer Segments", "Early Adopters",
        "Unique Value Proposition", "High-level Concept", "Solution", "Channels",
        "Revenue Streams", "Cost Structure", "Key Metrics", "Unfair Advantage"
    ]

    for section in sections:
        st.subheader(section)
        st.session_state.form_data[section] = st.text_area(f"Enter {section}", st.session_state.form_data[section])

    # Generate button
    # Inside the Generate button callback

    if st.button("Generate Lean Canvas"):
        if not st.session_state.form_data["Problem"]:
            st.error("Error: The 'Problem' field is required.")
        else:
            # Call the generate method and pass in the form data
            canvas_data = generate(
                problem=st.session_state.form_data["Problem"],
                existing_alternatives=st.session_state.form_data["Existing Alternatives"],
                customer_segments=st.session_state.form_data["Customer Segments"],
                early_adopters=st.session_state.form_data["Early Adopters"],
                unique_value_proposition=st.session_state.form_data["Unique Value Proposition"],
                high_level_concept=st.session_state.form_data["High-level Concept"],
                solution=st.session_state.form_data["Solution"],
                channels=st.session_state.form_data["Channels"],
                revenue_streams=st.session_state.form_data["Revenue Streams"],
                cost_structure=st.session_state.form_data["Cost Structure"],
                key_metrics=st.session_state.form_data["Key Metrics"],
                unfair_advantage=st.session_state.form_data["Unfair Advantage"],
            )

            # Create the Lean Canvas image using the data returned from generate()
            img = create_lean_canvas_image(canvas_data)

            # Convert the image to bytes for download and display
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Display the image
            st.image(img, caption='Your Lean Canvas', use_column_width=True)

            # Provide option to download as PNG
            st.download_button(
                label="Download Lean Canvas as PNG",
                data=img_byte_arr,
                file_name="lean_canvas.png",
                mime="image/png",
            )


if __name__ == "__main__":
    main()

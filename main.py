import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

from src.main import build, generate


def create_lean_canvas_image(problem, customer_segments, existing_alternatives, solution, 
                             high_level_concept, unique_value_proposition, channels, 
                             revenue_streams, cost_structure, early_adopters, key_metrics, 
                             unfair_advantage):
    img = Image.open("./data/lean-canvas.jpg")
    draw = ImageDraw.Draw(img)
    
    # Load a font - you may need to adjust the font path and size
    font = ImageFont.truetype("arial.ttf", 70)  # Adjust size as needed
    
    # Define text color and border colors
    text_color = (0, 0, 0)  # Black
    
    # Function to wrap text
    def wrap_text(text, max_width):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return '\n'.join(lines)
    
    # Define positions, max widths, and heights for each section
    sections = {
        'problem': (500, 1800, 2500, 3200), # DONE
        'customer_segments': (11200, 1800, 2500, 3200),  # DONE
        'existing_alternatives': (500, 5400, 2500, 1000), # DONE
        'solution': (3100, 1800, 2500, 2000), # DONE
        'high_level_concept': (5800, 5600, 2500, 850), # DONE
        'unique_value_proposition': (5800, 1800, 2500, 3000), # DONE
        'unfair_advantage': (8500, 1800, 2500, 1700),# DONE
        'channels': (8500, 4500, 2500, 1700), # DONE
        'early_adopters': (11200, 5400, 2500, 1000),
        'key_metrics': (3100, 4500, 2500, 1500),# DONE
        'cost_structure': (500, 7150, 6000, 1450), # DONE
        'revenue_streams': (7200, 7150, 6000, 1450) # DONE
    }
    
    # Draw borders and add text to each section
    for section, (x, y, max_width, height) in sections.items():
        text = locals()[section]
        wrapped_text = wrap_text(text, max_width)
        
        # Add the wrapped text inside the section
        draw.text((x, y), wrapped_text, font=font, fill=text_color)
    
    draw.text((500, 9600), "Warning: This canvas was AI-generated, and should be seen as a suggestion", font=font, fill=(255, 0, 0))    
    return img

def main():
    st.set_page_config(
        page_title="Generative Lean Canvas",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🛠️"
    )

    st.title("Lean Canvas Generator")

    with st.expander('❔ How it works'):
        st.markdown("""
        This app helps you easily create a Lean Canvas, a tool used to map out the key elements of your business idea on a single page.

        **Step 1**: Provide an API key (If you're unsure what an API key is, you can learn more [here](https://en.wikipedia.org/wiki/API_key)). This key allows the app to communicate with an AI service to help generate the canvas.

        **Step 2**: Start by filling in the 'Problem' field (this is the only required field). You can also complete any other sections you've thought of, like your proposed solution or customer segments.

        **Step 3**: The AI will take the information you provide and help fill out the remaining sections. It does this by analyzing your input and, when necessary, searching for additional details or thinking through multiple iterations to generate a complete Lean Canvas.
        
        Don't worry if you're missing some information — the AI will assist in completing the rest!
                    
        If you're interested in other projects of mine, go to my [GitHub](https://github.com/lypsoty112) or go to my [company's website](https://www.brevisai.com)
        """)


    key = os.getenv("OPENAI_API_KEY", None)
    if key is None or "KEY" not in st.session_state:
        st.sidebar.header("⚠️ WARNING: Paste your OpenAI key first.")
        st.sidebar.write(
            "You can find or create your OpenAI API key at https://platform.openai.com/account/api-keys. This app "
            "doesn't store your API key. It is only used to make requests to the OpenAI API.")
        key = st.sidebar.text_input("OpenAI API Key", type="password")
        if st.sidebar.button("Upload OpenAI API key"):
            os.environ["OPENAI_API_KEY"] = key
            st.session_state["KEY"] = key

    
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

    # Explanations for each field
    sections_explanations = {
        "Problem": "What specific problem are you solving for your customers? ⚠️This is the only field that's required. The others are completely optional.",
        "Existing Alternatives": "What alternatives do your potential customers currently use to solve this problem?",
        "Customer Segments": "Who are your target customers? Define the key segments you aim to serve.",
        "Early Adopters": "Who are the first users or customers likely to use your product or service?",
        "Unique Value Proposition": "What makes your solution unique and why should customers choose you over competitors?",
        "High-level Concept": "Summarize your solution in a single, easy-to-understand sentence or phrase.",
        "Solution": "What is your solution to the problem? Describe how your product or service solves it.",
        "Channels": "How will you reach your customers? List the key distribution channels you'll use.",
        "Revenue Streams": "How will your business make money? Define the ways you'll generate revenue.",
        "Cost Structure": "What are the main costs to operate your business? Include fixed and variable costs.",
        "Key Metrics": "What key performance indicators will help you track the success of your business?",
        "Unfair Advantage": "What do you have that cannot easily be copied or bought by your competitors?"
    }

    for section in sections:
        st.subheader(section)
        st.write(sections_explanations[section])
        st.session_state.form_data[section] = st.text_area(f"Enter {section}", st.session_state.form_data[section])

    # Generate button
    if st.button("Generate Lean Canvas"):
        if not st.session_state.form_data["Problem"]:
            st.error("Error: The 'Problem' field is required.")
        elif not st.session_state.form_data["KEY"]:
            st.error("Error: No API key has been given.")
        else:
            # Call the generate method and pass in the form data
            build(st.session_state["KEY"])
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
            img = create_lean_canvas_image(**canvas_data)

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

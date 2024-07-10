import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType
import base64

st.set_page_config(
    page_title="Mindmap Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE", type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Mindmap Generator")
st.markdown("## Welcome to the Mindmap Generator!")
st.markdown(
    "This App Harnesses power of Lyzr Automata to Generate Mindmaps. You Need to input Your topic and it will craft mindmap")


if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def mindmap_generator(topic):
    mindmap_agent = Agent(
        prompt_persona=f"You are an Expert in system design.",
        role="System Designer",
    )

    mindmap_task = Task(
        name="content writer",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=mindmap_agent,
        log_output=True,
        instructions=f"""
        Generate a Mindmap in given format for {topic}.
        mindmap in top is compulsory.
        format:
        "
        mindmap
          school_management
            administration
                staff_management
                    recruitment
                    training
                    scheduling
                student_management
                    enrollment
                    attendance
                    discipline
                facilities_management
                    maintenance
                    safety
                    supplies
            academics
                curriculum_development
                    syllabus_planning
                    material_selection
        "
                    
        ONLY GENERATE MINDMAP CODE NOTHING ELSE APART FROM IT
        """,
    )

    output = LinearSyncPipeline(
        name="Mindmap Generation",
        completion_message="Mindmap Generated!",
        tasks=[
            mindmap_task
        ],
        ).run()
    return output[0]['task_output']


topic = st.text_input("Enter Topic")

if st.button("Generate"):
    solution = mindmap_generator(topic)
    st.markdown(solution)


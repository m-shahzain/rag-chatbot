import gradio as gr
from rag import ask_rag

demo = gr.Interface(
    fn=ask_rag,

    inputs=gr.Textbox(
        lines=2,
        placeholder="Ask your question..."
    ),

    outputs=gr.Textbox(lines=8),

    title="ConnectGenie RAG Chatbot",

    description="Ask questions about the ConnectGenie Privacy Policy."
)

demo.launch(share=True)
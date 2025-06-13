import gradio as gr
import os
from typing import Dict, List
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.core.geo_optimizer import GEOOptimizer
from src.core.ai_simulator import AIResponseSimulator

# Initialize core components
geo_optimizer = GEOOptimizer()
ai_simulator = AIResponseSimulator(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

def create_geo_interface() -> gr.Blocks:
    """Create the main Gradio interface for the GEO AI Optimizer."""
    
    with gr.Blocks(
        title="🚀 GEO AI Optimizer",
        theme=gr.themes.Soft(),
        css=".container { max-width: 1200px; margin: auto; }"
    ) as app:
        gr.Markdown(
            """
            # 🚀 GEO AI Optimizer
            
            Optimize your content for AI assistants and search engines using advanced NLP and machine learning techniques.
            
            ### Features:
            - Content optimization for AI understanding
            - Q&A pair generation
            - Entity extraction and enhancement
            - AI response simulation
            - Performance analytics
            """
        )
        
        with gr.Tab("Content Input"):
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        label="Input Content",
                        placeholder="Enter your content here...",
                        lines=10
                    )
                    file_input = gr.File(
                        label="Or upload a file (PDF, DOCX, TXT)",
                        file_types=["pdf", "docx", "txt"]
                    )
                
                with gr.Column():
                    target_queries = gr.Textbox(
                        label="Target Queries (one per line)",
                        placeholder="Enter target queries...",
                        lines=5
                    )
                    optimization_level = gr.Radio(
                        choices=["conservative", "balanced", "aggressive"],
                        value="balanced",
                        label="Optimization Level"
                    )
        
        with gr.Tab("GEO Optimization"):
            with gr.Row():
                with gr.Column():
                    optimize_btn = gr.Button("🔄 Optimize Content", variant="primary")
                    
                    optimized_output = gr.Textbox(
                        label="Optimized Content",
                        lines=10,
                        interactive=False
                    )
                    
                with gr.Column():
                    optimization_stats = gr.JSON(
                        label="Optimization Statistics"
                    )
                    
                    qa_pairs = gr.Dataframe(
                        headers=["Question", "Answer", "Confidence"],
                        label="Generated Q&A Pairs"
                    )
        
        with gr.Tab("AI Simulation"):
            with gr.Row():
                with gr.Column():
                    simulate_btn = gr.Button("🤖 Simulate AI Responses", variant="primary")
                    
                    with gr.Accordion("GPT-4 Response", open=False):
                        gpt4_response = gr.Textbox(
                            label="GPT-4 Response",
                            lines=5,
                            interactive=False
                        )
                    
                    with gr.Accordion("Claude Response", open=False):
                        claude_response = gr.Textbox(
                            label="Claude Response",
                            lines=5,
                            interactive=False
                        )
                
                with gr.Column():
                    inclusion_scores = gr.Plot(
                        label="AI Inclusion Scores"
                    )
                    
                    simulation_stats = gr.JSON(
                        label="Simulation Statistics"
                    )
        
        with gr.Tab("Analytics"):
            with gr.Row():
                with gr.Column():
                    entity_graph = gr.Plot(
                        label="Entity Distribution"
                    )
                    
                    semantic_coverage = gr.Plot(
                        label="Semantic Coverage"
                    )
                
                with gr.Column():
                    performance_metrics = gr.JSON(
                        label="Performance Metrics"
                    )
        
        # Event handlers
        async def optimize_content(
            text: str,
            queries: str,
            level: str
        ) -> tuple:
            """Handle content optimization."""
            try:
                # Process queries
                query_list = [q.strip() for q in queries.split("\n") if q.strip()]
                
                # Optimize content
                result = geo_optimizer.optimize_for_ai_assistants(
                    content=text,
                    target_queries=query_list,
                    optimization_level=level
                )
                
                # Prepare Q&A pairs for display
                qa_data = [
                    [qa["question"], qa["answer"], f"{qa['confidence']:.2f}"]
                    for qa in result.qa_pairs
                ]
                
                return (
                    result.optimized_content,
                    {
                        "Confidence Score": result.confidence_score,
                        "Entity Count": result.metadata["entity_count"],
                        "Q&A Pairs": result.metadata["qa_pair_count"]
                    },
                    qa_data
                )
                
            except Exception as e:
                return (
                    f"Error during optimization: {str(e)}",
                    {"error": str(e)},
                    []
                )
        
        async def simulate_responses(
            text: str,
            queries: str
        ) -> tuple:
            """Handle AI response simulation."""
            try:
                # Process queries
                query_list = [q.strip() for q in queries.split("\n") if q.strip()]
                
                # Run simulation
                result = await ai_simulator.evaluate_content_inclusion_probability(
                    content=text,
                    queries=query_list
                )
                
                # Create inclusion score plot
                plot = create_inclusion_plot(result.inclusion_scores)
                
                return (
                    result.responses["gpt-4"],
                    result.responses["claude-3"],
                    plot,
                    {
                        "Average Score": f"{result.average_score:.2f}",
                        "Number of Queries": result.metadata["num_queries"],
                        "Content Length": result.metadata["content_length"]
                    }
                )
                
            except Exception as e:
                return (
                    f"Error: {str(e)}",
                    f"Error: {str(e)}",
                    None,
                    {"error": str(e)}
                )
        
        def create_inclusion_plot(scores: Dict[str, float]) -> gr.Plot:
            """Create a bar plot of inclusion scores."""
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(8, 4))
            models = list(scores.keys())
            values = list(scores.values())
            
            ax.bar(models, values)
            ax.set_ylim(0, 1)
            ax.set_title("AI Assistant Inclusion Scores")
            ax.set_ylabel("Score")
            
            for i, v in enumerate(values):
                ax.text(i, v + 0.01, f'{v:.2f}', ha='center')
            
            return fig
        
        # Connect event handlers
        optimize_btn.click(
            optimize_content,
            inputs=[input_text, target_queries, optimization_level],
            outputs=[optimized_output, optimization_stats, qa_pairs]
        )
        
        simulate_btn.click(
            simulate_responses,
            inputs=[optimized_output, target_queries],
            outputs=[gpt4_response, claude_response, inclusion_scores, simulation_stats]
        )
        
        # File upload handler
        def process_file(file) -> str:
            """Process uploaded file and return its content."""
            if file is None:
                return ""
                
            file_path = file.name
            ext = Path(file_path).suffix.lower()
            
            try:
                if ext == '.txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                        
                elif ext == '.pdf':
                    from PyPDF2 import PdfReader
                    reader = PdfReader(file_path)
                    return "\n".join(page.extract_text() for page in reader.pages)
                    
                elif ext == '.docx':
                    from docx import Document
                    doc = Document(file_path)
                    return "\n".join(para.text for para in doc.paragraphs)
                    
                else:
                    return "Unsupported file format"
                    
            except Exception as e:
                return f"Error processing file: {str(e)}"
        
        file_input.upload(
            process_file,
            inputs=[file_input],
            outputs=[input_text]
        )
        
        return app

if __name__ == "__main__":
    app = create_geo_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        auth=None  # Add authentication if needed
    ) 
TOPICS = {
    "Python": "Python basics, functions, OOP",
    "SQL": "SQL joins, aggregations, window functions",
    "Excel": "Excel formulas, pivot tables",
    "Power BI": "Power BI dashboards and DAX basics",
    "Pandas": "Pandas data cleaning and analysis",
    "Statistics": "Descriptive stats and hypothesis testing",
    "Data Visualization": "Matplotlib / Plotly charts",
    "Machine Learning": "Supervised learning fundamentals",
    "Scikit-learn": "Model training and evaluation with scikit-learn",
    "Deep Learning": "Neural networks with PyTorch or TensorFlow",
    "PyTorch": "PyTorch tensors, training loops",
    "NLP": "Text preprocessing, embeddings, classification",
    "Transformers": "Transformer architecture and fine-tuning",
    "Hugging Face": "Hugging Face pipelines and model hub",
    "LLM": "Prompting and LLM API usage",
    "RAG": "Build a RAG app with embeddings and a vector store",
    "OpenCV": "Image processing with OpenCV",
    "CNN": "CNN architectures for image tasks",
    "YOLO": "Object detection with YOLO",
    "FastAPI": "FastAPI basics, deploy an ML model as an API",
    "Flask": "Flask routes and templates",
    "APIs": "REST API design and consumption",
    "Docker": "Docker fundamentals, containerise an app",
    "Git": "Git and GitHub workflow",
    "MLflow": "Experiment tracking with MLflow",
    "Cloud Deployment": "Deploy on Streamlit Cloud / Render / AWS",
}


def generate_roadmap(missing: list[str], per_week: int = 2) -> list[str]:
    plan = []
    for i in range(0, len(missing), per_week):
        chunk = missing[i:i + per_week]
        topics = "; ".join(TOPICS.get(s, f"Learn the basics of {s}") for s in chunk)
        plan.append(f"Week {i // per_week + 1}: {topics}")
    return plan

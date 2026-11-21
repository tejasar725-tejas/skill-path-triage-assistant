"""Small language-model inference wrapper."""
from .core import train_model


def suggest_next_skills(current_skills: list[str], model=None, top_n: int = 5) -> list[dict]:
    if not current_skills or not any(s.strip() for s in current_skills):
        raise ValueError("Provide at least one current skill.")
    model = model or train_model()
    return model.predict([s.strip() for s in current_skills if s.strip()], top_n=top_n)

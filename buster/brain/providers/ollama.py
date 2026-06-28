class OllamaProvider:
    name = "ollama"

    def __init__(self, model="llama3.2"):
        self.model = model
        self.last_error = ""

    def available(self):
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=1.5)
            return r.status_code == 200
        except Exception as exc:
            self.last_error = str(exc)
            return False

    def complete(self, prompt, context=""):
        try:
            import requests
            r = requests.post("http://localhost:11434/api/generate", json={
                "model": self.model,
                "prompt": f"You are Buster, a desktop AI companion. Be direct.\n\nContext:\n{context}\n\nUser:\n{prompt}\n\nBuster:",
                "stream": False,
            }, timeout=90)
            if r.status_code != 200:
                return f"Ollama error: {r.status_code} {r.text[:200]}"
            return r.json().get("response", "").strip() or "Ollama returned no text."
        except Exception as exc:
            self.last_error = str(exc)
            return f"Ollama is not available: {exc}"

    def status(self):
        return f"ollama: {'ready' if self.available() else 'not running'} model={self.model}"

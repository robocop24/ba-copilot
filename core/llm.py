class LLMProvider:
   
   def generate(self, prompt):
      raise NotImplementedError("Subclasses must implement the generate method.")
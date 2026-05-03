# translator.py
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch
import os

class FixedTranslator:
    
    def __init__(self):
        print("\n" + "=" * 70)
        print("🚀 Loading Cross-Lingual Model (M2M100-418M)")
        print("   Mode: Direct Translation (e.g., Hindi -> Marathi)")
        print("   Optimization: 8-bit Dynamic Quantization (< 1GB RAM)")
        print("=" * 70)
        
        # Force CPU for quantization (Quantization is best supported on CPU)
        self.device = "cpu"
        print(f"   Device: {self.device} (Optimized for Quantized Inference)")
        
        model_name = "facebook/m2m100_418M"
        
        print("   Loading tokenizer...")
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        
        print("   Loading model (this may take a moment)...")
        # Load the full model first
        model = M2M100ForConditionalGeneration.from_pretrained(model_name)
        
        print("   📉 Applying Quantization (Compressing model)...")
        # MAGIC STEP: This reduces size from ~1.7GB to ~500MB
        self.model = torch.quantization.quantize_dynamic(
            model, 
            {torch.nn.Linear}, 
            dtype=torch.qint8
        )
        
        print("   ✅ Model loaded & compressed successfully!\n")
    
    def translate(self, text, source_lang_code, target_lang_code):
        """
        Translates directly between languages (No English pivot).
        """
        # Set the source language
        self.tokenizer.src_lang = source_lang_code
        
        # Prepare inputs
        encoded_input = self.tokenizer(
            text, 
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            generated_tokens = self.model.generate(
                **encoded_input,
                forced_bos_token_id=self.tokenizer.get_lang_id(target_lang_code),
                max_length=512,
                num_beams=4,  # Lower beam size slightly for speed
                early_stopping=True
            )
        
        # Decode output
        result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return result.strip()
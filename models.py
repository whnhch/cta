import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

class Similarity(nn.Module):
    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.cos = nn.CosineSimilarity(dim=-1)

    def forward(self, x, y):
        return self.cos(x, y) / self.temp
    
class TabCSE(nn.Module):
    def __init__(self, model_name, temp):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.sim = Similarity(temp)
        
    def forward(self, input_ids, attention_mask):
        bs=len(input_ids)/2
        input_ids = input_ids.view((-1, input_ids.size(-1))) # (bs * num_sent, len)
        attention_mask = attention_mask.view((-1, attention_mask.size(-1))) # (bs * num_sent len)
        
        x_outputs = self.bert(input_ids, attention_mask=attention_mask)

        # Extract embeddings from the model outputs
        pooler_output = x_outputs.pooler_output
        
        pooler_output = pooler_output.view((bs, 2, pooler_output.size(-1))) # (bs, num_sent, hidden)

        # Separate representation
        return pooler_output[:,0], pooler_output[:,1]

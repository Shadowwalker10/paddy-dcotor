import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models import vit_b_16, ViT_B_16_Weights
from torchinfo import summary
from paddydoctor.entity import PrepareBaseModelConfig


## Update Components
class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
    def get_base_model(self):
        weights_map = {"IMAGENET1K_V1": ViT_B_16_Weights.IMAGENET1K_V1, 
                       "IMAGENET1K_SWAG_E2E_V1": ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1}
        
        self.model = vit_b_16(weights=weights_map[self.config.params_weights])
        self.save_model(path = self.config.base_model_path, model = self.model)

    ## Static Method is defined when we want to use a function that doesn't rely on the class
    ## We cannot use self when a function is defined as static method
    ## Static Function can be directly run without instantating the class. Use it directly as
    ## PrepareBaseModel._prepare_full_model()
    
    @staticmethod
    def _prepare_full_model(model, 
                            classes:int, 
                            freeze_all:bool, 
                            freeze_till:int, 
                            learning_rate:float, 
                            dropout_rate: float, 
                            l2_weight_decay: float):
        # Freeze all layers if freeze_all is true
        if freeze_all:
            for param in model.parameters():
                param.requires_grad = False
        elif freeze_till is not None and freeze_till>0:
            for param in list(model.parameters())[:-freeze_till]:
                param.requires_grad = False

        # Replace the classification head
        
        model.heads = nn.Sequential(nn.Linear(768,1028),
                                    nn.ReLU(), 
                                    nn.Dropout(dropout_rate),
                                    nn.Linear(1028, 128),
                                    nn.ReLU(),
                                    nn.Dropout(dropout_rate),
                                    nn.Linear(128, classes),
                                    nn.Softmax(dim = 1))
        # Define optimizer
        optimizer = optim.Adam(params = model.parameters(), 
                               lr = learning_rate, 
                               weight_decay = l2_weight_decay)
        # Define loss function
        criterion = nn.CrossEntropyLoss()

        print(summary(model = model, 
                input_size = (32,3,224,224), 
                col_names=["input_size", "output_size", "num_params", "trainable"],
                col_width = 20, row_settings = ["var_names"]))

        
        return model, optimizer, criterion
    
    def update_base_model(self):
        self.full_model,self.optimizer, self.criterion = self._prepare_full_model(model = self.model, 
                                                                                  classes = self.config.classes,
                                                                                  freeze_all = self.config.freeze_all, 
                                                                                  freeze_till = self.config.freeze_till, 
                                                                                  learning_rate = self.config.learning_rate, 
                                                                                  dropout_rate = self.config.dropout_rate, 
                                                                                  l2_weight_decay = self.config.l2_weight_decay
                                                                                  )
        self.save_model(self.config.updated_base_model_path, self.full_model)
    
    @staticmethod
    def save_model(path, model):
        torch.save(model.state_dict(), path)
        
        
from torch.utils.tensorboard import SummaryWriter
import time
import torch
from paddydoctor.entity import PrepareCallbacksConfig
import os

## Update the components

class PrepareCallbacks:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config
    
    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(self.config.tensorboard_root_log_dir, 
                                          f"tb_logs_at_{timestamp}")
        self.writer = SummaryWriter(log_dir = tb_running_log_dir)
        return self.writer
    @property
    def _create_ckpt_callbacks(self, model, optimizer):
        checkpoint_path = self.config.checkpoint_model_filepath
        self.best_val_loss = float("inf")
        def save_checkpoint(epoch, val_loss):
            if val_loss<self.best_val_loss:
                self.best_val_loss = val_loss
                torch.save({"epoch": epoch, 
                            "model_state_dict": model.state_dict(),
                            "optimizer_state_dict": optimizer.state_dict(),
                            "val_loss": val_loss}, checkpoint_path)
            else:
                return
        return save_checkpoint
    
    @property
    def _create_reduce_lr_callbacks(self, optimizer):
        return torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer,
                                                          "min",
                                                          factor = self.config.lr_reduce_factor, 
                                                          patience = self.config.lr_reduce_patience, 
                                                          min_lr = self.config.min_lr)
    @property
    def _create_early_stopping_callbacks(self):
        patience = self.config.early_stopping_patience
        delta = self.config.early_stopping_delta
        class EarlyStopping:
            def __init__(self):
                self.counter = 0 #counter for epochs without improvement
                self.best_score = None #tracks the lower val_score
                self.early_stop = False
                self.val_loss_min = float("inf")
            def __call__(self, val_loss): 
                #Using __call__ allows us to directly pass value to the class like a function
                ## The __call__ function directly allows us to pass the val_loss to the class itself
                ##obj =  _create_early_stopping_callbacks()
                ##obj(val_loss)

                score = -val_loss
                if self.best_score is None:
                    self.best_score = score
                    self.val_loss_min = val_loss
                elif score<self.best_score + delta:
                    self.counter+=1
                    print(f"EarlyStopping counter: {self.counter} out of {self.patience}")
                    if self.counter>patience:
                        self.early_stop = True
                else:
                    self.best_score = score
                    self.counter = 0 #reset counter if there is an improvement
                    self.val_loss_min = val_loss
        return EarlyStopping()
    
    def get_callbacks(self, model, optimizer):
        return {
            "tensorboard": self._create_tb_callbacks(),
            "model_ckpt": self._create_ckpt_callbacks(model, optimizer),
            "lr_scheduler": self._create_reduce_lr_callbacks(optimizer),
            "early_stopping": self._create_early_stopping_callbacks()
        }
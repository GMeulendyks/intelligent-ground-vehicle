
import os
import sys
import time
import v2
from torch import nn
from torch.utils.data import DataLoader
import torch
from v2 import data

def main():

    try:
        training_data_dir = sys.argv[1]
        validation_data_dir = sys.argv[2]
        save_fn = sys.argv[3]
    except:
        print('Error with getting arguments from input.')
        print('usage: python3 training.py {training_dir} {validation_dir} {output_file}')
        return

    if (torch.cuda.is_available()):
        print(f'Utilizing CUDA')
        device = 'cuda'
    else:
        device = 'cpu'

    # these parameters are wack
    # sometimes it uses a bunch of gpu
    # sometimes it uses no gpu
    # sometimes it goes fast
    # sometimes its slow
    batch_size = 32
    workers = 0

    model = v2.nn.NeuralNetwork().to(device)
    training_data = v2.data.DatasetV2(training_data_dir)
    training_data = DataLoader(training_data, batch_size=batch_size, pin_memory=True, num_workers=workers)
    validation_data = v2.data.DatasetV2(validation_data_dir)
    validation_data = DataLoader(validation_data, batch_size=batch_size, pin_memory=True, num_workers=workers)
    
    learning_rate = 1e-3

    loss_fn = nn.MSELoss().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    epochs = 500

    for epoch in range(epochs):
        try:
            print(f'Running epoch {epoch}....')
            print(f'Training...')
            now = time.time()
            avg_loss = v2.nn.train_nn(training_data, model, loss_fn, optimizer, device)
            print(f'Training took: {time.time() - now}s to finish')
            print(f'Returned loss: {avg_loss}')
            print(f'Validating...')
            now = time.time()
            v2.nn.test_nn(validation_data, model, loss_fn, device)
            print(f'Validation took: {time.time() - now}s to finish')
            print(f'Saving intermediary model....')
            torch.save(model.state_dict(), save_fn + '.int')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'Unexpected exception occurred! {e}')


    print("Training finished.")

    torch.save(model.state_dict(), save_fn)

if __name__ == "__main__":
    main()

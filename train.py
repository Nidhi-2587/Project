import json
from nltk_utils import tokenize,stem, bag_of_words
import numpy as np
import torch 
import torch.nn as nn 
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json','r', encoding='utf-8') as f:
    intents = json.load(f)
all_words = []
tags = []
xy=[]
for intent in intents['intents']:
    tag=intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))
    
ignore_words = ['?','!','.',',']  
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words)) #unique words
# Flatten the list of lists to get all tags
all_tags = [tag for tag_list in tags for tag in tag_list]

# Extract unique tags and sort them
unique_tags = sorted(set(all_tags))
#tags=sorted(set(tags))
#print(tags)

X_train = [] #bag_of_words
y_train = []
for(pattern_sentence,tag) in xy:
    bag= bag_of_words(pattern_sentence,all_words)
    X_train.append(bag)
    
    label = tags.index(tag)
    y_train.append(label) # Crossentropy loss
X_train = np.array(X_train) #training data
y_train = np.array(y_train) 


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
        
    def __getitem__(self,index):
        return self.x_data[index], self.y_data[index]
        
    def __len__(self):
        return self.n_samples 
 #hyperparameters   
batch_size=8  
hidden_size = 8  
output_size = len(tags)
input_size = len(X_train[0])
learning_rate=0.01
num_epochs = 1000
print(input_size, len(all_words))
print(output_size,tags)
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True,num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size,hidden_size,output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels= labels.to(torch.int64)
        
        #forward
        outputs = model(words)
        loss= criterion(outputs,labels)
        
        outputs = torch.softmax(outputs, dim=1)
        loss= criterion(outputs,labels)
        
        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch +1) % 100 ==0:
        print(f'epoch{epoch+1}/{num_epochs}, loss={loss.item():.4f}')
print(f'final loss,loss={loss.item():.4f}')    


data = {
    "model_state" :model.state_dict(),
    "model_class":str(model.__class__),
    "input_size" :input_size,
    "output_size" :output_size,
    "hidden_size" :hidden_size,
    "all_words": all_words,
    "tags": tags
    
}
FILE = "data.pth"
torch.save(data,FILE)

# Add these lines to check the training data
print("Sample X_train:", X_train[0])  # Print the first training data sample
print("Sample y_train:", y_train[0])  # Print the corresponding label


print(f'training complete. file saved to {FILE}')
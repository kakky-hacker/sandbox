import onnx
import onnx.helper
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 100)
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST(
        "./data",
        train=True,
        download=True,
        transform=transforms.Compose(
            [
                transforms.ToTensor(),
            ]
        ),
    ),
    batch_size=32,
    shuffle=True,
)

model = Net().to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

epochs = 10
for i in range(epochs):
    print(f"epoch : {i + 1}")
    model.train()
    loss_array = []
    for _, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.cross_entropy(output, target)
        loss_array.append(loss)
        loss.backward()
        optimizer.step()
    print(f"loss : {sum(loss_array) / len(loss_array)}")

dummy_input = torch.randn(1, 1, 28, 28, device=device)
torch.onnx.export(model, dummy_input, "mnist.onnx", opset_version=9)

model = onnx.load("mnist.onnx")
print(onnx.helper.printable_graph(model.graph))

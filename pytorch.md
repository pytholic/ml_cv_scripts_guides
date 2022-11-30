# Data prallelism
```python
device = torch.device("cuda:2")
batch_size=128
epochs = 5
...
if __name__ =='__main__':
    model_ft = models.mobilenet_v2(pretrained=True)
    model_ft.classifier[1] = nn.Linear(model_ft.last_channel, 2)
    model_ft = model_ft.to(device)
    model_ft = torch.nn.parallel.DataParallel(model_ft, device_ids=[2,3], dim=0)
```

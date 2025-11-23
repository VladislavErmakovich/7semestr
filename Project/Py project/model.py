import cv2
import torch
import torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, embeding_len=256, device_str = 'cuda'):
        super(Encoder, self).__init__()
        if device_str == 'cuda':
            self.device = torch.device(device_str)
        elif device_str == 'cpu':
            self.device = torch.device('cpu')
        
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)

        self.maxpool = nn.MaxPool2d(2, 2)
        self.drop = nn.Dropout(0.2) 

        self.fc1 = nn.Linear(256 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, embeding_len)

        self.to(self.device)
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def forward(self, x):
        out = self.maxpool(torch.nn.functional.relu(self.bn1(self.conv1(x))))
        out = self.maxpool(torch.nn.functional.relu(self.bn2(self.conv2(out))))
        out = self.maxpool(torch.nn.functional.relu(self.bn3(self.conv3(out))))
        out = self.maxpool(torch.nn.functional.relu(self.bn4(self.conv4(out))))
        out = out.flatten(start_dim=1)
        out = self.drop(out)
        out = torch.nn.functional.relu(self.fc1(out))
        out = self.fc2(out)
        out = torch.nn.functional.normalize(out, p=2, dim=1)
        return out
    
    def preprocess_face_haar(self, frame, target_size=(128, 128)):
       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        
        if len(faces) == 0:
            return None, None

        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_img = rgb_frame[y:y+h, x:x+w]
        
        try:
            face_resized = cv2.resize(face_img, target_size)
        except:
            return None, None

        face_tensor = torch.tensor(face_resized, dtype=torch.float32) / 255.0
        face_tensor = face_tensor.permute(2, 0, 1).unsqueeze(0)
        
        
        return face_tensor.to(self.device), (x, y, w, h)
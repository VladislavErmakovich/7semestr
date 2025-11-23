from model import Encoder
import cv2
import torch
import os

if __name__ == "__main__":
    WEIGHTS_FILE = "user_pre_best_model.pth"
    DB_FILE = "face_db.pt"
    THRESHOLD = 0.8 

    print("Загрузка модели...")
    model = Encoder(device_str='cpu')
    if os.path.exists(WEIGHTS_FILE):
        model.load_state_dict(torch.load(WEIGHTS_FILE))
    model.eval()

    if os.path.exists(DB_FILE):
        database = torch.load(DB_FILE)
        for name in database:
            database[name] = database[name].to(model.device)
    else:
        print("База не найдена")
        exit()


    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    print("Камера работает (Haar Cascades). 'q' - выход.")

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        face_tensor, coords = model.preprocess_face_haar(frame)

        if face_tensor is not None:
            x, y, w, h = coords
            
            with torch.no_grad():
                current_vector = model(face_tensor)

            best_name = "Unknown"
            best_score = -1.0

            for name, db_vector in database.items():
                score = torch.mm(current_vector, db_vector.t()).item()
                if score > best_score:
                    best_score = score
                    best_name = name

            if best_score > THRESHOLD:
                color = (0, 255, 0)
                label = f"{best_name} ({best_score:.2f})"
            else:
                color = (0, 0, 255)
                label = f"Unknown ({best_score:.2f})"

            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255, 255,255), 2)
            print(label)
        cv2.imshow('Face ID ', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
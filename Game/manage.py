import cv2

import sys
sys.path.append('C:\dimi_coding\FacePosition\AccountManager')
import sql_connector

connector  =  sql_connector.Connector("faceposition")
#Load the cascade
if hasattr(cv2, "data"):
    strPath =  cv2.data.haarcascades
else:
    strPath = "./"
face_cascade=cv2.CascadeClassifier( strPath + "haarcascade_frontalface_default.xml")

def scan_face(img):
    #Find face, draws rectangles around them
    #If zero img (red) if more than one face (blue) returns img in list
    #else returns the img plus the position and the size of the face

    #Detect faces
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    
    #Detect if zero or more than one face
    if len(faces) != 1:
        # Zero faces so img is red
        if len(faces) == 0:
            img[ :, :, 2] = 255
        # More than 1 faces so img is blue
        else:
            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 5)
            img[ :, :, 0] = 255
            
        return [img]
        
    # Rectangle around face
    else:
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 5)
        return [img, [x, y], [w, h]]


def add_score(user : str, game : str, score : float) -> None:
    user_id = connector.get_data("accounts", "Id", "UserName", user)[0][0]
    connector.add_data("scores", ("UserId", "Game", "Score"), (user_id, game, score))
    return 


def play(user):
    import follow_pos
    import match_pos

    # Print input
    if 0:
        while 1:
            print("What you want to play? Match the position[mp] or Follow the position[fp] ")
            choice = input().lower()
            if choice == "mp":
                #match_pos.main()
                break
            elif choice == "fp":
                #follow_pos.main()
                break
            elif choice == "q":
                break
            else:
                print("I didnt understand")

    # camera 
    if 1:
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        # Update shape
        h, w = img.shape[:2]
        h = int(h*1.2)
        w = int(w*1.2)

        while 1:
            ret, img = cap.read()
            # Resize img
            img = cv2.resize(img, (w, h))
            img = cv2.flip(img, 1)

            data_list = scan_face(img)

            img = data_list[0]

            # Draw the rectangle
            x1 = int(w/5)-10
            y = int(h/3.5)
            x_1 = x1+25
            y_1 = y+25
            cv2.rectangle(img, (x1, y), (x1+200, y+200), (0, 255, 255),  4)
            cv2.rectangle(img, (x_1, y_1), (x_1+150, y_1+150), (0, 255, 255), 4)
            x2 = x1*3
            x_2 = x2+25
            cv2.rectangle(img, (x2, y), (x2+200, y+200), (0, 255, 255),  4)
            cv2.rectangle(img, (x_2, y_1), (x_2+150, y_1+150), (0, 255, 255), 4)

            # Write the texts
            cv2.putText(img, "Match", (x1+30, y-50), 4, 1, [0, 0, 0], 2)
            cv2.putText(img, "the position", (x1, y-15), 4, 1, [0, 0, 0],2)

            cv2.putText(img, "Follow", (x2+30, y-50), 4, 1, [0, 0, 0], 2)
            cv2.putText(img, "the position", (x2, y-15), 4, 1, [0, 0, 0], 2)
            
            cv2.putText(img, f"{user}", (30,30), 4, 1, [0, 0, 0], 1)

            # check if the face is in the rectangle drawn to change coordinates
            if len(data_list) == 3:
                if ( abs(data_list[1][0] - x1) < 20 and abs(data_list[1][1] - y) < 20 ) or ( abs(data_list[1][0] - x_1) < 20 and abs(data_list[1][1] - y_1) < 20 ):
                    match_pos.main(user)
                    break
                if ( abs(data_list[1][0] - x2) < 20 and abs(data_list[1][1] - y) < 20 ) or ( abs(data_list[1][0] - x_2) < 20 and abs(data_list[1][1] - y_1) < 20 ):
                    follow_pos.main(user)
                    break

            cv2.imshow("Start", img)
            key = cv2.waitKey(1)
            if key == 32:
                break


if __name__ == "__main__":
    play("Guest")

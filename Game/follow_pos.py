import cv2
import time
import  random as rand
from manage import add_score, scan_face, connector

def main(user:str, step=5):
    # Initialize img
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    # Update shape
    h, w = img.shape[:2]
    h = int(h*1.2)
    w = int(w*1.2)
    # Initialize coorrdinates of the rectangle to follow
    x = 35 ; y = 30 ; before_x = 30
    # Random flip img or not
    if rand.randint(0, 1) == 0:
        flip = True
    else:
        flip = False
    print("The image is flipped?", flip)
    # Initialize won variable as False and change it to Win if pos (x, y) = (>=200, >= 360)
    won = False
    # Initialize time
    start_time = time.time()

    while 1:
        if time.time() - start_time > 100:
            break

        ret, img = cap.read()
        # Resize img each frame
        img = cv2.resize(img, (w, h))

        # Flip the image horizontaly if flip==true
        if flip:
            img = cv2.flip(img, 1)

        # Get the data
        data_list = scan_face(img)

        # Get image
        img = data_list[0]

        # wait 2 seconds before start
        if time.time() - start_time > 2:

            # Check if there is only one face
            if len(data_list) == 3:

                # Change the w and h of data_list to be realistic
                if data_list[2][0] > 150:
                    data_list[2][0] = (150)
                if data_list[2][1] > 150:
                    data_list[2][1] = (150)

                # check if the face is in the rectangle drawn to change coordinates
                if (abs(data_list[1][0]  - x) < 50 and abs(data_list[1][1] - y) < 50) :
                    if x >= w - 200:
                        if y <= 30:
                            before_y = y
                            y += step
                        elif y >= 360:                       
                            won = True
                            break
                        elif y >= 180:                            
                            before_y = y
                            before_x = x
                            x -= step
                        elif before_y < y:
                            before_y = y
                            y += step
                    elif x <= 30:
                        if y <= 180 + step:
                            before_y = y
                            y += step
                        elif y >= 360:
                            before_y = y
                            before_x = x
                            x += step
                        elif before_y < y:
                            before_y = y
                            y += step
                    elif before_x < x:
                        before_x = x
                        x += step
                    elif before_x > x:
                        before_x = x
                        x -= step
                    
                # If face not in rectangle put img cyan
                else:
                    img[:, :, 2]  = 50
                
                # draw rectangle
                cv2.rectangle(img, (x, y), (x+data_list[2][0], y+data_list[2][1]), [0, 255 ,255], 4)
            
            # Write the score using puText()
            cv2.putText(img, "time: " + str(round((time.time()-start_time-2), 1)), (w-100, 30), 1, 1, [255, 125, 0], 2)
        # Write username
        cv2.putText(img, f"{user}", (30,h-10), 4, 1, [255, 125, 0], 1)

        # cv2 functions to display the image
        cv2.imshow("Follow the position", img)
        key = cv2.waitKey(1)
        if key == 32:
            break

    # If completed 
    if won:
        # Calculate the time to reach score = 10  
        end_time = time.time()
        final_time = end_time - start_time - 2
        final_time = round(final_time, 1)
        # Print score at the end
        print("Your time to complete the path was " + str(final_time) + " seconds")
        # Check if user is logged in to add score to table
        if user[:4].lower() != "guest":
            add_score(user, "F", final_time)
        # Display score at the end
        img[ :, :, :] = 255
        cv2.putText(img, "Your final time is : ", (int(100*1.2) , int(200*1.2)), 1, 3, [0, 0, 0], 5)
        cv2.putText(img, str(final_time), (int(240*1.2), int(300*1.2)), 1, 5, [0, 0, 0], 5)
        cv2.imshow('Follow the position', img)
        key = cv2.waitKey(5000)
        if key == 32:
            print("You left")
            exit()

    # IF won = Flase
    else:
        # Display score at the end
        img[ :, :, :] = 255
        cv2.putText(img, "You lost!", (int(220*1.2) , int(220*1.2)), 1, 3, [0, 0, 0], 5)        
        cv2.imshow('Follow the position', img)
        key = cv2.waitKey(5000)
        if key == 32:
            print("You left")
            exit()

if __name__ == "__main__":
    main("Guest")

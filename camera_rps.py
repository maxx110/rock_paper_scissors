import random
from enum import IntEnum
from random import randint
import numpy as np
from keras.models import load_model
import cv2
import time

class items(IntEnum):
     Nothing =0
     Paper    =1
     Rock   =2
     Scissors=3



class game:
    def __init__(self):
        self.model = load_model('keras_model.h5', compile=False)
        self.cap = cv2.VideoCapture(0)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.round=0
        self.user_score=0
        self.computer_score=0

    def user_intro(self):
        self.user_name= input("Please enter your name: ")
        print(f"Welcome {self.user_name} to this game")
        return self.user_name



    def user_choices(self):
        prediction = self.model.predict(self.data)
        print(prediction)
        chooses = np.argmax(prediction[0])
        print(chooses)
        self.user_choice = items(chooses)
        print(self.user_choice)
        return self.user_choice

    def compu_prediction(self):
        comp_input=random.randint(1, len(items)-1)
        self.comp_pick= items(comp_input)
        print(self.comp_pick)
        return self.comp_pick

    def who_won(self,user_choice,comp_pick):
        if user_choice == comp_pick:
            self.winner="its a tire"
            self.round+=1
        elif user_choice == items.Rock and comp_pick == items.Scissors:
            self.winner=self.user_name
            self.user_score+=1
            self.round+=1

        elif user_choice == items.Rock and comp_pick == items.Paper:
            self.winner="computer"
            self.computer_score+=1
            self.round+=1
        
        elif user_choice == items.Paper and comp_pick == items.Rock:
            self.winner=self.user_name
            self.user_score+=1
            self.round+=1

        elif user_choice == items.Paper and comp_pick == items.Scissors:
            self.winner="computer"
            self.computer_score+=1
            self.round+=1

        elif user_choice == items.Scissors and comp_pick == items.Paper:
            self.winner=self.user_name
            self.user_score+=1
            self.round+=1

        elif user_choice == items.Scissors and comp_pick == items.Rock:
            self.winner="computer"
            self.computer_score+=1
            self.round+=1

        else:
            self.winner='No winner'
            print(self.winner)
            print('Play Aain')

        return self.winner

    def begin_game(self):
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        ret, self.frame = self.cap.read()
        #if self.frame is None:
        #    print('No image')
        #else:
        #    self.frame = self.frame[32:, 188:]
        #resize the frame
        resized_frame = cv2.resize(self.frame, (224,224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32)/127.0) - 1 #normalize the image
        self.data[0] = normalized_image
        #cv2.imshow('frame',self.frame)
        #cv2.waitKey(1)


        #initial instruction
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(self.frame, (10,10), (600,120), (255,255,0), -1)
        screen_message= "Current_Round: " + str(self.round) + " " + "Current Score" +str(self.user_score) + " CPU:" + str(self.computer_score)
        cv2.putText(self.frame, screen_message, (10,30), 1, 1.5, (0,0,0))
        cv2.putText(self.frame, "Press q to quit", (20,70), 1,1.5, (255,0,0))
        cv2.imshow("frame",self.frame)

    def end_game(self):
        self.cap.release()
        if self.computer_score == 3 or self.user_score == 3:
            print('Game over')
        else:
            print('you left the game')

        cv2.waitKey(1)
        cv2.destroyAllWindows()
        cv2.waitKey(1)

      



def play_game():
    game1=game()
    game1.user_intro()
    
    while True:
        count_time=5
        #open the game
        game1.begin_game()
        # press s to start the game

        if cv2.waitKey(80) & 0xFF == ord('s'):
            prev_time= time.time()
            while count_time > 0:
                game1.begin_game()
                cv2.putText(game1.frame, str(count_time), (190,420), 1, 1.5, (0,0,0))
                cv2.imshow('frame',game1.frame)
                cv2.waitKey(1)

                #count down
                current_time= time.time()
                if current_time - prev_time >=1:
                    prev_time = current_time
                    count_time -= 1

            else:
                user_input=game1.user_choices()
                compu_input=game1.compu_prediction()
                game1.who_won(user_input,compu_input)

                #output winner
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(game1.frame, f"{game1.user_name}'s choice : {game1.user_choice}",
                            (10, 200), font, 0.7, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(game1.frame, f"Computer's choice : {game1.comp_pick}",
                            (270, 200), font, 0.7, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(game1.frame, f"winner : {game1.winner}",
                            (10, 250), font, 1.2, (0,0,0), 1, cv2.LINE_AA)
                cv2.imshow('frame', game1.frame)
                cv2.waitKey(2000)

                if  game1.computer_score == 3:
                    game1.begin_game()
                    cv2.rectangle(game1.frame,(10,400), (150, 160), (180,170,50), -1)
                    cv2.putText(game1.frame, "Game Over", (10,400), 3 ,1, (0,0,0))
                    cv2.putText(game1.frame, "Computer wins over human", (10,450), 3 ,1, (0,0,0))
                    cv2.imshow('frame',game1.frame)
                    cv2.waitKey(6000)
                    game1.end_game()
                    break
                elif game1.user_score == 3:
                    game1.begin_game()
                    cv2.rectangle(game1.frame,(10,400), (150, 160), (180,170,50), -1)
                    cv2.putText(game1.frame, "Game Over", (10,400), 3 ,1, (0,0,0))
                    cv2.putText(game1.frame, "Congratulation You won", (10,450), 3 ,1, (0,0,0))
                    cv2.imshow('frame',game1.frame)
                    cv2.waitKey(6000)
                    game1.end_game()
                    break
               # if cv2.waitKey(1) & 0xFF == ord('q'):
                #        break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       
play_game()


            





    

    





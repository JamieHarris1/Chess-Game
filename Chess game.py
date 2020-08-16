import pygame
import os
import time

#pawn promotion
'''
-in gen moves not all checkmate avoiding move being removed
-make function to be used for replace main and gen moves looking if checkmate is there
'''
#castle
#stop moving piece leaving king in check
class Chess:

        def __init__(self):
                self.Board=[
                ['br1','bn1','bb1','bq','bk','bb2','bn2','br2'],
                ['bp1','bp2','bp3','bp4','bp5','bp6','bp7','bp8'],
                ['--','--','--','--','--','--','--','--'],
                ['--','--','--','--','--','--','--','--'],              #sets up 2d array of a 8x8 chess board
                ['--','--','--','--','--','--','--','--'],
                ['--','--','--','--','--','--','--','--'],
                ['wp1','wp2','wp3','wp4','wp5','wp6','wp7','wp8'],
                ['wr1','wn1','wb1','wq','wk','wb2','wn2','wr2'],
                ]
                self.pieces=['bp1','bp2','bp3','bp4','bp5','bp6','bp7','bp8','br1','br2','bn1','bn2','bb1','bb2','bq','bk','wp1','wp2','wp3','wp4','wp5','wp6','wp7','wp8','wr1','wr2','wn1','wn2','wb1','wb2','wq','wk']
                self.Move_Log=[]
                self.Dimensions=8
                self.Images={}
                self.Images_Selected={}
                self.Black_In_Check=False
                self.White_In_Check=False
                self.running=True
                self.Height=self.Width=512
                self.Sq_Size=self.Height//self.Dimensions               #divides 512 pixels into 8x8 divisible squares
                self.Colours=(pygame.Color('White'),pygame.Color('Grey'))
                self.White_Go=True
                self.King_Pos=[7,4],[0,4]
                self.Check_Counter=0
               
        def Load_Images(self):
                for Piece in self.pieces:
                        
                        
                        
                        self.Images[Piece]=pygame.image.load(f'/Users/jamieharris/Documents/Documents/Python_Projects/Chess/Images/{Piece[:2]}.png')                    #loads 2 lists of images
                        self.Images_Selected[Piece]=pygame.image.load(f'/Users/jamieharris/Documents/Documents/Python_Projects/Chess/Images/{Piece[:2]} copy.png')      #one is normla one is highlighted                      
        
        def Draw_Board(self):
                num=0
                for r in range(self.Dimensions):
                        for c in range(self.Dimensions):
                                self.Colour=self.Colours[((r+c)%2)]          #finds whole remainder, therefore alternates between 0 and 1
                                pygame.draw.rect(screen,self.Colour,pygame.Rect(c*self.Sq_Size,r*self.Sq_Size,self.Sq_Size,self.Sq_Size))    #
                                piece=self.Board[r][c]
                                if piece!='--':
                                        
                                        screen.blit(self.Images[piece],pygame.Rect(c*self.Sq_Size,r*self.Sq_Size,self.Sq_Size,self.Sq_Size))

        def Move(self,Current_R,Current_C,Piece_Moved,Next_R,Next_C,Piece_Left):

                Piece_Removed=self.Board[self.Next_R][self.Next_C]
                self.Board[self.Current_R][self.Current_C]=Piece_Left
                self.Board[self.Next_R][self.Next_C]=Piece_Moved

                
                Move=c.Move_Properties(Current_R,Current_C,Piece_Moved,Next_R,Next_C,Piece_Removed)
                self.Move_Log.append(Move)
                self.White_Go= not self.White_Go
                pygame.display.update()
                        
        def Undo(self):
                '''
                Move the most recently moved peiece back to where it came from
                Input the taken piece back onto the board
                '''

                
                Move=self.Move_Log.pop()
                
               
                self.Board[Move.Current_R][Move.Current_C]=Move.Piece_Moved
                self.Board[Move.Next_R][Move.Next_C]=Move.Piece_Removed
                self.White_Go=not self.White_Go
                
        def Swap_Current_Next(self):
                self.Next_R,self.Next_C,self.Current_R,self.Current_C=self.Current_R,self.Current_C,self.Next_R,self.Next_C
                
        def Find_Piece(self):
                Piece=self.Board[self.Current_R][self.Current_C]
                return Piece
        
        def Find_Click(self):
                Check1=False
                Check2=False
                pos = pygame.mouse.get_pos()
                for i in range(self.Dimensions):
                        if self.Sq_Size*i>pos[0] and Check1==False:
                                Column=i-1
                                Check1=True

                        if self.Sq_Size*i>pos[1] and Check2==False:
                                Row=i-1
                                Check2=True
                if Check1==False:
                        Column=self.Dimensions-1
                if Check2==False:
                        Row=self.Dimensions-1
                return [Row,Column]
           
        def Pawn_Check(self):
               
                if self.Current_C==self.Next_C:
                                if self.Colour=='w':
                                        
                                        if self.Next_R==4 or self.Next_R==self.Current_R-1:
                                                if self.Board[self.Next_R][self.Next_C]=='--':
                                                        
                                                        return True
                                                
                                        

                                else:
                                        if self.Next_R==3 or self.Next_R-1==self.Current_R:
                                                if self.Board[self.Next_R][self.Next_C]=='--':
                                                        return True


                
                if self.Next_C==self.Current_C+1 or self.Next_C==self.Current_C-1:
                        if self.Colour=='w':
                                if self.Next_R==self.Current_R-1:
                                        if self.Board[self.Next_R][self.Next_C]!='--' and self.Board[self.Next_R][self.Next_C][0]=='b':
                                                return True
                
                
                        else:
                                if self.Next_R==self.Current_R+1:
                                        if self.Board[self.Next_R][self.Next_C]!='--' and self.Board[self.Next_R][self.Next_C][0]=='w':
                                                return True

                return False
        
        def Rooke_Check(self):
                if self.Current_C==self.Next_C:
                        Row_Change=self.Next_R-self.Current_R
                        if Row_Change<0:
                                Row_Change=abs(Row_Change)
                                for i in range(Row_Change):
                                        Looking_Piece=self.Board[self.Current_R-i][self.Current_C]
                                        if Looking_Piece!='--' and Looking_Piece!=self.Board[self.Current_R][self.Current_C]:
                                                return False
                        else:
                                for i in range(Row_Change):
                                        Looking_Piece=self.Board[self.Current_R+i][self.Current_C]
                                        if Looking_Piece!='--' and Looking_Piece!=self.Board[self.Current_R][self.Current_C]:
                                                return False

                else:
                        Column_Change=self.Next_C-self.Current_C
                       
                        if Column_Change<0:
                                Column_Change=abs(Column_Change)
                                for i in range(Column_Change):
                                        Looking_Piece=self.Board[self.Current_R][self.Current_C-i]
                                        if Looking_Piece!='--' and Looking_Piece!=self.Board[self.Current_R][self.Current_C]:
                                                return False
                        else:
                                for i in range(Column_Change):
                                        Looking_Piece=self.Board[self.Current_R][self.Current_C+i]
                                        if Looking_Piece!='--' and Looking_Piece!=self.Board[self.Current_R][self.Current_C]:
                                                return False
                

                


                if self.Current_C==self.Next_C or self.Current_R==self.Next_R:
                        if (self.Colour=='w' and self.Board[self.Next_R][self.Next_C][0]=='b') or self.Board[self.Next_R][self.Next_C]=='--':
                                return True
                        elif (self.Colour=='b' and self.Board[self.Next_R][self.Next_C][0]=='w') or self.Board[self.Next_R][self.Next_C]=='--':
                                return True
                
        def Knight_Check(self):
                
                if self.Current_C-2==self.Next_C or self.Current_C+2==self.Next_C:
                        if self.Current_R+1==self.Next_R or self.Current_R-1==self.Next_R:
                                if (self.Colour=='w' and self.Board[self.Next_R][self.Next_C][0]=='b') or (self.Colour=='b' and self.Board[self.Next_R][self.Next_C][0]=='w'):
                                        return True
                                elif self.Board[self.Next_R][self.Next_C]=='--':
                                        return True
        

                if self.Current_R-2==self.Next_R or self.Current_R+2==self.Next_R:
                        if self.Current_C+1==self.Next_C or self.Current_C-1==self.Next_C:
                                if (self.Colour=='w' and self.Board[self.Next_R][self.Next_C][0]=='b') or (self.Colour=='b' and self.Board[self.Next_R][self.Next_C][0]=='w'):
                                        return True
                                elif self.Board[self.Next_R][self.Next_C]=='--':
                                        return True
                
        def Bishop_Check(self):
                Row_Change=self.Next_R-self.Current_R
                Column_Change=self.Next_C-self.Current_C
                pos=[self.Current_R,self.Current_C]
                Up=False
                Right=False
                if Row_Change<0:
                        Up=True
                if Column_Change>0:             #finds direction of travel
                        Right=True
                        
                
                

                if abs(Row_Change)==abs(Column_Change):
                        Check=False
                        while pos!=[self.Next_R,self.Next_C]:
                                
                                if self.Board[pos[0]][pos[1]]!='--' and Check==True:
                                        return False
                                if Up:
                                        pos[0]+=-1
                                else:
                                        pos[0]+=1
                                if Right:
                                        pos[1]+=1
                                else:
                                        pos[1]+=-1
                                Check=True
                        
                        
                        if (self.Colour=='w' and self.Board[self.Next_R][self.Next_C][0]=='b') or self.Board[self.Next_R][self.Next_C]=='--':
                                return True
                        elif (self.Colour=='b' and self.Board[self.Next_R][self.Next_C][0]=='w') or self.Board[self.Next_R][self.Next_C]=='--':
                                return True

        def King_Check(self):
                Row_Change=self.Next_R-self.Current_R
                Column_Change=self.Next_C-self.Current_C

                


                if (self.Colour=='w' and self.Board[self.Next_R][self.Next_C][0]=='b') or self.Board[self.Next_R][self.Next_C]=='--':
                        if abs(Row_Change)+abs(Column_Change)==1 or abs(Row_Change)+abs(Column_Change)==2:
                                return True
                                
                elif (self.Colour=='b' and self.Board[self.Next_R][self.Next_C][0]=='w') or self.Board[self.Next_R][self.Next_C]=='--':
                        if abs(Row_Change)+abs(Column_Change)==1 or abs(Row_Change)+abs(Column_Change)==2:
                                return True

        def Rule_Check(self,Piece):
                
                self.Colour=Piece[0]
                Piece=Piece[1]
                
                
                     

                if Piece=='p' :
                      
                        return c.Pawn_Check()
                if Piece=='r' :
                        
                        return c.Rooke_Check()
                if Piece=='n' :
                        
                        return c.Knight_Check()
                if Piece=='b' :
                        
                        return c.Bishop_Check()
                if Piece=='k' :
                        
                        return c.King_Check()
                if Piece=='q' :
                        
                        if c.Rooke_Check() or c.Bishop_Check():
                                return True
                
                

                
                

        
                return False

        def Can_Take_King(self):
                Piece=c.Find_Piece()
                Piece_Removed=self.Board[self.Next_R][self.Next_C]
                self.Current_Move=c.Move_Properties(self.Current_R,self.Current_C,Piece,self.Next_R,self.Next_C,Piece_Removed)
                
                

                self.White_Go=not self.White_Go

                for i in range(2):
                        
                        King_Pos=self.King_Pos[i]
                        


                        for Piece in self.pieces:
                                
                                Row=0
                                for i in self.Board:
                                        try:
                                                Pos=[Row,i.index(Piece)]
                                        except:
                                                pass
                                        Row+=1
                                
                                try:
                                        self.Current_R=Pos[0]
                                        self.Current_C=Pos[1]
                                        self.Next_R=King_Pos[0]
                                        self.Next_C=King_Pos[1]
                                except:
                                        pass
                                
                                        
                                
                               
                        
                                if c.Rule_Check(Piece):
                                        
                                        self.White_Go=not self.White_Go
                                        
                                         
                                        print('In Check')
                                        self.Check_Counter+=1
                                        pygame.display.update()

                                        return True,Piece[0]
                                c.Reset_Move()
                                
                self.Check_Counter=0
                self.White_Go=not self.White_Go 
                pygame.display.update()
                return False,None
        
        def Reset_Move(self):
                self.Current_R=self.Current_Move.Current_R
                self.Current_C=self.Current_Move.Current_C
                self.Next_R=self.Current_Move.Next_R
                self.Next_C=self.Current_Move.Next_C
                
        def Gen_Moves(self):
                Pieces=[]
                Moves=[]
                Valid_Moves=[]
                if self.White_Go:
                        Colour='w'
                else:
                        Colour='b'

                for Piece in self.pieces:
                        if Piece[0]==Colour:
                                Pieces=Pieces+[Piece]
                for Piece in Pieces:
                                
                        Row=0
                        for i in self.Board:
                                try:
                                        Pos=[Row,i.index(Piece)]
                                except:
                                        pass
                                Row+=1
                        try:
                                self.Current_R=Pos[0]
                                self.Current_C=Pos[1]
                        except:
                                pass

                        for Row in range(8):
                                self.Next_R=Row
                                for Column in range(8):
                                        self.Next_C=Column
                                        
                                        if c.Rule_Check(Piece):
                                                
                                                Piece_Removed=self.Board[Row][Column]
                                                Move=c.Move_Properties(self.Current_R,self.Current_C,Piece,self.Next_R,self.Next_C,Piece_Removed)
                                                Moves=Moves+[Move]
                
                                
                for Move in Moves:
                        
                        self.Current_R=Move.Current_R
                        self.Current_C=Move.Current_C
                        self.Next_R=Move.Next_R
                        self.Next_C=Move.Next_C
                        
                        
                        c.Move(Move.Current_R,Move.Current_C,Move.Piece_Moved,Move.Next_R,Move.Next_C,Move.Piece_Removed)
                        
                        if not c.Can_Take_King()[0]:
                                Valid_Moves=Valid_Moves+[Move]
                        
                        c.Undo()
                        pygame.display.update()
        
                if len(Valid_Moves)==0:
                        print('Checkmate')
                return Valid_Moves
                
        def Main(self):
                Check=False
                pygame.init()
                global screen
                Counter=0
                screen=pygame.display.set_mode((self.Width,self.Height))
                clock=pygame.time.Clock()
                Mouse_Down=False
                Selected=False
                while self.running:
                        King_Into_Check=False
                        events = pygame.event.get()
                        Check=False

                        

                        for event in events:
                                if event.type==pygame.QUIT:
                                        self.running=False
                                elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                                c.Gen_Moves()
                                
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                
                                        if Selected==True:
                                                End_Sq=c.Find_Click()
                                                self.Next_R=End_Sq[0]
                                                self.Next_C=End_Sq[1]
                                                
                                                if self.Board[self.Current_R][self.Current_C]!='--':
                                                        Selected=False
                                                        Mouse_Down=True
                                                        if (Piece[0]=='w' and self.White_Go==True)  or (Piece[0]=='b' and self.White_Go==False):
                                                                Piece=c.Find_Piece()
                                                                self.Images[Piece]=Temp_Image

                                                        Piece_Removed=self.Board[self.Next_R][self.Next_C]
                                                        
                                                        self.Current_Move=c.Move_Properties(self.Current_R,self.Current_C,Piece,self.Next_R,self.Next_C,Piece_Removed)
                                                        
                                                        
                                                        
                                                        
                                                        if c.Rule_Check(Piece):
                                                                if self.White_Go:
                                                                        Colour='b'
                                                                else:
                                                                        Colour='w'


                                                                if Piece[1]=='k':
                                                                       
                                                                        if Piece[0]=='w':
                                                                                
                                                                                self.King_Pos=[self.Next_R,self.Next_C],self.King_Pos[1]
                                                                        else:
                                                                                self.King_Pos=self.King_Pos[0],[self.Next_R,self.Next_C]
                                                              
                                                                        c.Move(c.Current_Move.Current_R,c.Current_Move.Current_C,Piece,c.Current_Move.Next_R,c.Current_Move.Next_C,'--')
                                                                        Check=c.Can_Take_King()[0]
                                                                        c.Undo()
                                                                        if Check:
                                                                                King_Into_Check=True
                                                                
                                                                if not King_Into_Check:
                                                                        c.Move(c.Current_Move.Current_R,c.Current_Move.Current_C,Piece,c.Current_Move.Next_R,c.Current_Move.Next_C,'--')
                                                                        Check,Who_In_Check=c.Can_Take_King()
                                                                        
                                                                        print(Who_In_Check)
                                                                        if (Check and self.Check_Counter>1) or (Check and Who_In_Check==Colour):
                                                                                c.Undo()
                                                                                if Check and len(c.Gen_Moves())==0 and self.Check_Counter:
                                                                                        print('Good game')   
                                                                        
                                                                
                                                                                
                                                               
                                                        
                                                                
                                                        
                                                         

                                        else:
                                                Start_Sq=c.Find_Click()
                                                self.Current_R=Start_Sq[0]
                                                self.Current_C=Start_Sq[1]
                                                if self.Board[self.Current_R][self.Current_C]!='--':
                                                
                                                        Selected=True
                                                        Piece=c.Find_Piece()
                                                        if (Piece[0]=='w' and self.White_Go==True)  or (Piece[0]=='b' and self.White_Go==False):
                                                                
                                                                Temp_Image=self.Images[Piece]
                                                                self.Images[Piece]=self.Images_Selected[Piece]  
                        
                                        
                                        
                                        
                                
                                                
                                                
                                


                       

                                

                        c.Draw_Board()
                        clock.tick(60)
                        pygame.display.flip()
        
        class Move_Properties:
                def __init__(self,Current_R,Current_C,Piece_Moved,Next_R,Next_C,Piece_Removed):
                        self.Current_R=Current_R
                        self.Current_C=Current_C
                        self.Next_R=Next_R
                        self.Next_C=Next_C
                        self.Piece_Removed=Piece_Removed
                        self.Piece_Moved=Piece_Moved
                
                def Properties(self):
                        print(
                        self.Current_R,
                        self.Current_C,
                        self.Next_R,
                        self.Next_C,
                        self.Piece_Moved,
                        self.Piece_Removed
                        )
                        
        
c=Chess()
c.Load_Images()
c.Main()

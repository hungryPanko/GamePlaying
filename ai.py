import time
import random 
import io

# global var, number of stone per bin for the test purpose
nSTONE = 6

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass

    class state:
        # Kalah:
        #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
        # b_fin                                         a_fin
        #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    ########################################################
    # Check the game is end
    # arguments: a_fin(kalah of a), b_fin(kalha of b)
    # Return values: True(game is end), False(Not end)
    ########################################################
    def isEnd(self, a_fin, b_fin): 
        if a_fin >= nSTONE*6 or b_fin>=nSTONE*6: #If one of kalah is more than half of all stones, games end
            return True
        else:
            False

    ########################################################
    # If a wins, return inf. If b wins, return -inf
    # arguments: a_fin(kalah of a), b_fin(kalha of b)
    # Return values: Inf(win), -Inf(loss), 0(draw) 
    ########################################################
    def getEndValue(self, a_fin, b_fin):
        if a_fin > nSTONE*6: # If a wins, A kalha(a_fin) is bigger than half of all stones
            return float('inf') # Inf for you win
        if b_fin > nSTONE*6: # If b wins, A kalha(b_fin) is bigger than half of all stones
            return float('-inf') # -Inf for you loss
        if a_fin == nSTONE*6 and b_fin == nSTONE*6: # If A and B have same kalah, it is tie
            return 0 # 0 for tie
        return 0 # Exception

    ########################################################
    # Return string of a, a_fin, b, b_fin
    # The string used for the test purporse. (Useful in print) 
    # arguments: a, b, a_fin, b_fin
    # Return values: String eg. 0,1,0,4,3,0#36#0,0,0,0,1,0#27
    ########################################################
    def strState(self, a, b, a_fin, b_fin):
        s = str(a[0]) + ',' + str(a[1]) + ',' + str(a[2]) + ',' + str(a[3]) + ',' + str(a[4]) + ',' + str(a[5]) + '#' \
               + str(a_fin) + '#' + str(b[0]) + ',' + str(b[1]) + ',' + str(b[2]) + ',' + str(b[3]) + ',' + str(b[4]) + ',' + \
               str(b[5]) + '#' + str(b_fin)
        return s

    ########################################################
    # Swap between a and b. Swap a_fin and b_fin
    # This can be used alternating between MAX and MIN node 
    # a->b, b->a, a_fin->bfin, b_fin->a_fin
    # arguments: a, b, a_fin, b_fin
    # Return values: a, b, a_fin, b_fin
    ########################################################
    def swap(self, a, b, a_fin, b_fin):
        c=a[:]
        a=b[:]
        b=c[:]
        c = a_fin
        a_fin = b_fin
        b_fin = c
        return a, b, a_fin, b_fin

    ########################################################
    # Return the possible move of 'a' select the 'move'.
    # It returns the next position of a, b, a_fin, b_fin
    # Also, check that the move gives 'again' chance and 'eat' status 
    # arguments: a, b, a_fin, b_fin, move
    # Return values: a, b, a_fin, b_fin, 
    #                cagain(last stone ends up to a_fin)
    #                ceat(last stone eats the opposite stone)
    ########################################################
    def possibleMove(self, a, b, a_fin, b_fin, move):
        ao = a[:]
        all = a[move:] + [a_fin] + b + a[:move]
        count = a[move]
        all[0] = 0
        p = 1
        while count > 0:
            all[p] += 1
            p = (p + 1) % 13
            count -= 1
        a_fin = all[6 - move]
        b = all[7 - move:13 - move]
        a = all[13 - move:] + all[:6-move]
        cagain = bool()
        ceat = False
        p = (p - 1) % 13
        if p == 6 - move:
            cagain = True
        if p <= 5 - move and ao[move] < 14:
            id = p + move
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        elif p >= 13 - move and ao[move] < 14:
            id = p + move - 13
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        if ceat:
            a_fin += b[5-id]+1
            b[5-id] = 0
            a[id] = 0
        if sum(a)==0:
            b_fin += sum(b)
        if sum(b)==0:
            a_fin += sum(a)

        return a, b, a_fin, b_fin, cagain, ceat

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        """
        # This is for the test to to see the time depending on the depth of the tree. 
        f = open('time.txt', 'a')
        for depth in [3, 5, 7, 9, 11, 13, 15, 17]:
            f.write('depth = '+str(depth)+'\n')
            t_start = time.time()
            [v, action] = self.minimax(a, b, a_fin, b_fin, d=depth)  # to do d_limit
            f.write(str(time.time()-t_start)+'\n')

            a, b, a_fin, b_fin = self.swap(a, b, a_fin, b_fin)
            print("depth: ", depth)
            print(" =="+self.strState(a, b, a_fin, b_fin)+", "+"action: "+str(action)+", v: "+str(v))
            a, b, a_fin, b_fin = self.swap(a, b, a_fin, b_fin)
            print(str(time.time()-t_start)+"\n")
        f.close()
        return action
        """
        # The timing variable used for return immediately if it exceeds the time limit
        global start_t
        start_t = time.time()
        global limit_t
        #limit_t = t #This is for the general API. API sends t (500ms, 1sec, 5sec etc)
        limit_t = 900  # This is for the tornament game. Time restrcition is 1 sec. I used 900ms for the call back and buffer. 

        # Main algorithm
        [v, action] = self.minimax(a, b, a_fin, b_fin, d=7) 

        return action
        

    ############################################################
    # Wrapper function for min max. We call Max first. 
    # Double check for illegal move. (exception) 
    # arguments: a, b, a_fin, b_fin, d(tree depth limit)
    # Return values: v(Utility of best move), action(best move)
    ############################################################
    def minimax(self, a, b, a_fin, b_fin, d):
        # Call the max first 
        [v, action] = self.max(a, b, a_fin, b_fin, depth=0, d_limit=d) #first depth is 0, d_limit is given.
        
        # Double check the illegal move
        r = [] # r has possible move
        for i in range(6):
            if a[i] != 0:
                r.append(i)
        if not action in r: # In case of illega move return the last move in the possible move
            v = 0
            action = r[-1]
        return [v, action] # return next action

    ############################################################
    # This is the main search. Minimax with alpha beta pruning. 
    # Select the child that gives the max utility. 
    # arguments: a, b, a_fin, b_fin, depth(current dpeth), 
    #            d_limit(tree depth limit), alpha,beta for purning
    # Return values: v(Utility of best move), action(best move)
    ############################################################
    def max(self, a, b, a_fin, b_fin, depth, d_limit, alpha=None, beta=None):
        # check the end state, if it is end return the utility
        if self.isEnd(a_fin, b_fin):
            #print("leaf "+self.strState(a, b, a_fin, b_fin)+" "+str(self.getEndValue(a_fin, b_fin)))
            return [self.getEndValue(a_fin, b_fin), -1] #return [v, action]
        
        # check all possible move from current state
        r = [] # r has possible move
        for i in range(6):
            if a[i] != 0:
                r.append(i)
        
        # Adjust depth limit, close to the end of game, search more. 
        if depth<=1 and a_fin+b_fin >= nSTONE*nSTONE:
            d_limit = (a_fin+b_fin)//nSTONE + 2

        # We call heuristic at the first move for 'again' chance and capturing opp stones. 
        # Toward the end of game, we don't use heuristic and rely on the minimax
        depth += 1
        if depth == 1 and a_fin+b_fin<=50:
            v, action = self.heuristic_max(a, b, a_fin, b_fin)
            if v > 0:
                return v, action 
        
        # If depth is more than limit, return the utility (a_fin-b_fin)
        # MAX tries to maximize the difference b_fin and b_fin
        elapsed_time = time.time() - start_t # Return immediate if it exceeds the time limit. 
        if depth>=d_limit or elapsed_time*1000>=limit_t: 
            return [a_fin-b_fin, 0] 

        v = float('-inf') # v = -inf (utility)
        action = None # possible action init
        for move in r: # for all succ
            a_, b_, a_fin_, b_fin_, cagain, ceat = self.possibleMove(a, b, a_fin, b_fin, move) # should get new position from the current state            
            if cagain: #if do game again, call the max
                if depth < d_limit:
                    v = self.max(a_, b_, a_fin_, b_fin_, depth, d_limit)[0]
                action = move # update move in the leaf node
            else:
                v_ = self.min(a_, b_, a_fin_, b_fin_, depth, d_limit, alpha, beta)[0]
                if v_ >= v: # Choose MAX 
                    v = v_
                    action = move
                # alpha beta pruning 
                if beta is not None and v_>=beta: # if v_>= beta, return v
                    return [v, move] 
                if alpha is None or v_>alpha: #if v_>=alpha, a=v_
                    alpha = v_
            
        #print("max "+self.strState(a, b, a_fin, b_fin)+" depth: "+str(depth)+"/"+str(d_limit)+" v:"+str(v))
        return [v, action]

    ############################################################
    # This is the main search. Minimax with alpha beta pruning. 
    # Select the child that gives the min utility. 
    # We assumes that opponent against me. 
    # arguments: a, b, a_fin, b_fin, depth(current dpeth), 
    #            d_limit(tree depth limit), alpha, beta for purning
    # Return values: v(Utility of best move), action(best move)
    ############################################################
    def min(self, a, b, a_fin, b_fin, depth, d_limit, alpha=None, beta=None):
        # check the end state, if it is end return the utility
        if self.isEnd(a_fin, b_fin):
            #print("leaf "+self.strState(a, b, a_fin, b_fin)+" "+str(self.getEndValue(a_fin, b_fin)))
            return [self.getEndValue(a_fin, b_fin), -1] #return [v, action]

        # check all possible move from current state
        r = [] # r has possible move
        for i in range(6):
            if b[i] != 0:
                r.append(i)
        
        depth += 1
        # If depth is more than limit, return the utility (a_fin-b_fin)
        # MIN tries to minimize the difference b_fin and b_fin
        elapsed_time = time.time() - start_t # Return immediate if it exceeds the time limit. 
        if depth>=d_limit or elapsed_time*1000>=limit_t: 
            return [a_fin-b_fin, 0] 
            
        v = float('inf') # v = inf (utility)
        action = None #possible action init
        for move in r: # for all succ  
            a, b, a_fin, b_fin = self.swap(a, b, a_fin, b_fin)
            a_, b_, a_fin_, b_fin_, cagain, ceat = self.possibleMove(a, b, a_fin, b_fin, move) # should get new position from the current state
            a, b, a_fin, b_fin = self.swap(a, b, a_fin, b_fin)
            a_, b_, a_fin_, b_fin_ = self.swap(a_, b_, a_fin_, b_fin_)

            if cagain: #if do game again, call the min
                v = self.min(a_, b_, a_fin_, b_fin_, depth, d_limit)[0]
                action = move # update move in the leaf node
            else:
                v_ = self.max(a_, b_, a_fin_, b_fin_, depth, d_limit, alpha, beta)[0]
                if v >= v_: # Choose min
                    v = v_
                    action = move
                # alpha beta pruning 
                if alpha is not None and v_<=alpha: #if v_<= a, return v
                    return [v, move]
                if beta is None or v_<beta: #if v_<beta, b=v_
                    beta = v_

        #print("min "+self.strState(a, b, a_fin, b_fin)+" depth: "+str(depth)+"/"+str(d_limit)+" v:"+str(v)) 
        return [v, action]

    ############################################################
    # At root node, we first priotize the 'again' and 'eat chance.
    # It gives utility based on the next move without branching out. 
    # More hueristic on eat, again move. 
    # arguments: a, b, a_fin, b_fin
    # Return values: v(Utility of best move), action(best move)
    ############################################################
    def heuristic_max(self, a, b, a_fin, b_fin):
        r = [] # r has possible move
        for i in range(6):
            if a[i] != 0:
                r.append(i)
        
        # Without Heuristic, return the random number for the experiment
        #action = r[random.randint(0, len(r)-1)]
        #v = 0
    
        # With Heuristic
        v = float('-inf') # v = -inf (utility) for init
        v_ = 0
        action = r[0] # possible action init
        for move in r: # for all succ
            # should get new position from the current state      
            a_, b_, a_fin_, b_fin_, cagain, ceat = self.possibleMove(a, b, a_fin, b_fin, move)       
            if cagain or ceat: # if I can have good two choices(again, eat), choose better one
                if cagain: 
                    v_ = 200
                if cagain and a[5]==1 and a_[5]==0: # if a[5] has 1 stone, we can do again,
                    v_ = 1000
                if cagain and a[4]==2 and a_[4]==0: # if a[4] has 2 stones, we can do again. 
                    v_ = 900
                if cagain and a[3]==3 and a_[4]==0: # if a[3] has 3 stones, we can do again. 
                    v_ = 800 
                if cagain and a[2]==4 and a_[2]==0: # if a[2] has 4 stones, we can do again. 
                    v_ = 700
                if cagain and a[1]==5 and a_[1]==0: # if a[1] has 5 stones, we can do again. 
                    v_ = 600
                if cagain and a[0]==6 and a_[1]==0: # if a[0] has 6 stones, we can do again. 
                    v_ = 500
                if ceat and a_fin_-a_fin>=3: # give more priority to ceat
                    v_ = 100*(a_fin_ - a_fin)

            if v_ >= v: # Choose MAX 
                v = v_
                action = move    

        return [v, action]
        




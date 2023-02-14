# GamePlaying
[Kalah Game] MiniMax + Alpha Beta Pruning + Heuristic


[ Description of the game ]
The board has 6 small pits, called houses, on each side; and a big pit, called a Kalah, at each end. The object of the game is to capture more seeds than one's opponent.
Game rule:
At the begging of the game, each player has 6 holes and a Kalah as shown in the lecture slides.
A turn consists of selecting one of your own holes, picking up all the stones, and distributing them in each consecutive hole, including your Kalah but not the opponent's Kalah, in the counterclockwise direction.
You get an extra turn if your last stone lands in your own Kalah.
If your last stone lands in your own empty hole, you take all the stones in the opponent's opposite hole and put them in your Kalah. You will also place your last stone in your Kalah. If you cannot capture any of your opponent's stones, because you landed across from an empty hole, leave your last stone where it is and do not move it to your Kalah.
If you run out of stones on your side, the opponent takes all the stones left on his side and puts them in his Kalah


[ Description of the AI agent ]
AI agent plays the Kalah game. It tries to win against a human player or the other AI agent. AI agent deploys Minimax with alpha-beta pruning algorithms. At the first AI’s move, it first prioritizes the ‘catch’ and ‘again’ chance on its possible move at the heuristic function. The search is limited by the given search limit to save the runtime. If the search exceeds the search limit, the difference between AI’s Kalah and the opponent’s Kalah is at the given node and returns the value to its parent node without branching out to the game-end state. The tree search depth limit is adjusted on runtime doing a shallow search at first and a deep search toward the end of the game. Also, AI returns the action immediately if it exceeds the time limit.
When running the minimax algorithm, it is assumed that AI’s opponent is playing against AI. Alpha-beta pruning decrease the number of searches. It stops evaluating a move when at least one possibility has been found that proves the move to be worse than a previously examined move. Such moves need not be evaluated further. It returns the same move as minimax would, but prunes away branches that cannot possibly influence the final decision.

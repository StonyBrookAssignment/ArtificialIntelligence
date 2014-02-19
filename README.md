ArtificialIntelligence
======================

Assignments
PROJECT REPORT ARTIFICIAL INTELLIGENCE
Project-2 MULTI-AGENT Pac-Man
By:- Rohan Mehta (108648007) Manish Chhabra (109136341) Group-23
Our Submission includes this report and files name multiagent.py. We have properly commented the code, comments specify our approach on each step. You will see comments in # tag above each statement to make understand anyone about our approach.
We have implemented Reflex Agent, Mini max Agent and alpha-beta pruning on Pac-man search. Let us see now, the stats for each of them.
Implementations:-
1) ReflexAgent:-
In this we had to improve the reflex agent code already made available to us. Proper commenting in code is done to explain our approach.
HEURISTIC:-
Scores are computes using evaluation function which is called in the getAction function, so we make changes in the evaluation function in such a way it is optimized for the reflex agent.
Here, we have our food list as well as the Ghost states which can be derived by formulae’s provided. So we maintain two lists, where in one we maintain distance to Ghost and in other we maintain distance to food from Pac man. We compute this using Manhattan distance. Proper commenting line by line is provided for clear understanding.
Once we have list of all the distances, we find the minimum of both the list.
Two points to keep in mind:-
1) We have to maintain distance to food near so that we can eat as much food as
possible. So, we consider the fraction of minimum Distance to food to increase the
probability of eating that food as mentioned in the hints of question.
2) Also, distance to ghost we have to maintain, so we consider it’s whole value so that
Pac man remains away from the ghost.
So our Heuristic, computes (min(DistanceToGhost) * FoodFactorLess) where FoodFactorLess is the fraction of the min food we obtained. Hence keeping the food near and ghost away. This value is incrementally added to our heuristic to obtain the optimum path.
Also, program by default return score, so in order to incorporate that , we have to add that factor to our final heuristic like heuristic + successorGameState.getScore()
IMPORTANT:-
Our heuristic checks, if distance to ghost is less than 2, that is Ghost is near that radius, we assign our heuristic some large negative value so it doesn’t meet the ghost and takes some arbitrary path not of ghost.
Let us see the stats for reflex agents:-
a) python pacman.py -p ReflexAgent -l testClassic
   Pacman emerges victorious! Score: 562
   Average Score: 562.0
Scores:
Win Rate:
Record:
562.0
1/1 (1.00)
Win
b) python pacman.py --frameTime 0 -p ReflexAgent -k 1
This maze our agent finishes quickly and emerges victorious
   Pacman emerges victorious! Score: 1030
   Average Score: 1030.0
Scores:
Win Rate:
Record:
1030.0
1/1 (1.00)
Win
c) python pacman.py --frameTime 0 -p ReflexAgent -k 2
This maze our agent finishes quickly and emerges victorious
   Pacman emerges victorious! Score: 1372
   Average Score: 1372.0
Scores:
Win Rate:
Record:
1372.0
1/1 (1.00)
Win
Our Agent fare very well in case of the last board. Yes, it does sometimes dies too, but it often wins and it shoes, or evaluation function is good.
We made use of hints in the question of reversing the distance to food, and evaluating state- action pairs.
But, it doesn’t run for directional ghost and our agent eventually dies in that case.
d) python pacman.py -p ReflexAgent -l openClassic -n 10 -q
Pacman emerges victorious! Score: 947 Pacman emerges victorious! Score: 746 Pacman emerges victorious! Score: 754 Pacman emerges victorious! Score: 402 Pacman emerges victorious! Score: 666 Pacman emerges victorious! Score: 755 Pacman emerges victorious! Score: 482 Pacman emerges victorious! Score: 623 Pacman emerges victorious! Score: 426 Pacman emerges victorious! Score: 797 Average Score: 659.8
Scores: 947.0, 746.0, 754.0, 402.0, 666.0, 755.0, 482.0, 623.0, 426.0, 797.0 Win Rate: 10/10 (1.00)
Record: Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
Here we see, our agent can rapidly clear the openClassic layout ten times without dying more than twice or thrashing around infinitely (i.e. repeatedly moving back and forth between two positions, making no progress).
Note:- Sometimes, one or more scores are negative, but our agent does clear the layout and wins.
2) MultiAgent:-
In this we had to write mini max general version of the algorithm provided in the textbook. Proper commenting in code is done to explain our approach. We made changes to MiniMaxAgent stub class.
Heuristic:-
We consider Pac man game where pac-man our agent is on depth 0. Now, for every pac man move there will be move for all the ghost in the game. For-example:- if depth is 4, at depth 0 pac-man moves, now for that depth, we need to move number ghost (each ghost). Once, moves are done, we increment the depth to 1 and move pac man and then corresponding to that we keep moving ghost for that level. In this way, once depth equals the depth we passed through command line, game stops, and return the score for the game.
Each situation is explained and carried out in code with proper documentation. We have taken care pf every hint and observations to carry out this task.
Algorithm:-
1) In out Mini Max stub class, we specify for each legal moves, a Min function in which
we initially pass depth as 0 and agent index as 1 as pac man has made his legal move
and now, Min is called for Ghost to run.
2) In min function, for each legal move of every Ghost, we see whether agent Index is
equal to number of ghost or it is less than that. If it is less than ghost, that means, we still are on same depth, so we need to recursively call min function foe every ghost keeping depth constant.
3) Else, when it becomes equal to ghost, that means, depth is covered, we need to increment the depth and move the pacman, so we call Max function with index =0 meaning pac man on depth +1.
4) Max in return call recursively the min function and keep performing the same logic.
5) Once, we return the values to the get Action back, we compute the maximum of that value that is the best score and compute the best move according to that score
and return that.
6) Hence, our algorithm runs well.
Let us see the stats:-
a) python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
   Pacman emerges victorious! Score: 516
   Average Score: 516.0
Scores:
Win Rate:
Record:
516.0
1/1 (1.00)
Win
If we try computing multiple times, it runs and pac man emerge victorious and sometimes also loses. As mentioned in the question, the rate is 665/1000 wins for pac man. Let us see what we got.
b) python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4 -n 1000 –q
         We get Win Rate:      787/1000 (0.79)
There were 1000 values, so we didn’t mention it on report, but this was our result.
c) python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
In this case, our pac man always dies, as it is in trapped state, and it runs towards the closest ghost, because it wants to end the game as soon as possible. So it runs towards the minimum distance ghost as it believes that death is unavoidable.
Note:- To increase the search depth achievable by our agent, we removed the Directions.STOP action from Pac-Man's list of possible actions.
Observations:-
On larger boards such as openClassic and mediumClassic (the default), we find that Pac-Man to be good at not dying, but quite bad at winning. He often thrash around without making progress. He also even thrash around right next to a dot without eating it because he doesn't know where he'd go after eating that dot. So, we also got this observation true.
3) Alpha Beta Pruning :-
In this wrote alpha-beta pruning algorithm provided in the textbook. Ours is as usual general as compared to the textbook as we have consider multiple ghost. Proper commenting in code is done to explain our approach. We made changes to AlphaBetaAgent stub class.
The code logic flows same as explained in the mini max, we just have to introduce alpha and beta variables into the function and use them to compare from our scores and then
replace them each time in the recursive function, thereby neglecting visiting the part of tree which has values not needed to be visited, hence pruning the graph.
We assign alpha and beta as minus infinity and beta to be infinity as defined in he algorithm in the class. Now we have to increase alpha and decrease beta and find the optimal path, so that we can prun the graph.
1) We pass alpha and beta as additional arguments in the min function in get Action. The flow is same as explained above.
2) Only difference lies, when minval function is called, they return a min score based on the conditions specified above, then we check, if score is less than alpha, if it is then we return score. But if not we compute minimum of score and beta and then replace it with beta, and return score. So this way initially alpha comes with - infinity and beta as infinity. Here beta value changes, if score is less than beta value. Replacing is done and fed into the function back again. Recursive calls are made again and again and keeps updating the score at each depth and returning the values.
3) Same is the case of max function, where we consider alpha and we compute maximum of alpha and replace it with the older value. Recursive calls are made here too as above.
4) Now, once the list of values is returned back to get Action we need to compute best move there based on that and then update the value of alpha. That is done in get action after function ends.
5) Then we return the bestMove.
Let us see the stats :-
a) python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
Pacman died! Score: -167
Pacman died! Score: -289
Pacman emerges victorious! Score: 1240 Pacman emerges victorious! Score: 1378 Pacman emerges victorious! Score: 825 Pacman emerges victorious! Score: 1098 Pacman died! Score: -101
Pacman died! Score: 82
Pacman emerges victorious! Score: 913 Pacman emerges victorious! Score: 950 Average Score: 592.9
Scores: Win Rate: Record:
-167.0, -289.0, 1240.0, 1378.0, 825.0, 1098.0, -101.0, 82.0, 913.0, 950.0 6/10 (0.60)
Loss, Loss, Win, Win, Win, Win, Loss, Loss, Win, Win
We see, we do lose, as evaluation function is not in our hand, when pacman is trapped, it dies.

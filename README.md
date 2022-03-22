# Documentation exercise 05
###### Written by Marián Šebeňa
###### Python Interpreter 3.9
### Assigment 
You can find assigment on this  **[link](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/).** 
#### Short description 
According to the lecture, implement a solution to the problem of smokers. 
In the case of a modification in which the agent is not waiting for 
signaling of resource allocation, solve the problem of favoring smokers
and describe this solution in the documentation in an appropriate manner.
### Resources
When you click on links below you will be redirected on resource web page: </br>
**[PPDS Youtube channel](https://www.youtube.com/channel/UCnTxtvNFlicb2Mn0a6w8N-A)** <br/>
**[UIM/PPDS](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F)** <br/>

### Smokers
We want to implement problem of smokers. There are three deeply addicted smokers. Every
of smoker has infinite amount of one component. First smoker has tobacco, second paper and third has matches.
Next we have agent who delivers two of mentioned components. We want to secure that only smoker
who has missing component could take these two from agent and smoke.
###### Naive solution
Firstly we implemented naive solution from lecture. We have three agents threads who
deliver every possible combination(tobacco, paper)(tobacco, matches)(paper, matches). Next
we have three smokers threads for each component. And as we mentioned we want to secure that
only smoker with agent's missing component could take resources. Solution is pretty easy
but not correct. Let's look on example explanation.

As example, we choose agent who delivers tobacco and paper.

Agent locks access to other agents and release tobacco and paper.
```
shared.agentSem.wait()
shared.tobacco.signal()
shared.paper.signal()
```
Then we can see that smoker who have infinite amount of matches make cigarette and 
release agent who deliver missing components and start smoke. 
```
shared.tobacco.wait()
shared.paper.wait()
make_cigarette()
shared.agentSem.signal()
smoke()
```
It looks pretty cool and correct. But in our opinion could occur a situation when other thread
could overrun this thread and go through first wait. And in next iteration don't control two missing
resources but only one and the problem turns out.

##### Advanced solution

To avoid problem we mentioned let's look on Mgr. Ing. Matúš Jókay, PhD. solution from lecture. After all we added to
previous solution another three threads of dealers. Why? Because we want control which components are free and which
are already use. In first case we use boolean values to control it, but it's not enough. Because real operating system 
just provides resources and doesn't wait. Then we have to replace true/false values by numbers, and then we have complete
information about provided resources.

##### Threads advantage

The last thing we consider is advantage of some threads. We add to object shared three variables to count how many
cigarettes produce each smoker. Then we print values always when smoker produce cigarette 
```
self.made_tobacco = 0
self.made_match = 0
self.made_paper = 0
.
.
.
print(f"cigarettes made: tobacco:{shared.made_tobacco} "
      f"paper:{shared.made_paper} match:{shared.made_match}")
```
<b>Conclusion:</b> After small resource you can see below. We can't 100% say that depends on order of comparison in 
pusher's functions, but most of the time when resource always compares first reach 100 cigarettes first. On the other hand when
resource compares first just once from 3 experiments we have 3 different resolutions.

```
Tobacco always compare as first
exp1: cigarettes made: tobacco:100 paper:87 match:91
exp2: cigarettes made: tobacco:97 paper:96 match:100
exp3: cigarettes made: tobacco:100 paper:95 match:92

Paper always compare as first
exp1: cigarettes made: tobacco:96 paper:100 match:94
exp2: cigarettes made: tobacco:100 paper:100 match:96
exp3: cigarettes made: tobacco:99 paper:100 match:92

Match always compare as first
exp1: cigarettes made: tobacco:86 paper:90 match:100
exp2: cigarettes made: tobacco:98 paper:96 match:100
exp3: cigarettes made: tobacco:95 paper:96 match:100

Match, Tobacco, Paper start once
exp1: cigarettes made: tobacco:93 paper:96 match:100
exp2: cigarettes made: tobacco:100 paper:99 match:98
exp3: cigarettes made: tobacco:97 paper:100 match:93
```
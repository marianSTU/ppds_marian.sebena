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




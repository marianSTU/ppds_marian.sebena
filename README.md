# Documentation exercise 02  
###### Written by Marián Šebeňa
###### Python Interpreter 3.9
### Assigment 
You can find assigment on this  **[link](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F).** 
#### Short description 
Implement ADT SimpleBarrier as specified in the lecture. 
In it, we used ADT Semaphore for synchronization. After successful implementation in this way, 
try to use event signaling to implement the turnstile. For simplicity, we enclose a framework / implementation 
scheme in Python: </br> </br>
To further test the ADT SimpleBarrier, implement a reusable barrier as specified in the lecture. </br> </br>
Create N threads. Let i represent a node in which the element at position i + 2 of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21…) is calculated. Let all threads share a common list in which the calculated sequence elements are stored sequentially during the calculation. Let the first two elements 0 and 1 be fixed in this list. Use the synchronization tools you have downloaded so far to design a synchronization so that thread i + 2 can calculate the Fibonacci number it assigns only after it stores its results in the list of threads that calculate previous sequence numbers (that is, after the i and i + 1 threads are finished). Don't forget extreme cases when synchronizing!
Use semaphore first to sync. Then create a second version with events.
### Resources
When you click on links below you will be redirected on resource web page: </br>
**[PPDS Youtube channel](https://www.youtube.com/channel/UCnTxtvNFlicb2Mn0a6w8N-A)** <br/>
**[UIM/PPDS](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F)** <br/>
**[Semaphores in Process Synchronization](https://www.geeksforgeeks.org/semaphores-in-process-synchronization/)** <br/>

### Barriers
Simply barriers are good to understand. But when I tested code there were a lot of situations where program should not
work, but surprisingly worked and in opposite way too.
First implementation was simple barrier without loop. This Semaphore release threads randomly.
In next implementation we try barrier inside a loop. We noticed problem with one barrier, that did not occur on lecture. In my
machine on 3.9 interpreter this problem occurred. When we implement second barrier code worked correctly. In last implementation 
we tried to replace logic with semaphore with events. But we noticed problems, because events release all threads in same time.
As first, we released event's flag after that lock thread increment counter then unlock thread. In my opinion is not necessary to
hold lock longer. When all threads arrive to barrier they are released.


#### Sum up: Events - release all threads now/straight, Semaphore - release threads randomly. 

### Fibonacci

#### Sum up: 






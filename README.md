# Documentation exercise 01  
###### Written by Marián Šebeňa
###### Python Interpreter 3.9
### Assigment 
You can find assigment on this  **[link](https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/).** 
#### Short description 
Implement two threads that will use a common index in a common field (initialized to 0) 
of a certain size. Let each thread increment the element of the array where the common 
index is pointing. Then let the index increase. 
If the index is already pointing out of the field, the thread terminates. 
When the threads end, calculate how many elements of the array have a value of 1.
### Resources
When you click on links below you will be redirected on resource web page: </br>
**[PPDS Youtube channel](https://www.youtube.com/channel/UCnTxtvNFlicb2Mn0a6w8N-A)** <br/>
**[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)** <br/>
**[PEP8](https://realpython.com/python-pep8/#naming-conventions)** <br/>
**[UIM/PPDS](https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/)** <br/>
**[.md syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)** <br/>
**[Timer](https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution)** <br/>

### Lock while loop
This option is the easiest way to understand and implement. As we can see in **[solution_01](https://github.com/marianSTU/ppds_marian.sebena/blob/01/solution_01/solution_01.py)**,
whole ***while loop*** is lock. It means that only one thread can execute ***loop*** while second thread waits.
Second thread have to wait until first thread pass the lock.
#### Sum up: Shared object's index increments only one thread. 

### Lock inside while loop
In this option we use lock inside ***while loop***. As we can see  in **[solution_02](https://github.com/marianSTU/ppds_marian.sebena/blob/01/solution_02/solution_02.py)** 
We do it before comparison for more reasons.
1. Code executes more than one thread. Every iteration execute another thread.
2. If more threads reach comparison at same time could cause deadlock.


#### Sum up: Incrementation is lock inside ***while loop***

### Experiments
In **[experiment](https://github.com/marianSTU/ppds_marian.sebena/blob/01/testing/example_01.py)** we tested impact of used solutions with different size of array on algorithm speed. 
Before we started experiment our opinion was the using locks inside white loop will be faster, because of 2 thread 
parallel running. Surprisingly not and the reason why could be repeating locking and unlocking threads.In first
option we do only once this operation. Results and comparison you can see in table below.

SizeOfArr | 100 | 1_000 | 10_000 | 100_000 | 1_000_000 | 10_000_000
--- | --- | --- | --- |--- |--- |---  
InLoopSolution | insignificant | insignificant | insignificant | 0.100sec | 1.31sec | 13.86sec
OutLoopSolution | insignificant | insignificant | insignificant | 0.034sec | 0.28sec | 2.17sec 
SpeedDifference | --------------- | --------------- | --------------- | 3x | 4.67x | 6.39x

#### Deadlock: 
During programming occurred deadlock. 
When we forgot to unlock the thread which stay locked and program could not by terminated.
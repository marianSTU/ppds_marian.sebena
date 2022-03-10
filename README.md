# Documentation exercise 03  
###### Written by Marián Šebeňa
###### Python Interpreter 3.9
### Assigment 
You can find assigment on this  **[link](https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-%F0%9F%92%A1/).** 
#### Short description 

### Resources
When you click on links below you will be redirected on resource web page: </br>
**[PPDS Youtube channel](https://www.youtube.com/channel/UCnTxtvNFlicb2Mn0a6w8N-A)** <br/>
**[UIM/PPDS](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F)** <br/>
### Producer Consumer
In this exercise We firstly test program from lecture. We created variable storage in class shared
to check how access of threads in objects of this class. When producer produced an item variable storage 
incremented by 1 and when consumer took an item storage decremented by 1. We tested a lot of variations number of
producer a consumer and control which thread has already accessed to object Shared. Question was why the threads
accessed differently in time. In my opinion because of competitive execution.

##### Comparison of producer and consumer
As we can see first sleep just simulate time when item is creating. Then
producers threads wait to access into storage when they could take a mutex
to be sure that nobody(instead current thread) is in the storage. Save item in
storage and unlock mutex. 
```
def producer(shared):
    while True:
        sleep(randint(1, 10)/10)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.storage += 1
        shared.mutex.unlock()
        shared.items.signal()
```
```
def consumer(shared):
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.storage -= 1
        shared.mutex.unlock()
        shared.items.signal()
        sleep(randint(1, 10) / 10)
```

#### Sum up: 







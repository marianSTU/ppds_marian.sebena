# Documentation exercise 04
###### Written by Marián Šebeňa
###### Python Interpreter 3.9
### Assigment 
You can find assigment on this  **[link](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/).** 
#### Short description 
The nuclear power plant has 3 sensors:

one primary circuit coolant flow sensor (sensor P)<br/>
one primary circuit coolant temperature sensor (T sensor)<br/>
one control rod insertion depth sensor (sensor H)<br/><br/>
These sensors are constantly trying to update the measured values. They store the data in a common data repository. Each sensor has its own dedicated space in the storage, where it stores data (take into account when synchronizing).

The sensors update every 50-60 ms. The data update itself takes 10-20 ms for sensor P and T for sensor T, but it takes 20-25 ms for sensor H.

In addition to the sensors, there are eight operators in that power plant, who constantly look at each of their monitors, where the measured values ​​of the sensors are displayed. The data update request is sent by the monitor continuously and continuously in a cycle. One update takes 40-50 ms.

Monitors can only start working if all sensors have already delivered valid data to the repository.
### Resources
When you click on links below you will be redirected on resource web page: </br>
**[PPDS Youtube channel](https://www.youtube.com/channel/UCnTxtvNFlicb2Mn0a6w8N-A)** <br/>
**[UIM/PPDS](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F)** <br/>

### Nuclear power station 1
### Nuclear power station 2
#####Pseudocode

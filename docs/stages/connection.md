# Connection

### 1. Extract IP address of current host computer attached to stages:
Open command prompt and use following command:
```
ipconfig
```

![](../assets/ip_fetch.png)

From the output use Ethernet adapter's IPv4 Address.

### 2. Get Port for ASCII server:
Open A3200 Configuration Manager and in the left pane go to following parameter:

**config_file -> System -> Communication -> ASCII -> CommandPort**

![](../assets/port_fetch.png)

Note: Keep all other parameters default for now.


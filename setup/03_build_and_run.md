# Build

Help:
```bash
./build -h
```

Build all software:
```bash
./build
```

Build individual components:
```bash
./build sensors
```

<br/>
<br/>

# Clean

Help:
```bash
./clean -h
```

Clean all software:
```bash
./clean
```

Clean individual components:
```bash
./clean sensors
```

<br/>
<br/>

# Run

**NOTE: THIS WILL ONLY WORK ON LITTLE BLUE. DEVELOPER MACHINES WOULD NEED TO MIMIC THE SETUP OF LITTLE BLUE.**

Help:
```bash
./run -h
```

Run all software with no rviz:
```bash
./run
```

Run all software with rviz:
```bash
./run -rviz
```

Run individual components:
```bash
./run gps
```

Run individual components with rviz:
```bash
./run -rviz imu
```

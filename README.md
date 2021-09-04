# Working Timer

This is a timer that repeats work and rest for a specified number of times.

For example, if the work time is 50 minutes, the rest time is 10 minutes, and the number of repetitions is 3, the timer will run as follows

Work(50min) --> Rest(10min) --> Work(50min) --> Rest(10min) --> Work(50min)

At the end of each work and break, a voice speech will be read out loud, and after waiting for 2 seconds, the next phase will start automatically.

## How to use

Please just execute the following command.

```bash
$ python timer.py
```

## Sceenshot

<img src="https://user-images.githubusercontent.com/6835793/132087820-93da09ab-3787-42b7-b11d-206d79827d2d.png" width=400px>

<img src="https://user-images.githubusercontent.com/6835793/132088115-1a5fac76-8da2-49fd-be28-278b4d4f5ee7.png" width=400px>

## Notice
- If you are running the program for the first time in a Windows environment, run the following command to enable speechreading.
  ```
  $ pip install pywin32
  ```

- Before running the program, prepare the following configuration file.
  - config.ini
    ```bash
    [DEFAULT]
    TimeWork = 50    ; time span for working (min)
    TimeBreak = 10   ; time span for breaking (min)
    Iteration = 5    ; number of Iteration
    ```
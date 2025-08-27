# Wahoo .plan File Format Description

Wahoo `.plan` files are plain text files used to define structured cycling workouts. They are typically uploaded to Wahoo ELEMNT head units or other compatible training software.

## Structure

A `.plan` file is divided into two main sections:

1.  **HEADER Section:** Contains metadata about the workout.
2.  **STREAM Section:** Defines the sequence of intervals.

---

## HEADER Section

This section starts with `=HEADER=` and contains key-value pairs for workout metadata. Each piece of metadata is on a new line.

### Required Fields:

*   `NAME=<Workout Name>`: The name of the workout (e.g., `NAME=4x4 Intervals`).
*   `DURATION=<Total Duration in Seconds>`: The total planned duration of the workout in seconds (e.g., `DURATION=3600`).
*   `TSS=<Training Stress Score>`: The estimated Training Stress Score for the workout (e.g., `TSS=75`).
*   `IF=<Intensity Factor>`: The estimated Intensity Factor for the workout (e.g., `IF=0.85`).

### Optional Fields:

*   `DESCRIPTION=<Description Line>`: One or more lines providing a description of the workout. Each line starts with `DESCRIPTION=`. (e.g., `DESCRIPTION=This is a tough workout.`).

---

## STREAM Section

This section starts with `=STREAM=` and defines the actual intervals of the workout. Intervals can be simple or complex (with subintervals and repetitions).

### Basic Interval Structure:

Each basic interval starts with `=INTERVAL=` and contains:

*   `INTERVAL_NAME=<Interval Name>`: The name of the interval (e.g., `INTERVAL_NAME=Warm-up`).
*   `PERCENT_FTP_HI=<Percentage of FTP>`: The target intensity for the interval, as a percentage of Functional Threshold Power (FTP). (e.g., `PERCENT_FTP_HI=75`).
*   `MESG_DURATION_SEC>=<Duration in Seconds>?EXIT`: The duration of the interval in seconds. The `?EXIT` part is a command for the Wahoo device to proceed to the next interval after this duration. (e.g., `MESG_DURATION_SEC>=300?EXIT`).

### Complex Interval Structure (with Subintervals and Repetitions):

For blocks of repeating intervals, you use a main `=INTERVAL=` block that contains `=SUBINTERVAL=` entries.

*   **Main Interval Block:**
    *   Starts with `=INTERVAL=`.
    *   `INTERVAL_NAME=<Block Name>`: Name for the entire block (e.g., `INTERVAL_NAME=Main Set`).
    *   `REPEAT=<Number of Repetitions>`: Specifies how many times the `subintervals` within this block should be repeated (e.g., `REPEAT=4`).
    *   `MESG_DURATION_SEC>=0?EXIT`: This line is typically present in repeating blocks and indicates that the block's duration is determined by its subintervals and repetitions.

*   **Subintervals:**
    *   Each subinterval starts with `=SUBINTERVAL=`.
    *   `INTERVAL_NAME=<Subinterval Name>`: Name for the subinterval (e.g., `INTERVAL_NAME=Work`).
    *   `PERCENT_FTP_HI=<Percentage of FTP>`: Target intensity for the subinterval.
    *   `MESG_DURATION_SEC>=<Duration in Seconds>?EXIT`: Duration of the subinterval.

---

## Example Snippet:

```
=HEADER=

NAME=My Custom Workout
DURATION=1800
TSS=45
IF=0.75
DESCRIPTION=A simple workout with warm-up and main set.

=STREAM=

=INTERVAL=
INTERVAL_NAME=Warm-up
PERCENT_FTP_HI=50
MESG_DURATION_SEC>=300?EXIT

=INTERVAL=
INTERVAL_NAME=Main Set
REPEAT=3
MESG_DURATION_SEC>=0?EXIT

=SUBINTERVAL=
INTERVAL_NAME=Work
PERCENT_FTP_HI=100
MESG_DURATION_SEC>=120?EXIT

=SUBINTERVAL=
INTERVAL_NAME=Rest
PERCENT_FTP_HI=40
MESG_DURATION_SEC>=60?EXIT
```

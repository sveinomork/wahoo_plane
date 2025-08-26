# Example: 4x4 3-2-1 Workout

This example demonstrates how to use the YAML to .plan converter with a structured cycling workout.

## Workout Description

**4x4 3-2-1** is an intensive cycling workout featuring:
- Warm-up phases at lower intensities
- 4 repetitions of 4-minute intervals at 105% FTP with recovery
- Pyramid finish: 3-2-1 minute intervals at 105% FTP
- Cool-down period

**Total Duration:** 57 minutes (3420 seconds)  
**TSS:** 62  
**IF:** 0.81

## Files in this Example

- `4x4-3-2-1.yaml` - Source workout definition in YAML format
- `4x4-3-2-1.plan` - Original .plan file (for reference)
- `4x4-3-2-1_generated_by_library.plan` - Generated .plan file from YAML

## How to Run the Example

### 1. Convert YAML to .plan format

From the project root directory, run:

```bash
python yaml_to_plan.py example/4x4-3-2-1.yaml example/4x4-3-2-1.plan
```

This will generate: `example/4x4-3-2-1_generated_by_library.plan`

### 2. Compare the files

You can compare the original and generated files to verify the conversion:

```bash
# On Windows
fc example\4x4-3-2-1.plan example\4x4-3-2-1_generated_by_library.plan

# On Linux/Mac
diff example/4x4-3-2-1.plan example/4x4-3-2-1_generated_by_library.plan
```

### 3. Using with uv

If you're using `uv` for dependency management:

```bash
uv run python yaml_to_plan.py example/4x4-3-2-1.yaml example/4x4-3-2-1.plan
```

## YAML Structure Explained

```yaml
name: 4x4 3-2-1                    # Workout name
duration: 3420                     # Total duration in seconds
tss: 62                            # Training Stress Score
if: 0.81                           # Intensity Factor
description:                       # Multiple description lines
  - 4x4 på 105%, avsluttet med 3-2-1 pyramide.
  - Selvkomponert

intervals:
  # Simple intervals
  - name: WARM UP
    percent_ftp: 50                # 50% of FTP
    duration: 300                  # 5 minutes

  # Complex intervals with repetitions
  - name: 4X2min 75-65
    repeat: 3                      # Repeat this block 3 times
    subintervals:
      - name: 4 min Tempo
        percent_ftp: 105           # 105% of FTP
        duration: 240              # 4 minutes
      - name: 3 min Hvile
        percent_ftp: 50            # Recovery at 50% FTP
        duration: 180              # 3 minutes
```

## Workout Structure Breakdown

1. **Warm-up** (10 minutes total)
   - 5 min at 50% FTP
   - 5 min at 60% FTP

2. **Main Set** (21 minutes total)
   - 3 x (4 min at 105% FTP + 3 min recovery at 50% FTP)

3. **Pyramid Finish** (6 minutes total)
   - 3 min at 105% FTP + 2 min recovery
   - 2 min at 105% FTP + 1 min recovery
   - 1 min at 105% FTP

4. **Cool-down**
   - 10 min at 50% FTP

## Testing the Conversion

Run the test suite to verify the converter works correctly:

```bash
uv run pytest tests/test_yaml_to_plan.py -v
```

This will test that the YAML input produces the expected .plan output format.
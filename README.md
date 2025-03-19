# Flow Log Parser

## Overview

This program parses AWS VPC Flow Logs (default format, version 2) and maps each log entry to a tag based on a lookup table provided as a CSV file. The program then generates an output file containing:

- **Tag counts**: The number of times each tag appears.
- **Port/Protocol combination counts**: The occurrences of each `(dstport, protocol)` combination.

The tool can handle:

- **Flow log files up to 10MB in size**
- **Lookup tables with up to 10,000 mappings**
- **Case-insensitive matching for protocol names**

## Assumptions

1. **Supported Flow Log Format**:

   - The program **only supports AWS VPC Flow Logs in the default format, version 2**.
   - Custom log formats are **not supported**.
   - Each log entry is expected to have at least **11 space-separated fields**.

2. **Lookup Table Constraints**:

   - The lookup table must be in **CSV format** with exactly 3 columns: `dstport, protocol, tag`.
   - The **same tag can be mapped to multiple port/protocol combinations**, but each `(dstport, protocol)` pair **can only have one tag**.
   - The lookup table **does not contain duplicate (dstport, protocol) pairs**.

3. **Protocol Handling**:

   - Protocols are stored as **case-insensitive strings** (`tcp`, `udp`, `icmp`, etc.).
   - If the Flow Log contains protocol numbers (`6`, `17`, etc.), they are mapped to their corresponding names.
   - The supported protocol mappings include:
     ```json
     {
         "6": "tcp",
         "17": "udp",
         "1": "icmp",
         "50": "esp",
         "47": "gre",
         "58": "icmpv6"
     }
     ```

## Installation

### Prerequisites

- **Python 3.6+** is required.
- No additional libraries need to be installed.

### Running the Program

To execute the parser, run:

```bash
python processLog.py <flow_log_file> <lookup_file> <output_file>
```

Example:

```bash
python processLog.py vpc_flow_logs.txt lookup.csv output.txt
```

### Input Files

- **Flow Log File (`vpc_flow_logs.txt`)**
  - Contains AWS VPC Flow Logs (default format, version 2).
  - Must be a **plain text (ASCII) file**.
  - Size **up to 10MB**.
  
- **Lookup File (`lookup.csv`**)
  - Contains **destination port, protocol, and tag mappings**.
  - Must be a **CSV file with 3 columns** (`dstport, protocol, tag`).
  - Supports **up to 10,000 mappings**.

### Output File

The results are saved in `<output_file>`, containing Tag Counts and Port/Protocol Combination Counts.

#### **Tag Counts Example**

```
Tag Counts:
Tag,Count
sv_P2,1500
sv_P1,3000
email,2500
Untagged,5000
```

#### **Port/Protocol Combination Counts Example**

```
Port/Protocol Combination Counts:
Port,Protocol,Count
49187,tcp,4
49188,icmp,1
49189,udp,1
49191,tcp,2
49192,gre,1
49192,icmp,1
49192,tcp,3
49193,tcp,6
```

## Testing

### Functional Tests

1. **Basic functionality**: Verified that logs are correctly mapped to tags and counts are accurate.
2. **Case insensitivity**: Ensured that `TCP` and `tcp` are treated the same.
3. **Large file handling**: Successfully processed a **10.50MB log file with 100,000 lines**.
4. **Edge cases**:
   - Missing or malformed log entries are ignored.
   - Lookup table entries without a valid tag are handled gracefully.

### Performance Tests

- Processed **100,000 flow log entries** in under **2 seconds** on a standard machine.
- Ensured that **memory usage remains low** by using streaming file processing.

## Known Issues & Limitations

- **Custom Flow Log formats are not supported**.
- **IPv6 addresses are not separately handled** (they will be treated as standard IP addresses).

## Future Enhancements

- Add support for **custom Flow Log formats**.
- Support **additional network protocols**.
- Improve **error handling and logging** for better debugging.

## Contact

For any issues or feature requests, please open an issue on GitHub.&#x20;


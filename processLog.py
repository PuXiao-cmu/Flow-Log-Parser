import csv
import sys
from collections import defaultdict

def load_lookup_table(lookup_file):
    """Load lookup table from a CSV file."""
    lookup = {}
    try:
        with open(lookup_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 3:
                    continue  # Skip malformed rows
                dstport, protocol, tag = row
                key = (dstport.strip(), protocol.strip().lower())  # Case insensitive
                lookup[key] = tag.strip()
    except Exception as e:
        print(f"Error reading lookup file: {e}")
        sys.exit(1)
    return lookup

def process_flow_logs(flow_log_file, lookup_table):
    """Parse the flow log file and count tag occurrences."""
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    
    try:
        with open(flow_log_file, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.split()
                if len(parts) < 11:
                    continue  # Skip malformed lines
                
                dstport = parts[6]  # Destination port
                protocol = parts[7]  # Protocol (number)
                protocol_name = protocol_map.get(protocol, protocol)  # Convert protocol number to name
                key = (dstport, protocol_name.lower())
                
                tag = lookup_table.get(key, "Untagged")
                tag_counts[tag] += 1
                port_protocol_counts[key] += 1
    except Exception as e:
        print(f"Error reading flow log file: {e}")
        sys.exit(1)
    
    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    """Write results to the output file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("Tag Counts:\n")
            file.write("Tag,Count\n")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[0]):
                file.write(f"{tag},{count}\n")
            
            file.write("\nPort/Protocol Combination Counts:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in sorted(port_protocol_counts.items()):
                file.write(f"{port},{protocol},{count}\n")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

protocol_map = {
    "6": "tcp",
    "17": "udp",
    "1": "icmp",
    "50": "esp",
    "47": "gre",
    "58": "icmpv6"
}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python flow_log_parser.py <flow_log_file> <lookup_file> <output_file>")
        sys.exit(1)
    
    flow_log_file = sys.argv[1]
    lookup_file = sys.argv[2]
    output_file = sys.argv[3]
    
    lookup_table = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = process_flow_logs(flow_log_file, lookup_table)
    write_output(tag_counts, port_protocol_counts, output_file)
    
    print(f"Processing complete. Results saved to {output_file}")

import re

def parse_iperf(output_text):
    results = []
    pattern = r"(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+\.?\d*)\s+[KMG]Bytes\s+(\d+\.?\d*)\s+[KMG]bits/sec"
    matches = re.findall(pattern, output_text)

    for match in matches:
        results.append({
            'Interval': match[0],
            'Transfer': float(match[1]),
            'Bitrate': float(match[2])
        })
    return results
